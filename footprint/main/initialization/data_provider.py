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
from nose.config import user_config_files
from tastypie.models import ApiKey
from footprint.client.configuration.fixture import BuiltFormFixture, ConfigEntitiesFixture, PolicyConfigurationFixture, InitFixture
from footprint.client.configuration.utils import resolve_fixture
from footprint.main.lib.functions import remove_keys, get_single_value_or_create, merge, flat_map
from footprint.main.models import Medium
from footprint.main.models.category import Category
from footprint.main.models.config.project import Project
from footprint.main.models.config.region import Region
from footprint.main.models.config.global_config import global_config_singleton

from django.conf import settings

__author__ = 'calthorpe_associates'

config_entities_fixture = resolve_fixture("config_entity", "config_entities", ConfigEntitiesFixture, settings.CLIENT)
policy_fixture = resolve_fixture("policy", "policy", PolicyConfigurationFixture, settings.CLIENT)
init_fixture = resolve_fixture(None, "init", InitFixture, settings.CLIENT)

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

    def users(self):
        for user_configuration in init_fixture.users:
            self.user(**user_configuration)

    def user(self, username='test', password='test', email='testy@test.ca', api_key='TEST_API_KEY'):
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
        api_key_instance = ApiKey.objects.get_or_create(user=user)[0]
        if api_key_instance.key != api_key:
            api_key_instance.key = api_key
            api_key_instance.save()
        return {'user': user, 'api_key': api_key_instance}


    def scenarios(self, scenario_fixtures=None, project_fixtures=config_entities_fixture.projects(), **kwargs):
        """
            Initializes scenarios using fixture data. The fixture data is expected in the form
            dict(BaseScenario=[dict(),...], FutureScenario=[dict()....]) where the dicts in the former are used
            to create BaseScenario instances and those in the latter to create FutureScenario instances.
            Use kwargs to limit class processing to one model class with e.g. class=FutureScenario
        :param scenario_fixtures:
        :return:
        """
        projects = self.projects(project_fixtures, **kwargs)

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
                                project.schema()).scenarios(project), **kwargs),
            projects
        )

    def scenarios_per_project(self, project, scenario_fixtures, **kwargs):
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
            # If kwargs['limit_to_classes'] is specified, only do Scenario subclasses that match it, if any
            filter(lambda scenario_fixture:
                   scenario_fixture['class_scope'] in kwargs.get('limit_to_classes', [scenario_fixture['class_scope']])
                   or [scenario_fixture['class_scope']],
                   scenario_fixtures))

        for scenario_tuple in scenarios_created_updated:
            logger.info("{update_or_create} Scenario {config_entity}".format(update_or_create='Created' if scenario_tuple[1] else 'Updated', config_entity=scenario_tuple[0]))

        # Apply the categories, and other simple many-to-many attributes as needed
        for i, scenario_dict in enumerate(scenario_fixtures):
            for category in scenario_dict.get('categories', []):
                category, created, updated = Category.objects.update_or_create(key=category.key, value=category.value)
                scenario = scenarios_created_updated[i][0]
                scenario.add_categories(category)
                scenario.save()

        return map(lambda scenario_created_updated: scenario_created_updated[0], scenarios_created_updated)

    def projects(self, project_fixtures=config_entities_fixture.projects(), region_fixtures=config_entities_fixture.regions(), **kwargs):
        """
        Create test projects according to the samples
        :param project_fixtures:
        :return:
        """

        def update_or_create_project(project_dict):
            project_tuple = Project.objects.update_or_create(
                key=project_dict['key'],
                defaults=merge(remove_keys(project_dict, ['key', 'base_table', 'region_index', 'media']), {
                    'parent_config_entity': self.regions(region_fixtures, **kwargs)[project_dict['region_index']]
                })) if Project in kwargs.get('limit_to_classes', [Project]) or [Project] else (Project.objects.get(key=project_dict['key']), False, False)
            logger.info("{update_or_create} Project {config_entity}".format(update_or_create='Created' if project_tuple[1] else 'Updated', config_entity=project_tuple[0]))

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

    def regions(self, region_fixtures=config_entities_fixture.regions(), **kwargs):
        """
        Create test regions according to the sample
        :return:
        """

        def update_or_create_region(region_dict):
            region_tuple = Region.objects.update_or_create(
                key=region_dict['key'],
                defaults=merge(remove_keys(region_dict, ['key', 'media']), {
                    'parent_config_entity': global_config_singleton()
                })) if Region in kwargs.get('limit_to_classes', [Region]) or [Region] else (Region.objects.get(key=region_dict['key']), False, False)

            logger.info("{update_or_create} Region {config_entity}".format(update_or_create='Created' if region_tuple[1] else 'Updated', config_entity=region_tuple[0]))

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

    def import_table_name(self, db_entity):
        """
            Returns the full db_entity table name (schema+table) and optionally adds the suffix
            _sample if a sample-size table shall be used for importing
        :param db_entity:
        :return:
        """
        full_table_name = db_entity.full_table_name
        return "{0}_{1}".format(full_table_name, 'sample') if settings.USE_SAMPLE_DATA_SETS else full_table_name


