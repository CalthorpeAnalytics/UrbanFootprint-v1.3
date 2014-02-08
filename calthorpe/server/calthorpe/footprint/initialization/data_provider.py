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

from django.contrib.auth.models import User, Permission
from tastypie.models import ApiKey
from footprint.initialization.fixture import BuiltFormFixture, ConfigEntitiesFixture, PolicyFixture
from footprint.initialization.utils import resolve_fixture, resolve_default_fixture
from footprint.lib.functions import remove_keys, get_single_value_or_create, merge, deep_map_dict_structure, map_property, flatten, map_dict, flat_map_dict, flatten_values, flat_map
from footprint.models import Medium, BuiltForm
from footprint.models.category import Category
from footprint.models.config.project import Project
from footprint.models.config.region import Region
from footprint.models.config.policy_set import PolicySet
from footprint.models.config.global_config import global_config_singleton
from footprint.models.config.policy import Policy
from settings import USE_SAMPLE_DATA_SETS

import settings

__author__ = 'calthorpe'

config_entities_fixture = resolve_fixture("config_entity", "config_entities", ConfigEntitiesFixture, settings.CLIENT)
built_form_fixture = resolve_fixture("built_form", "built_form", BuiltFormFixture, settings.CLIENT)
policy_fixture = resolve_fixture("policy", "policy", PolicyFixture, settings.CLIENT)

import logging

logger = logging.getLogger(__name__)


class SQLImportError(Exception):
    def __init__(self, value):
        super(SQLImportError, self).__init__(value)


