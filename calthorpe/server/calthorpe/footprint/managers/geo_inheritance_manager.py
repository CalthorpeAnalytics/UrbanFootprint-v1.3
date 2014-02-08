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

__author__ = 'calthorpe'

class GeoInheritanceQuerySet(GeoQuerySet, InheritanceQuerySet):
    pass

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
