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
from django.db import models

__author__ = 'calthorpe'

class TooManyFoundException(Exception):
    pass

# http://www.djangosnippets.org/snippets/562/#c673
class QuerySetManager(models.Manager):
    # http://docs.djangoproject.com/en/dev/topics/db/managers/#using-managers-for-related-object-access
    # Not working cause of:
    # http://code.djangoproject.com/ticket/9643
    use_for_related_fields = True
    def __init__(self, qs_class=models.query.QuerySet):
        self.queryset_class = qs_class
        super(QuerySetManager, self).__init__()

    def get_query_set(self):
        return self.queryset_class(self.model)

    def __getattr__(self, attr, *args):
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_query_set(), attr, *args)

class CustomQuerySet(models.query.QuerySet):
    """
        Adds general methods to the default QuerySet class
    """

    def one_or_none(self, **kwargs):
        """
            Raise an exception unless 0 or 1 results are found upon filtering
        :param kwargs:
        :return:
        """
        results = self.filter(**kwargs)
        if len(results) > 1:
            raise TooManyFoundException("Expected 0 or 1 result but found {1}. Found: {2}".format(len(results), list(results)))
        return results[0] if len(results)==1 else None

    @classmethod
    def as_manager(cls, ManagerClass=QuerySetManager):
        return ManagerClass(cls)
