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
from footprint.lib.functions import get_list_or_if_empty

from footprint.utils.utils import has_explicit_through_class, foreign_key_field_of_related_class

__author__ = 'calthorpe'

class RelatedCollectionAdoption(object):

    def donor(self):
        """
            Mixers must override this method to return the donor instance
        :return: An instance containing the same ManyToMany fields as self to enable adoption of ManyToMany collection items
        """
        raise Exception("No donor defined. Override donor() in the mixer")

    def _add(self, attribute, *values):
        """
            Adds a many-to-many instance to this many field. For attributes with explicit through classes, the values must be the through instances. For non-explicit through classes the values must be the normal related instances
            :param attribute: the attribute of the many-to-many property
            :param values: the values to add. These must be through instances for explicit through classes or else related instances
        """
        # Prepare for adding new items by first adopt those of the donor, if needed        self._adopt_from_donor(attribute)
        self._adopt_from_donor(attribute)
        # Add only new items, or replace items with the same key (for non-SharedKey) items
        self._add_difference(attribute, *values)

    def _set(self, attribute, *values):
        """
            Sets the attribute collection to the given values. Existing values of matching pk (or matching related pk for through instances) are left alone rather than removing them and re-adding. This minimizes the number of changes for observers to mimic, and minimizes database writes
        :param attribute: the attribute of the many-to-many property
        :param values: the values to set. These must be through instances for explicit through classes or else related instances
        """
        # Remove existing values that are not in the incoming values
        self._subtract_difference(attribute, *values)
        # Prepare for adding new items by first adopt those of the donor, if needed
        self._adopt_from_donor(attribute)
        # Add only new items, or replace items with the same key (for non-SharedKey) items
        self._add_difference(attribute, *values)

    def _remove(self, attribute, *values, **kwargs):
        """
            Remove the given values from the collection of attribute, first adopting values from the donor in case the caller wishes to remove adopted values
        :param attribute:
        :param values:
        :param kwargs: The only options is 'skip_adopt', to prevent infinite recursion in internal calls
        :return:
        """


        # Adopt the donor values in case the caller wishes to remove some of those from self
        if not kwargs.get('skip_adopt', False):
            self._adopt_from_donor(attribute)
        if has_explicit_through_class(self, attribute):
            # If the Many has an explict through class, we must instead delete the through instances that reference the given values
            foreign_key_attribute = foreign_key_field_of_related_class(self.many_field(attribute).through, self.many_field(attribute).model).name
            filter = {"{0}__id__in".format(foreign_key_attribute):map(lambda v: v.id, values)}
            throughs = self.through_set(attribute).filter(**filter)
            self._remove_throughs(attribute, *throughs, **kwargs)
        else:
            # No explicit through, simply remove the values
            getattr(self, attribute).remove(*values)

    def _remove_throughs(self, attribute, *throughs, **kwargs):
        """
            Removes the specified through instances
        :param attribute:
        :param throughs:
        :param kwargs: The only options is 'skip_adopt', to prevent infinite recursion in internal calls
        :return:
        """

        # Adopt the donor instances in case the user wants to remove some of the donor instances
        if not kwargs.get('skip_adopt', False):
            self._adopt_from_donor(attribute)
        for through in throughs:
            through.delete()

    def _clear(self, attribute):
        """
            Deletes all instances of the given attribute belonging the self, resulting in it delegating calls to _computed to its donor
        :param attribute:
        :return:
        """
        if has_explicit_through_class(self, attribute):
            self._clear_throughs(attribute)
        else:
            getattr(self, attribute).clear()


    def _clear_throughs(self, attribute):
        """
            Deletes all through instances of the given attribute associated with self
        :param attribute:
        :return:
        """
        throughs = self.through_set(attribute).all()
        for through in throughs:
            through.delete()

    def _adopt_from_donor(self, attribute, force=False):
        """
            Adoption of a parent values takes place only when the child values are empty and about to add or remove a set. Adoption is needed because a child can simply inherit to parent values while it has no overrides, but once it has overrides it must manage the parent values more explicitly. If the parent changes its values after adoption, the child will receive signals from the parent (see self.parent_listeners())
        :param attribute: 'policy_sets', 'built_form_sets', etc
        :param force: optionally set to True to force the items of the donor to be added that aren't already adopted. This is used for through-class attributes because saving the initial through class instances makes it seems like self already has its own item attributes, even though the donor attributes haven't been adopted yet So force is used after the initial through class instances are saved
        :return:
        """
        if self.donor() and (force or len(getattr(self, attribute).all()) == 0):
            self._add_difference(attribute, *self.donor()._computed(attribute), from_donor=True)


    def _add_difference(self, attribute, *values, **flags):
        """
            Adds only those items not already in the list, according to the pk. If the instance class defines has a Key mixin, then the key attribute will be used to let an incoming instance replace an instance with the same key. For attributes with an explicit through class, values must be the through instances, and their equality to the current items will be tested by the foreign key pk, not the value's pk.
        :param attribute: 'policy_sets', etc.
        :param values: the related or through instances to add which might match instances already adopted from the donor
        :param flags: 'from_donor':True indicates that these values are coming from the 'donor', so shouldn't override Key instances with a matching key
        :return:
        """

        # Create functions for the attribute based on whether or not it has an explicit through class
        tool = AdoptionTool(self, attribute, **flags)
        # Get all values of the many attribute or the through attribute
        existing_values = getattr(self, tool.resolved_attribute).all()

        # Handle duplicate keys by removing parent instances with keys that match the child
        # This only applies to unique_key implementors
        # Remove the items with duplicate keys without adopting first (to prevent infinite recursion)
        self._remove(attribute, *tool.matching_existing_values_to_remove(values, existing_values), skip_adopt=True)

        # Get values that don't yet exist according to the pks (and key for unique_key implementors)
        new_values = tool.filter_out_duplicates(
            values,
            getattr(self, tool.resolved_attribute).all()) # call this again in case _remove eliminated duplicates

        if tool.is_through:
            for non_existing_value in new_values:
                # Set the foreign key relationship to self. This might already be done
                setattr(non_existing_value, tool.self_foreign_key_attribute, self)
                # Clear the pk in case the value is coming from the donor (via self._adopt_from_donor)
                setattr(non_existing_value, 'pk', None)
                non_existing_value.save()
        else:
            getattr(self, attribute).add(*new_values)

    def _subtract_difference(self, attribute, *values):
        """
            Removes existing values that are not specified in *values. This is used by _set()
        :param attribute:
        :param values:
        :return:
        """

        # Create functions for the attribute based on whether or not it has an explicit through class
        tool = AdoptionTool(self, attribute)
        # Get all values of the many attribute or the through attribute
        existing_values = getattr(self, tool.resolved_attribute).all()
        self._remove(attribute, *tool.unmatched_existing_values(values, existing_values), skip_adopt=True)

    def _get(self, attribute, **kwargs):
        """
            Gets an expected instance from the collection named by attr by calling get on the results of _computed(). Thus the instance will be queried for in combination of ancestrial and personal collection items.
            TODO what is this supposed to do, throw on no match?
        :param attr:
        :param kwargs:
        :return:
        """
        return self._computed(attribute, **kwargs)

    def _computed(self, attribute, **query_kwargs):
        """
            Returns this instance's attribute's related values or through values (for attributes with an explicit through class) or the donor's if this instance hasn't overridden its values
        :param attribute: 'db_entities', etc. Not the through attribute name (e.g. dbentities_set)
        :param **query_kwargs: optionally specify query arguments to use with filter() on the results
        :return: this attribute's collection or its parents, with optional filtering applied after
        """
        resolved_attribute = self.through_attribute(self.many_field(attribute)) if has_explicit_through_class(self, attribute) else attribute
        if self.donor():
            return get_list_or_if_empty(
                # Get instance's own Many items
                self._filter_computed(
                    getattr(self, resolved_attribute).all(),
                    **query_kwargs),
                # If none exist get donor's
                lambda: self.donor()._computed(attribute, **query_kwargs))
        else:
            # No donor is defined so just consider this instance's items
            return self._filter_computed(getattr(self, resolved_attribute).all(), **query_kwargs)

    def _filter_computed(self, all, **query_kwargs):
        return all.filter(**query_kwargs) if len(query_kwargs) > 0 else all

    def _computed_related(self, attribute, **query_kwargs):
        """
            Like _computed, but returns the related item of the through class instances for attributes having a through class. Attributes without an explict through class behave just like _computed()
        :param attribute: 'db_entities', etc. Not the through attribute name (e.g. dbentityinterest_set)
        :param query_kwargs: optional args to filter the results
        :return: The related class instances
        """
        if self.donor():
            return get_list_or_if_empty(
                # Get instance's own Many items
                self._filter_computed(
                    getattr(self, attribute).all(),
                    **query_kwargs),
                # If none exist get donor's
                lambda: self.donor()._computed_related(attribute, **query_kwargs))
        else:
            # No donor is defined so just consider this instance's items
            return self._filter_computed(getattr(self, attribute).all(), **query_kwargs)

    def through_class(self, attribute):
        return self.many_field(attribute).through

    def through_attribute(self, many_field):
        """
            Inspects the model field for an ManyToMany attribute with a through class to get the reference to the through instances. TODO this assumes the _set suffix but I know there's a way to override. I'm not sure how to inspect the through class to find the way that it should be referred to that overrides the lowercase_set attribute. It should used self.related_field to figure out the name
        :param through_class: The through class, such as DbEntityInterest
        :return: the set attr for self, such as 'dbentityinterest_set'
        """
        through_class = many_field.through
        return "{0}_set".format(through_class._meta.module_name)

    def through_set(self, attribute):
        return getattr(self, self.through_attribute(self.many_field(attribute)))

    def many_field(self, attribute):
        return getattr(self, attribute)

