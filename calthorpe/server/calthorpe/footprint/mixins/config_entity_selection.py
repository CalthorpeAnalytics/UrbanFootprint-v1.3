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
from footprint.lib.functions import map_to_keyed_collections

from footprint.utils.utils import has_explicit_through_class, foreign_key_field_of_related_class

__author__ = 'calthorpe'

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class ConfigEntitySelection(object):

    def select_policy_set(self, policy_set):
        """
            Stores a selected policy_set from one of those among computed_policy_sets(). This enables the use of selected_policy_set. Some classes, such as Scenario, must have a selected_policy_sets to carry out certain function. Selecting a policy_set has no bearing on the computed_policy_sets. However, selected_policy_set will default to the only set if only one exists in computed_policy_sets. If multiple exist and none are selected, selected_policy_set will raise an error
        :return:
        """
        self._select('policy_sets', policy_set)

    def deselect_policy_set(self):
        """
            Exactly the opposite of select_policy_set. No set will be selected after this is called, whether or not one was selected, unless there is exactly on set returned by computed_policy_sets()
        :return:
        """
        self.selections['sets']['policy_sets'] = None

    def selected_policy_set(self):
        """
            Returns the policy_set selected by select_policy_set, or the only policy_set if self.computed_policy_sets has exactly one set
        :return: the selected policy_set
        """
        return self._selected('policy_sets')

    def select_built_form_set(self, built_form_set):
        """
            Stores a selected built_form_set from one of those among computed_built_form_sets(). This enables the use of selected_built_form_set. Some classes, such as Scenario, must have a selected_built_form_sets to carry out certain function. Selecting a built_form_set has no bearing on the built_form_sets. However, selected_built_form_set will default to the only set if only one exists in computed_built_form_sets. If multiple exist and none are selected, selected_built_form_set will raise an error
        :return:
        """
        self._select('built_form_sets', built_form_set)

    def deselect_built_form_set(self):
        """
            Exactly the opposite of select_built_form_set. No set will be selected after this is called, whether or not one was selected, unless there is exactly on set returned by computed_built_form_sets()
        :return:
        """
        self.selections['sets']['built_form_sets'] = None

    def selected_built_form_set(self):
        """
            Returns the built_form_set selected by built_form_set, or the only built_form_set if self.computed_built_form_sets has exactly one set
        :return: the selected built_form_set
        """
        return self._selected('built_form_sets')

    def selected_db_entities(self, **query_kwargs):
        """
            Like computed_db_entities, but only returns one DbEntity per unique DbEntity key based on which DbEntity in each shared key set is selected (or the only one for unshared keys)
        :param **query_kwargs - optional filtering to apply to the results
        :return:
        """
        db_entities = self._computed_related('db_entities', **query_kwargs)
        # There's probably an easier way to do this, but checking pks is the most obvious
        selected_db_entity_pks = map(lambda db_entity: db_entity.pk,
            filter(lambda db_entity: self._is_selected_of_shared_key('db_entities', db_entity),
                db_entities))
        return db_entities.filter(pk__in=selected_db_entity_pks)

    def selected_db_entity_interests(self, **query_kwargs):
        db_entities = self.selected_db_entities(**query_kwargs)
        return self.dbentityinterest_set.filter(db_entity__in=db_entities)

    def select_db_entity_of_key(self, db_entity_key, instance):
        return self._select_among_shared_key('db_entities', db_entity_key, instance)

    def selected_db_entity(self, db_entity_key):
        """
            A ConfigEntity may reference multiple DbEntities with the same key via DbEntityInterest. One of those with the same key may be marked as selected, or if only one exists it is considered selected. This method returns the 'selected' DbEntity of the given db_entity_key.
        :param db_entity_key
        :return: The selected DbEntity of the given db_entity_key
        """
        return self._selected_of_shared_key('db_entities', db_entity_key)

    def selected_db_entity_interest(self, db_entity_key):
        """
            A ConfigEntity may reference multiple DbEntities with the same key via DbEntityInterest. One of those with the same key may be marked as selected, or if only one exists it is considered selected. This method returns the 'selected' DbEntity of the given db_entity_key.
        :param db_entity_k
        :return: The DbEntityInterest of the selected DbEntity
        """
        selected_db_entity = self._selected_of_shared_key('db_entities', db_entity_key)
        return self.dbentityinterest_set.filter(db_entity=selected_db_entity)[0]

    def _select_implicit_defaults(self, attribute):
        """
            Inspect all of the items of the given shared-key collection and select those with unique keys to make them the default for that key. This insures that every key has a defaults in the selections[key'] dict
        :return: None
        """
        items_by_key = map_to_keyed_collections(lambda item: item.key, self._computed_related(attribute))
        for key, items in items_by_key.iteritems():
            if len(items)==1:
                # Single items always become the selected item for that key
                self._select_among_shared_key(attribute, key, items[0])
            else:
                # All keys that are shared should have something selected already
                try:
                    selection = self._selected_of_shared_key(attribute, key)
                except:
                    # This shouldn't happen, but log a warning and set the first item as the selected item
                    logger.warning("Instance {0} has no {1} with key {2} does not return exactly one set, but returns {3}".format(
                        self,
                        attribute,
                        key,
                        len(items)))
                    self._select_among_shared_key(attribute, key, items[0])

    def _select(self, attribute, value):
        """
            Selects the given value from among the collection indicated by attribute. The value is indicated by selected in the self.selections['sets'] dict
        :param attribute: The name of a collection of the instance, such as 'built_forms'
        :param value: An collection value that must be part of the collection indicated by the attribute
        :return:
        """
        if not value in self._computed_related(attribute):
            raise Exception("For instance {0}, {1} is not among the {2} in {3}".format(
                self,
                value,
                "computed_{0}".format(attribute),
                self._computed_related(attribute)))
        self.selections['sets'][attribute] = value

    def _selected(self, attribute):
        """
            Returns the selected value of the collection indicated by attribute. Raises an exception if selected value exists and there is not exactly one value in the collection.
        :param attribute: The name of a collection of the instance, such as 'built_forms"
        :return: The selected value or the only value of the collection if its a one-item collection
        """
        selection = self.selections['sets'].get(attribute, None)
        if selection:
            return selection
        if len(self._computed_related(attribute))==1:
            return self._computed_related(attribute)[0]
        raise "Instance {0} has no {1} selected does not return exactly one set, but returns {2}".format(
            self,
            attribute,
            len(self._computed_related(attribute)))

    def _is_selected(self, attribute, value):
        """
            Returns true if the value of the collection indicated by the given attribute is the value selected for that collection
        :param attribute:
        :param value:
        :return:
        """
        return self._selected(attribute) == value

    def query_prefix(self, attribute):
        """
            Get the key query name based on if the many-to-many attribute has an explicit through class or not
        :param attribute:
        :return:
        """
        if has_explicit_through_class(self, attribute):
            return "{0}__".format(foreign_key_field_of_related_class(
                self.many_field(attribute).through,
                self.many_field(attribute).model).name)
        else:
            return ''

    def _select_among_shared_key(self, attribute, key, value):
        """
            For ManyToMany attributes that mixin SharedKey, it's possible to have multiple items with the same key. With this method, one of the items with the same key can be selected, adding it to the self.selected dict.
        :param attribute: The attribute name of the ManyToMany field
        :param key: The common item key
        :param value:  The item among the items with the same key to be selected
        :return:
        """
        prefix = '' #self.query_prefix(attribute)
        kwargs = {"{0}{1}".format(prefix, 'key'):key, "{0}{1}".format(prefix, 'pk'):value.pk}
        if not len(self._computed_related(attribute, **kwargs))==1:
            raise Exception("For instance {0}, many-to-many item {1} with key {2} and pk {3} is not among the {4} in {5}".format(
                self,
                value,
                key,
                value.pk,
                "computed_{0}".format(attribute),
                self._computed_related(attribute)))
        self.selections[attribute][key] = value

    def _selected_of_shared_key(self, attribute, key):
        """
            Selects the ManyToMany item of the given attribute name that is selected for the given key. An exception is through if multiple items with the given key exist but non have been selected using _select_among_shared_key
        :param attribute: The name of a ManyToMany attribute of the instance
        :param key: A shared key string of the SharedKey mixin field
        :return: The item previously selected by _select_among_shared_key, or the only item with the given key if only one item exists.
        """
        selection = self.selections[attribute].get(key, None)
        if selection:
            return selection
        prefix = '' #self.query_prefix(attribute)
        kwargs = {"{0}{1}".format(prefix, 'key'):key}
        instances = self._computed_related(attribute, **kwargs)
        if len(instances)==1:
            return instances[0]
        raise Exception("Instance {0} has a selected item problem for attribute {1} with key {2}. It does not return exactly one item, but returns {3}".format(
            self,
            attribute,
            key,
            len(self._computed_related(attribute, **kwargs))))

    def _is_selected_of_shared_key(self, attribute, keyed_value):
        """
            Returns true if the given value of the given collection attribute is the selected instance for the values's key, as determined by _select_among_shared_key() or if it's the only instance of that key
        :param attribute: The attribute of a collection with shared keys, such as 'db_entities'
        :param keyed_value: A value of the collection indicated by attribute, having a key property
        :return:
        """
        return self._selected_of_shared_key(attribute, keyed_value.key)==keyed_value

