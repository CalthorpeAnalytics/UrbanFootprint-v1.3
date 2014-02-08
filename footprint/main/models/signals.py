# coding=utf-8
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

from django.dispatch import Signal


__author__ = 'calthorpe_associates'

# Defines custom Django Signals that are used by UrbanFootprint models instances to communicate
initialize_media = Signal(providing_args=[])
initialize_presentations = Signal(providing_args=[])

def items_changed(attribute):
    def _items_changed(sender, **kwargs):
        """
            Listens for m2m signals on ConfigEntity instances. The instance alerts its children of the change so that
            can update their adopted collections as needed
        :param sender:
        :param kwargs:
        :return:
        """
        donor = kwargs['instance']
        donees = donor.children()
        action = kwargs['action']
        if action=='post_add':
            # If the donee instance's related list is nonempty, add any that the donor added (empty ones will get the
            # change by deferring to the donor's list)
            for donee in donees:
                manager = getattr(donee, attribute)
                if len(manager.all()) > 0:
                    added = getattr(donor, attribute).filter(pk__in=kwargs['pk_set'])
                    donee._add(attribute, *added)
        elif action=='pre_remove':
            # If the donee instance's related list is nonempty, remove any that the donor removed (empty ones will get
            # the change by deferring to the donor's list)
            for donee in donees:
                manager = getattr(donee, attribute)
                if len(manager.all()) > 0:
                    removed = manager.filter(pk__in=kwargs['pk_set'])
                    donee._remove(attribute, *removed)
        elif action=='pre_clear':
            # If the donee instance's related list is nonempty, remove all those of the donor (empty ones will get the
            # change by deferring to the donor's list)
            for donee in donees:
                manager = getattr(donee, attribute)
                if len(manager.all()) > 0:
                    donor_manager = getattr(donor, attribute)
                    removed = donor_manager.all()
                    donee._remove(attribute, *removed)
    return _items_changed


def through_item_added(attribute):
    def _through_item_added(sender, **kwargs):
        if kwargs['created']:
            through_item_changed(sender, attribute, 'add', **kwargs)
    return _through_item_added


def through_item_deleted(attribute):
    def _through_item_deleted(sender, **kwargs):
        through_item_changed(sender, attribute, 'deleted', **kwargs)
    return _through_item_deleted


def through_item_changed(sender, attribute, action, **kwargs):
    through_instance = kwargs['instance']
    donor = through_instance.config_entity
    donees = donor.children()
    for donee in donees:
        manager = getattr(donee, attribute)
        if len(manager.all()) > 0:
            # If the donee instance's related list is nonempty, add the through instance
            # The config_entity will be updated to that of the done
            if action == 'add':
                donee._add(attribute, through_instance)
            else:
                donee._remove(attribute, through_instance)

# TODO I'm suspicious of performance issues. So leaving these out until really needed.
# They will be needed as soon as we create new DbEntities at the project level, because
# the scenarios need to adopt them
# for attribute in ConfigEntity.INHERITABLE_COLLECTIONS:
#     through_class = getattr(ConfigEntity, attribute).through
#     # Listen to each through class for changes
#     if has_explicit_through_class(ConfigEntity, attribute):
#         # through_item_added won't actually do anything unless the item is new kwargs['created']==True
#         post_save.connect(through_item_added(attribute), sender=through_class, weak=False)
#         pre_delete.connect(through_item_deleted(attribute), sender=through_class, weak=False)
#     else:
#         m2m_changed.connect(items_changed(attribute), sender=through_class, weak=False)