class AdoptionTool(object):

    def __init__(self, obj, attribute, **kwargs):
        self.obj = obj
        self.attribute = attribute
        self.from_donor = kwargs.get('from_donor', False)
        self.is_through = has_explicit_through_class(self.obj, attribute)
        if self.is_through:
            self.resolved_attribute = obj.through_attribute(obj.many_field(attribute))
            through_class = obj.through_class(attribute)
            self.self_foreign_key_attribute = foreign_key_field_of_related_class(through_class, obj.__class__).name
            self.foreign_key_attribute = foreign_key_field_of_related_class(through_class, obj.many_field(attribute).model).name
        else:
            self.resolved_attribute = attribute
            self.self_foreign_key_attribute = self.foreign_key_attribute = None

        self.related = getattr(obj,attribute).model

    def resolve_pk(self, value):
        return getattr(value, self.foreign_key_attribute).pk if self.is_through else value.pk

    def resolve_key(self, value):
        return getattr(value, self.foreign_key_attribute).key if self.is_through else value.key

    def filter_out_duplicates(self, added_values, existing_values):
        """
            If the item class implements Key, filters out matching items matching existing items if flags['from_donor'] is True. We don't want the donor to replace a value having a matching key, because the donees choice for that Key should take precedence. If the value is not from the donor, then it's fine to replace a value having a matching key
        :param added_values:
        :return:
        """
        # Get the existing pks of the many or through items
        existing_value_pks = map(lambda value: self.resolve_pk(value), existing_values)
        new_values = filter(lambda value: not self.resolve_pk(value) in existing_value_pks, added_values)
        if hasattr(self.related, 'unique_key') and self.related.unique_key():
            existing_keys = map(lambda value: self.resolve_key(value), existing_values)
            return filter(lambda value: not self.from_donor or self.resolve_key(value) not in existing_keys, new_values)
        else:
            return new_values

    def matching_existing_values_to_remove(self, new_values, existing_values):
        """
            Get rid existing items matching incoming items by key if keys must be unique. Only allow this if the incoming items are not being adopted from the donor, since we never want the donor items to override this instance's. This applies to the corner case where the donor adds or changes its item of a certain key and the adoptor already has an item of that key. Ideally the adoptor would take the change if and only if their item matched the item of the donor being replaced, meaning the adoptor was really just mirroring the donor's item.
        :param new_values: incoming values via obj._set or obj._add
        :param existing_values: values of the attribute that already exist
        :return: the existing_values to be removed because new_values have conflicting keys
        """

        if hasattr(self.related, 'unique_key') and self.related.unique_key():
            incoming_keys = map(lambda value: self.resolve_key(value), new_values)
            return filter(lambda value: self.resolve_key(value) in incoming_keys and not self.from_donor, existing_values)
        else:
            return []

    def unmatched_existing_values(self, new_values, existing_values):
        """
            Find existing values that do not match the new_values according to the result of resolve_pk. For obj._set operations, these unmatched values will need to be removed
        :param new_values: values meant to replace the existing_values.
        :param existing_values: The existing values of the attribute collections
        :return: The unmatched existing values that will need to be removed
        """
        new_value_pks = map(lambda value: self.resolve_pk(value), new_values)
        return filter(lambda value: self.resolve_key(value.pk) not in new_value_pks, existing_values)

