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

__author__ = 'calthorpe_associates'

class DbEntities(models.Model):

    db_entities = models.ManyToManyField('DbEntity', through='DbEntityInterest')

    def add_db_entity_interests(self, *db_entity_interests):
        """
            Adds one or more unsaved DbEntityInterests to the instance's collection.
            If the instance has not yet overridden its parents' db_entities by adding at least one DbEntityInterest,
            the parents DbEntityInterests will be adopted and then the db_entity_interests give here will be added
        :return:
        """
        # This check exists to avoid infinite recursion, since db_entity_interests are sometimes added post_config_entity_save handler
        if len(db_entity_interests) > 0:
            # Even though the field name is db_entities, we need to pass the DbEntityInterests
            self._add('db_entities', *db_entity_interests)
            # Update the selections property to mark db_entities as selected that have a unique key.
            self._select_implicit_defaults('db_entities')

    def remove_db_entity_interests(self, *db_entity_interests):
        self._remove('db_entities', *db_entity_interests)

    class Meta:
        abstract = True
