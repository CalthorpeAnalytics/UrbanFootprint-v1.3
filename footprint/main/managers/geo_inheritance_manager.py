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
from django.contrib.gis.db.models import GeoManager
from django.contrib.gis.db.models.query import GeoQuerySet
from django.db import transaction, IntegrityError
from model_utils.managers import InheritanceManager, InheritanceQuerySet
from django.contrib.gis.geos import Polygon
from footprint.main.lib.functions import dual_map_to_dict

__author__ = 'calthorpe_associates'


class GeoInheritanceQuerySet(GeoQuerySet, InheritanceQuerySet):

    def result_fields_and_title_lookup(self):

        # Find the feature_class parent field so we can remove it from the result fields.
        parent_fields = map(lambda field: field.name + '_id', self.model._meta.parents.values())
        omit_fields = parent_fields+['wkb_geometry']

        # Call query_result.values() to gain access to the field names.
        values_query_result = self if hasattr(self, 'field_names') else self.values()
        result_fields = filter(lambda field_name: field_name not in omit_fields, values_query_result.field_names)
        return (
            result_fields,
            # Find normal field titles
            #titles = map(lambda tup: self.cleanup_title(tup[1]), values_query_result.query.select)
            # Create a lookup from field name to title
            dual_map_to_dict(lambda key, value: [key, value], result_fields, result_fields))

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
