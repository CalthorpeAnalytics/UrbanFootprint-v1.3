# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2012 Calthorpe Associates
#
# This program is free software: you can redistribute it and/or modify it under the terms of the # GNU General Public License as published by the Free Software Foundation, version 3 of the License.

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
from django.utils import unittest
from footprint.utils.utils import has_explicit_through_class

__author__ = 'calthorpe'

class SetComparer(object):

    def __init__(self, test, parent_config_entity, enhanced_config_entity, reduced_config_entity, attribute, set_generator):
        """
            Compares set data between a parent ConfigEntity and two children
        :param parent_config_entity: The parent ConfigEntity of the two other given entities
        :param enhanced_config_entity: A child ConfigEntity with one set added in addition to the parent's
        :param reduced_config_entity: A child ConfigEntity with one set removed from the parent's. Set this to None to exclude tests on a reduced instance
        :param attribute: 'policy_sets', 'built_form_sets', etc
        :param set_generator: a lambda that returns a new set item, which will be added to the set (or used with a through instance)
        """
        self.test = test
        self.parent_config_entity = parent_config_entity
        self.enhanced_config_entity = enhanced_config_entity
        self.reduced_config_entity = reduced_config_entity
        self.attribute = attribute
        self.item_generator = set_generator
        # Detect if this Many field has an explicit Through class
        self.is_through = has_explicit_through_class(self.parent_config_entity, self.attribute)

    def compare_sets(self, enhanced_difference=1, reduced_difference=1, **kwargs):
        """
            This procedure manipulates a parent ConfigEntity and checks the affect on sets of two children. This procedure leaves the instances in their passed in state.
        :param enhanced_difference: Defaults to N=1. The enhanced_config_entity should have N more sets than the parent
        :param reduced_difference: Defaults to N=1. The reduced_config_entity should have N fewer
        :param kwargs: optional query filter to apply to the _computed() method
        :return:
        """

        # We expect one more set in the enhanced region than its parent
        self.test.assertEqual(
            len(self.enhanced_config_entity._computed(self.attribute, **kwargs)),
            len(self.parent_config_entity._computed(self.attribute, **kwargs)) + enhanced_difference)
        # We expect one less set in the reduced region than its parent
        if self.reduced_config_entity:
            self.test.assertEqual(len(self.reduced_config_entity._computed(self.attribute, **kwargs)),
                len(self.parent_config_entity._computed(self.attribute, **kwargs)) - reduced_difference)
        # Try adding a set to the parent and make sure the children respond
        self.confirm_set_added_to_parent(enhanced_difference, reduced_difference, **kwargs)

        # Save a list of all items, including those adopted from the parent. These are either the through instances or normal instances
        saved_items = list(self.enhanced_config_entity._computed(self.attribute, **kwargs))
        if self.is_through:
            # Remove the pk to make these through items seem new, since we'll clear the originals below
            for item in saved_items:
                item.pk=None

        # Clear the enhance_config_entity's items
        self.enhanced_config_entity._clear(self.attribute)
        self.enhanced_config_entity.save()
        # We expect pk equality with parent's sets
        self.test.assertEqual(map(lambda set: set.pk, self.enhanced_config_entity._computed(self.attribute, **kwargs)),
            map(lambda set: set.pk, self.parent_config_entity._computed(self.attribute, **kwargs)))
        # Restore the self.enhanced_config_entity items by adding the old computed items
        # Even though donor items are part of the saved_items, they should be ignored by the add process, since they are already present
        self.enhanced_config_entity._add(self.attribute, *saved_items)
        # Ensure that the original number now exist even though the save_sets contained some of the parent's
        self.test.assertEqual(
            len(self.enhanced_config_entity._computed(self.attribute, **kwargs)),
            len(self.parent_config_entity._computed(self.attribute, **kwargs)) + enhanced_difference)

    def confirm_set_added_to_parent(self, enhanced_difference=1, reduced_difference=1, **kwargs):
        # Add a new item to parent
        generated_item = self.item_generator(self.parent_config_entity)
        # We expect the enhanced_region to continue to have 'difference' more items
        self.test.assertEqual(
            len(self.enhanced_config_entity._computed(self.attribute, **kwargs)),
            len(self.parent_config_entity._computed(self.attribute, **kwargs)) + enhanced_difference,
            "Expected a difference of {0} between {1} and {2}".format(
                enhanced_difference,
                self.enhanced_config_entity._computed(self.attribute, **kwargs),
                self.parent_config_entity._computed(self.attribute, **kwargs)))
        # We expect the reduced_region to continue to have 'difference' fewer items
        if self.reduced_config_entity:
            self.test.assertEqual(
                len(self.reduced_config_entity._computed(self.attribute, **kwargs)),
                len(self.parent_config_entity._computed(self.attribute, **kwargs)) - reduced_difference,
                "Expected a difference of {0} between {1} and {2}".format(
                    reduced_difference,
                    self.reduced_config_entity._computed(self.attribute, **kwargs),
                    self.parent_config_entity._computed(self.attribute, **kwargs)))
        # Remove that last item from the parent
        self.parent_config_entity._remove(self.attribute, generated_item)
        # Again we expect the config_entities to have updated according to the parent
        self.test.assertEqual(
            len(self.enhanced_config_entity._computed(self.attribute, **kwargs)),
            len(self.parent_config_entity._computed(self.attribute, **kwargs)) + enhanced_difference,
            "Expected a difference of {0} between {1} and {2}".format(
                enhanced_difference,
                self.enhanced_config_entity._computed(self.attribute, **kwargs),
                self.parent_config_entity._computed(self.attribute, **kwargs)))
        if self.reduced_config_entity:
            self.test.assertEqual(
                len(self.reduced_config_entity._computed(self.attribute, **kwargs)),
                len(self.parent_config_entity._computed(self.attribute, **kwargs)) - reduced_difference,
                "Expected a difference of {0} between {1} and {2}".format(
                    reduced_difference,
                    self.reduced_config_entity._computed(self.attribute, **kwargs),
                self.parent_config_entity._computed(self.attribute, **kwargs)))