class DataProvider(object):
    """
        This class loads test data from sources in the test_data directory.
        All persistence is performed here, and instances of persisted classes are returned to the
        caller.
    """

    def user(self):
        """
        Create a user.
        :return:
        """
        username = 'test'
        password = 'test'
        email = 'testy@test.ta'

        def create():
            user = User.objects.create_user(username, email, password)
            # Make sure the user has permission to update everything for testing purposes
            user.user_permissions.add(*list(Permission.objects.all()))
            return user
            # An api key is created upon creating a user

        user = get_single_value_or_create(User.objects.filter(username=username), create)
        try:
            api_key = ApiKey.objects.get_or_create(user=user, key='TEST_API_KEY')[0].key
        except:
            # Something is creating the api_key prematurely
            api_key = ApiKey.objects.get(user=user)
            api_key.key = 'TEST_API_KEY'
            api_key.save()
        return {'user': user, 'api_key': api_key}


    def scenarios(self, scenario_fixtures=None, project_fixtures=config_entities_fixture.projects()):
        """
            Initializes scenarios using fixture data. The fixture data is expected in the form
            dict(BaseScenario=[dict(),...], FutureScenario=[dict()....]) where the dicts in the former are used
            to create BaseScenario instances and those in the latter to create FutureScenario instances.
        :param scenario_fixtures:
        :return:
        """
        projects = self.projects(project_fixtures)

        # Get the scenario fixtures for each Project instance and build the Scenario instances.
        # Flatten the results and return them
        # scenario_fixtures may be a function that accepts the current project in order to filter the fixtures
        return flat_map(
            lambda project: self.scenarios_per_project(
                project,
                scenario_fixtures or
                # Resolve as the scenarios as specific to the project scope as available
                resolve_fixture("config_entity",
                                "config_entities",
                                ConfigEntitiesFixture,
                                project.schema()).scenarios(project)),
            projects
        )

    def scenarios_per_project(self, project, scenario_fixtures):
        # Create the Scenarios from the fixtures
        # The fixtures are dict keyed by the Scenario subclass (BaseScenario and FutureScenario) with a list of
        # Scenario fixtures for each
        scenarios_created_updated = map(
            lambda scenario_fixture:
            scenario_fixture['class_scope'].objects.update_or_create(
                key=scenario_fixture['key'],
                defaults=merge(remove_keys(scenario_fixture,
                                           ['class_scope', 'key', 'project_key', 'categories', 'selections', 'year']), {
                                   'parent_config_entity': project,
                                   'year': scenario_fixture.get('year', project.base_year)
                               })),
            scenario_fixtures)

        # Apply the categories, and other simple many-to-many attributes as needed
        for i, scenario_dict in enumerate(scenario_fixtures):
            for category in scenario_dict['categories']:
                category, created, updated = Category.objects.update_or_create(key=category.key, value=category.value)
                scenario = scenarios_created_updated[i][0]
                scenario.add_categories(category)

        for index, scenario_created_updated in enumerate(scenarios_created_updated):
            # Select a policy set and built_form_set for each scenario
            # If configured in the fixtures 'selections' dict, use the configured key
            scenario, created, updated = scenario_created_updated
            if created:
                selections = scenario_fixtures[index].get('selections', {})
                try:
                    scenario.select_policy_set(
                        scenario.computed_policy_sets(key=selections['policy_sets'])[0] if
                        selections.get('policy_sets', None) else
                        scenario.computed_policy_sets()[0]
                    )
                except Exception:
                    raise Exception(
                        "Bad policy_set configuration for scenario: {0}. Selected PolicySet key: {1}, All PolicySets".format(
                            scenario, selections.get('policy_sets', None), scenario.computed_policy_sets()
                        ))

                scenario.save()

        return map(lambda scenario_created_updated: scenario_created_updated[0], scenarios_created_updated)

    def projects(self, project_fixtures=config_entities_fixture.projects(), region_fixtures=config_entities_fixture.regions()):
        """
        Create test projects according to the samples
        :param project_fixtures:
        :return:
        """

        def update_or_create_project(project_dict):
            project_tuple = Project.objects.update_or_create(
                key=project_dict['key'],
                defaults=merge(remove_keys(project_dict, ['key', 'base_table', 'region_index', 'media']), {
                    'parent_config_entity': self.regions(region_fixtures)[project_dict['region_index']]
                }))

            media = map(lambda medium_config:
                        Medium.objects.update_or_create(
                            key=medium_config.key,
                            defaults=remove_keys(medium_config.__dict__['kwargs'], 'key'))[0],
                        project_dict.get('media', []))

            existing_media = project_tuple[0].media.filter(id__in=map(lambda medium: medium.id, media))
            media_to_add = set(media) - set(existing_media)
            if len(media_to_add) > 0:
                project_tuple[0].media.add(*media_to_add)
            return project_tuple

        projects_created_updated = map(
            lambda project_dict: update_or_create_project(project_dict),
            project_fixtures)

        for project, created, updated in projects_created_updated:

            if created:
                # Fire signals
                project.save()
        return map(lambda project_created_updated: project_created_updated[0], projects_created_updated)

    def regions(self, region_fixtures=config_entities_fixture.regions()):
        """
        Create test regions according to the sample
        :return:
        """

        def update_or_create_region(region_dict):
            region_tuple = Region.objects.update_or_create(
                key=region_dict['key'],
                defaults=merge(remove_keys(region_dict, ['key', 'media']), {
                    'parent_config_entity': global_config_singleton()
                }))

            media = map(lambda medium_config:
                        Medium.objects.update_or_create(
                            key=medium_config.key,
                            defaults=remove_keys(medium_config.__dict__['kwargs'], 'key'))[0],
                        region_dict.get('media', []))

            existing_media = region_tuple[0].media.filter(id__in=map(lambda medium: medium.id, media))
            media_to_add = set(media) - set(existing_media)
            if len(media_to_add) > 0:
                region_tuple[0].media.add(*media_to_add)
            return region_tuple

        regions_tuple = map(
            lambda region_dict: update_or_create_region(region_dict),
            region_fixtures)

        for region, created, updated in regions_tuple:
            if created:
                # Fire signals
                region.save()

        return map(lambda region_tuple: region_tuple[0], regions_tuple)

    def import_table_name(self, config_entity, db_entity):
        if USE_SAMPLE_DATA_SETS:
            return "{0}_{1}_{2}".format(config_entity.key, db_entity.table, 'sample')
        else:
            return "{0}_{1}".format(config_entity.key, db_entity.table)



    def policy_sets(self):
        def _update_or_create_policy(policy_dict):
            # Remove th:reub-policies, which have to be appended after
            filtered_policy_dict = remove_keys(policy_dict, ['policies', 'key'])
            policy, created, updated = Policy.objects.update_or_create(key=policy_dict['key'],
                                                                       defaults=filtered_policy_dict)
            if not created:
                for key, value in filtered_policy_dict.items():
                    setattr(policy, key, value)
                policy.save()

            # Sub policies will already by converted to Policy instances and saved
            # Add sub policies that haven't been added before
            # TODO update policy instances whose fixture data have changed
            existing_sub_policies = policy.policies.all()
            for sub_policy in filter(lambda sub_policy: not sub_policy in existing_sub_policies,
                                     policy_dict.get('policies', [])):
                policy.policies.add(sub_policy)
            return policy

        policy_set_dicts = map(
            lambda policy_set_dict: dict(
                policy_set=PolicySet.objects.update_or_create(
                    key=policy_set_dict['key'],
                    defaults=dict(name=policy_set_dict['name'], description=policy_set_dict['description']))[0],
                policies=deep_map_dict_structure(policy_set_dict['policies'],
                                                 # Turn sample data dicts into Policy instances
                                                 {dict: lambda value: _update_or_create_policy(value)}
                )),
            policy_fixture.policy_sets())
        for policy_set_dict in policy_set_dicts:
            policy_set = policy_set_dict['policy_set']
            policy_set.policies.add(*(set(policy_set_dict['policies']) - set(policy_set.policies.all())))

        return map_property(policy_set_dicts, 'policy_set')

