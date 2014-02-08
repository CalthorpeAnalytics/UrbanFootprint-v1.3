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
from django.db.models.signals import post_save, pre_delete, m2m_changed, pre_save
from django.dispatch import Signal
from footprint.models.config.config_entity import ConfigEntity
from footprint.utils.subclasses import receiver_subclasses
from footprint.utils.utils import has_explicit_through_class

__author__ = 'calthorpe'

# Defines custom Django Signals that are used by UrbanFootprint models instances to communicate
initialize_media = Signal(providing_args=[])
initialize_presentations = Signal(providing_args=[])
post_post_save_config_entity = Signal(providing_args=[])
post_analytic_run = Signal(providing_args=[])

def items_changed(attribute):
    def _items_changed(sender, **kwargs):
        """
            Listens for m2m singals on ConfigEntity instances. The instance alerts its children of the change so that
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


for attribute in ConfigEntity.INHERITABLE_COLLECTIONS:
    through_class = getattr(ConfigEntity, attribute).through
    # Listen to each through class for changes
    if has_explicit_through_class(ConfigEntity, attribute):
        post_save.connect(through_item_added(attribute), sender=through_class, weak=False)
        pre_delete.connect(through_item_deleted(attribute), sender=through_class, weak=False)
    else:
        m2m_changed.connect(items_changed(attribute), sender=through_class, weak=False)


# These signal handlers are here to ensure that it loads after all of ConfigEntity's subclasses
@receiver_subclasses(pre_save, ConfigEntity, "config_entity_pre_save")
def on_config_entity_pre_save(sender, **kwargs):
    """
        A presave event handler. Currently this just defaults the bounds of the instance to those of its parent
    :param sender:
    :param kwargs:
    :return:
    """
    instance = kwargs['instance']
    if not instance.pk:
        # Inherit the parent's bounds if none are defined
        if not instance.bounds:
            instance.bounds = instance.parent_config_entity.bounds


@receiver_subclasses(post_save, ConfigEntity, "config_entity_post_save")
def on_config_entity_post_save(sender, **kwargs):
    """
        Create the ConfigEntity's database schema on initial save
    :param sender:
    :param kwargs:
    :return:
    """
    config_entity = kwargs['instance']
    if kwargs['created']:
        config_entity.post_create()

    for child_config_entity in config_entity.children():
        child_config_entity.parent_config_entity_saved()

    # Send a message to publishers to configure after creation or update of the config_entity
    # This is executed through a Celery task so that it can run asynchronously
    from footprint.publishing.config_entity_creation import post_create_config_entity
    if not config_entity._no_post_post_save:
        post_create_config_entity(config_entity, **kwargs)


