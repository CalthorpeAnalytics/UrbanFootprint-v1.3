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


__author__ = 'calthorpe'

class ConfigEntityRelatedCollectionAdoption(object):
    """
        ConfigEntity QuerySet mixin that enables collections of the parent_config_entity to be inherited or merged with the child's own collection
    """

    def computed_policy_sets(self, **query_kwargs):
        """
            Return this instance's policy_sets if they are not an empty list, otherwise traverses the parent hierarchy until a non-empty policy_sets list or the GlobalConfig is encountered. The list of that ancestor is returned
            :param **query_kwargs - optional filtering to apply to the results
        :return: The computed results
        """
        return self._computed('policy_sets', **query_kwargs)

    def computed_built_form_sets(self, **query_kwargs):
        """
            Return this instance's built_form_sets if they are not an empty list, otherwise traverses the parent hierarchy until a non-empty policy_sets list or the GlobalConfig is encountered. The list of that ancestor is returned
            :param **query_kwargs - optional filtering to apply to the results
        :return: The computed results
        """
        return self._computed('built_form_sets', **query_kwargs)

    def computed_db_entities(self, **query_kwargs):
        """
            Return this instance's db_entities_interests if they are not an empty list, otherwise traverses the parent hierarchy until a non-empty db_entities list or the GlobalConfig is encountered. The list of that ancestor is returned
            :param **query_kwargs - optional filtering to apply to the results
        :return:
        """
        db_entities = self._computed_related('db_entities', **query_kwargs)
        for db_entity in db_entities:
            if db_entity.schema not in self.schema() and db_entity.schema != 'global':
                raise Exception("For some reason the DbEntity schema {0} is not part of the ConfigEntity schema hierarchy {1}".format(db_entity.schema, self.schema()))
        return db_entities

    def computed_db_entity_interests(self, **query_kwargs):
        """
            Like computed_db_entities, but returns the through DbEntityInterest instance instead of the DbEntityInterest
        :param query_kwargs:
        :return:
        """
        return self._computed('db_entities', **query_kwargs)

