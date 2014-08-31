# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2012 Calthorpe Associates
#
# This program is free software: you can redistribute it and/or modify it under the terms of the
 # GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
#
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates.
# Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709.
# Phone: (510) 548-6800. Web: www.calthorpe.com
import string
from django.contrib.gis.db.models import GeoManager
from django.contrib.gis.db.models.query import GeoQuerySet, GeoValuesQuerySet
from django.db import transaction, IntegrityError
from model_utils.managers import InheritanceManager, InheritanceQuerySet
from django.contrib.gis.geos import Polygon
from footprint.main.lib.functions import get_first, compact, flat_map, map_to_dict

__author__ = 'calthorpe_associates'

class GeoInheritanceQuerySetMixin(object):
    def result_fields_and_title_lookup(self, related_models=[], map_path_segments={}):
        """
            Given the field_paths of the queryset, returns a tuple of two items.
            The first is the field_paths minus specifically omitted ones--the parent id and geometry column
            The second is a lookup from the field_path to a title appropriate for the user. The generated
            title uses '.' in place of '__'
            :param: related_models: pass the related_models represented in the query results so that unneeded
            paraent reference fields can be removed from the result fields
            :param: map_path_segments: An optional dict that matches segments of the field_paths. The value
            corresponding the key is the name to convert it to for the title. If the value is None it will
            be eliminated from the path when it is rejoined with '.'
        """

        # Find the feature_class parent field so we can remove it from the result fields.
        omit_fields = map(lambda field: field.name + '_id', self.model._meta.parents.values()) + \
            map(lambda field: field.name, flat_map(lambda related_model: related_model._meta.parents.values(), related_models))

        # Call query_result.values() to gain access to the field names.
        values_query_set = self if hasattr(self, 'field_names') else self.values()

        result_paths = filter(lambda field_name: field_name not in omit_fields, values_query_set.field_names)
        return (
            # Replace '__' with '_x_'. We can't use __ because it confuse tastypie
            map(lambda path: string.replace(path, '__', '_x_'), result_paths),
            # Create a lookup from field name to title
            # The only processing we do to the title is to remove the middle path
            map_to_dict(lambda path: [
                # Replace '__' with '_x_'. We can't use __ because it confuse tastypie
                string.replace(path, '__', '_x_'),
                # match each segment to map_path_segments or failing that return the segment
                # remove segements that map to None
                '__'.join(compact(map(lambda segment: map_path_segments.get(segment, segment), path.split('__'))))],
                result_paths)
        )

    def extent_polygon(self):
        """
            Convert extent into something more useful--a simple geos polygon
        """
        try:
            # This seems to raise if no rows exist
            extent = self.extent()
        except:
            return None
        bounds = Polygon((
            (extent[0], extent[1]),
            (extent[0], extent[3]),
            (extent[2], extent[3]),
            (extent[2], extent[1]),
            (extent[0], extent[1]),
        ))
        return bounds


class GeoInheritanceValuesQuerySet(GeoValuesQuerySet, GeoInheritanceQuerySetMixin):
    pass

class GeoInheritanceQuerySet(GeoQuerySet, InheritanceQuerySet, GeoInheritanceQuerySetMixin):
    def values(self, *fields):
        return self._clone(klass=GeoInheritanceValuesQuerySet, setup=True, _fields=fields)



class FootprintGeoManager(GeoManager):
    # http://djangosnippets.org/snippets/1114/
    def update_or_create(self, **kwargs):
        """
            updates, creates or gets based on the kwargs. Works like get_or_create but in addition will update
            the kwargs specified in defaults and returns a third value to indicate if an update happened
        :param kwargs:
        :return:
        """
        assert kwargs, 'update_or_create() must be passed at least one keyword argument'
        obj, created = self.get_or_create(**kwargs)
        defaults = kwargs.pop('defaults', {})
        if created:
            return obj, True, False
        else:
            try:
                params = dict([(k, v) for k, v in kwargs.items() if '__' not in k])
                params.update(defaults)
                for attr, val in params.items():
                    if hasattr(obj, attr):
                        setattr(obj, attr, val)
                sid = transaction.savepoint()
                obj.save(force_update=True)
                transaction.savepoint_commit(sid)
                return obj, False, True
            except IntegrityError, e:
                transaction.savepoint_rollback(sid)
                try:
                    return self.get(**kwargs), False, False
                except self.model.DoesNotExist:
                    raise e

    # Update the related instance or add it. The toMany equivalent to update_or_create
    def update_or_add(self, **kwargs):
        assert kwargs, 'update_or_add() must be passed at least one keyword argument'
        defaults = kwargs.pop('defaults', {})
        obj = get_first(self.filter(**kwargs))
        result = (obj, False, True)
        create = False
        if not obj:
            obj = self.model()
            result = (obj, True, False)
            create = True
        try:
            params = dict([(k, v) for k, v in kwargs.items() if '__' not in k])
            params.update(defaults)
            for attr, val in params.items():
                if hasattr(obj, attr):
                    setattr(obj, attr, val)
            sid = transaction.savepoint()
            obj.save(force_update=not create)
            if not create:
                self.add(obj)
            transaction.savepoint_commit(sid)

            return result
        except IntegrityError, e:
            transaction.savepoint_rollback(sid)

class GeoInheritanceManager(FootprintGeoManager, InheritanceManager):
    """
        Combines the GeoManager and Inheritance Managers into one. The get_query_set is overridden below to return a
        class that combines the two QuerySet subclasses
    """

    def get_query_set(self):
        return GeoInheritanceQuerySet(self.model)

    def __getattr__(self, attr, *args):
        """
            Pass unknown methods to the QuerySetManager
        :param attr:
        :param args:
        :return:
        """
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_query_set(), attr, *args)

class ProxyGeoInheritanceManager(GeoInheritanceManager):
    """
        Identical to GeoInheritanceManager, but limits the queryset to the passed in query params
        This is used for Proxy models that distinguish their rows in the table with a filter (e.g. key='core')
    """
    def __init__(self, **filter):
        self.filter = filter
        super(ProxyGeoInheritanceManager, self).__init__(self)

    def get_query_set(self):
        return super(ProxyGeoInheritanceManager, self).get_query_set().filter(**self.filter)
