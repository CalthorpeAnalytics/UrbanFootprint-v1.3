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
#from memory_profiler import profile
from footprint.main.models.config.policy_set import PolicySet
from footprint.main.models.config.global_config import GlobalConfig
from footprint.main.models.config.policy import Policy
from footprint.main.models.config.scenario import Scenario

__author__ = 'calthorpe_associates'

def update_or_create_policy_sets(config_entity, **kwargs):
    """
        Creates a ResultLibrary and its Result instances upon saving a config_entity if they do not yet exist.
    :param config_entity
    :param kwargs
    :return:
    """

    # Create top-level policy if needed. TODO move to initializer
    global_policy = Policy.objects.update_or_create(
        key='global',
        schema=None,
        defaults=dict(
            name='Global',
            description='The parent policy of all',
            values={}
        ))[0]

    if isinstance(config_entity, GlobalConfig):

        from footprint.client.configuration.utils import resolve_fixture
        from footprint.client.configuration.fixture import PolicyConfigurationFixture
        client_policy = resolve_fixture(
            "policy",
            "policy",
            PolicyConfigurationFixture,
            config_entity.schema(),
            config_entity=config_entity)

        # Create each policy set and store them as a dict keyed by their key
        for policy_set_config in client_policy.policy_sets():
            policy_set = PolicySet.objects.update_or_create(
                key=policy_set_config['key'],
                defaults=dict(
                    name=policy_set_config['name'],
                    description=policy_set_config.get('description', None)
                )
            )[0]
            print 'this is a test change'
            policies = map(lambda policy_config: global_policy.update_or_create_policy(policy_config), policy_set_config.get('policies', []))
            policy_set.policies.add(*policies)
            config_entity.add_policy_sets(policy_set)


    elif isinstance(config_entity, Scenario): # and kwargs.get('created', None):
        # TODO for now just the first policy_set to the selected one
        config_entity.select_policy_set(config_entity.computed_policy_sets()[0])
        previous = config_entity._no_post_save_publishing
        config_entity._no_post_save_publishing = True
        config_entity.save()
        config_entity._no_post_save_publishing = previous


#@profile
def on_config_entity_post_save_policy(sender, **kwargs):
    """
        Sync a ConfigEntity's ResultPage presentation
    """
    config_entity = kwargs['instance']

    update_or_create_policy_sets(config_entity, **kwargs)

def on_db_entity_save():
    """
    respond to whenever a db entity is added or updated
    :return:
    """
    pass

def on_layer_style_save():
    """
    respond to any changes in style (
    :return:
    """
    pass

#@profile
def on_config_entity_post_save(sender, **kwargs):
    """
        Sync tilestache to a ConfigEntity class after the latter is saved
    """
    config_entity = kwargs['instance']


def on_config_entity_pre_delete_results(sender, **kwargs):
    """
        Sync geoserver to a ConfigEntity class after the latter is saved
    """
    config_entity = kwargs['instance']


