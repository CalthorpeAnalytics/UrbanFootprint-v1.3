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
import logging
from django.contrib.gis.geos import MultiPolygon, Polygon
from django.conf import settings
from footprint.main.initialization.data_provider import DataProvider
from footprint.client.configuration.fixture import ConfigEntitiesFixture, InitFixture
from footprint.client.configuration.utils import resolve_fixture
from footprint.main.models import Project
from footprint.main.models.built_form.placetype_component import PlacetypeComponentCategory
from footprint.main.models.keys.keys import Keys
from footprint.main.models.sort_type import SortType
import footprint.main.models as models

from footprint.main.models.signals import initialize_media, initialize_presentations
from footprint.main.models.config.global_config import GlobalConfig
from footprint.main.models.config.interest import Interest
from footprint.main.models.built_form.building_use_definition import BuildingUseDefinition

from footprint.main.models.database.information_schema import SouthMigrationHistory
from footprint.main.publishing.config_entity_publishing import post_save_config_entity_initial

# TODO Move this to publishers/application_publishing.py

__author__ = 'calthorpe_associates'
logger = logging.getLogger(__name__)


def application_initialization(**kwargs):
    """
        Initialize or sync the application
        :param kwargs: 'limit_to_classes' as an array of ConfigEntity classes to limit processing to those
    """

    # Initialize lookup table data
    if SouthMigrationHistory.objects.filter(app_name='main').exists():
        initialize_table_definitions()
        initialize_client_data()

        # Sync the DBEntities to tables in the global schema
        initialize_global_config(**kwargs)

        # Send a message telling Publishers to save their default media
        initialize_default_media()
        initialize_presentations.send(sender=models)
        create_data_provider_data(**kwargs)


def minimum_initialization(**kwargs):
    """
        A minimum initialization for unit tests
        :param kwargs: 'limit_to_classes' as an array of ConfigEntity classes to limit processing to those
    :return:
    """
    if SouthMigrationHistory.objects.filter(app_name='main').exists():
        # Disable built_forms
        from footprint.main.publishing import built_form_publishing
        post_save_config_entity_initial.disconnect(
            built_form_publishing.on_config_entity_post_save_built_form,
            GlobalConfig,
            True,
            "built_form_publishing_on_config_entity_post_save")

        initialize_table_definitions()
        # Sync the DBEntities to tables in the global schema
        initialize_global_config(**kwargs)
        # Send a message telling Publishers to save their default media
        initialize_default_media()
        initialize_presentations.send(sender=models)

        # Get access to the ConfigEntity fixtures for the configured client
        # For now we just try our soul client as the fixture schema, the client string is equivalent to Region schema
        config_entities_fixture = resolve_fixture(
            "config_entity",
            "config_entities",
            ConfigEntitiesFixture,
            settings.CLIENT)

        # For speed, just set up the first project
        project_fixture = config_entities_fixture.projects()[0]
        project = DataProvider().projects(project_fixtures=[project_fixture])[0]
        # For speed, just set up the first scenario
        scenario_fixture = config_entities_fixture.scenarios(project=project)[0]
        DataProvider().scenarios([scenario_fixture], [project_fixture])
        # Create the test user
        DataProvider().user()
        create_data_provider_data()


def initialize_client_data():
    # Initialize client-specific models
    logger.info("importing client fixtures for {client}".format(client=settings.CLIENT))
    print("importing client fixtures for {client}".format(client=settings.CLIENT))
    client_init = resolve_fixture(None, "init", InitFixture, settings.CLIENT)
    print("using fixture:" + str(client_init))
    client_init.populate_models()


def create_data_provider_data(**kwargs):
    # Creating the precooked scenarios will cause everything else to be created.
    DataProvider().scenarios(**kwargs)
    recalculate_project_bounds()


def recalculate_project_bounds():
    for project in Project.objects.all():
        project.recalculate_bounds()


def initialize_table_definitions():
    """
        Initialize any definition tables with constant values
    """
    Interest.objects.update_or_create(key=Keys.INTEREST_OWNER)
    Interest.objects.update_or_create(key=Keys.INTEREST_DEPENDENT)
    Interest.objects.update_or_create(key=Keys.INTEREST_FOLLOWER)

    for building_use_subcategory, building_use in Keys.BUILDING_USE_DEFINITION_CATEGORIES.items():
        BuildingUseDefinition.objects.update_or_create(name=building_use_subcategory)
        BuildingUseDefinition.objects.update_or_create(name=building_use)

    for component in Keys.COMPONENT_CATEGORIES:
        PlacetypeComponentCategory.objects.update_or_create(
            name=component,
            contributes_to_net=True if component in Keys.NET_COMPONENTS else False
        )

    # Ways to sort PresentationMedia QuerySets
    SortType.objects.update_or_create(
        key=Keys.SORT_TYPE_PRESENTATION_MEDIA_DB_ENTITY_KEY,
        defaults={'order_by': 'db_entity_key'})
    SortType.objects.update_or_create(
        key=Keys.SORT_TYPE_PRESENTATION_MEDIA_MEDIUM_KEY,
        defaults={'order_by': 'medium__key'})
    SortType.objects.update_or_create(
        key=Keys.SORT_TYPE_PRESENTATION_MEDIA_MEDIUM_NAME,
        defaults={'order_by': 'medium__name'})
    # Ways to sort Key-ed QuerySets
    SortType.objects.update_or_create(
        key=Keys.SORT_TYPE_KEY,
        defaults={'order_by': 'key'})
    SortType.objects.update_or_create(
        key=Keys.SORT_TYPE_NAME,
        defaults={'order_by': 'name'})


def initialize_global_config(**kwargs):
    global_bounds = MultiPolygon(
        [Polygon((
            (settings.DEFAULT_SRID_BOUNDS[1], settings.DEFAULT_SRID_BOUNDS[1]),  # bottom left
            (settings.DEFAULT_SRID_BOUNDS[0], settings.DEFAULT_SRID_BOUNDS[3]),  # top left
            (settings.DEFAULT_SRID_BOUNDS[2], settings.DEFAULT_SRID_BOUNDS[3]),  # top right
            (settings.DEFAULT_SRID_BOUNDS[2], settings.DEFAULT_SRID_BOUNDS[1]),  # bottom right
            (settings.DEFAULT_SRID_BOUNDS[1], settings.DEFAULT_SRID_BOUNDS[1]),  # bottom left
        ))],
        srid=settings.DEFAULT_SRID
    )

    # Consume default data hardcoded in the system, either from the defaults.data or tests.data package
    data_provider = DataProvider()

    data_provider.user()

    limit_to_classes = kwargs.get('limit_to_classes', [GlobalConfig]) \
        if kwargs.get('limit_to_classes', [GlobalConfig]) else [GlobalConfig]
    # Create and persist the singleton GlobalConfig
    global_config, created, updated = GlobalConfig.objects.update_or_create(
        key=Keys.GLOBAL_CONFIG_KEY,
        defaults={'name': Keys.GLOBAL_CONFIG_NAME, 'bounds': global_bounds}
    ) if GlobalConfig in limit_to_classes else (GlobalConfig.objects.get(), False, False)

    return global_config


def initialize_default_media():
    """
        Initialize default media that is used by presentations in the absence of custom values
    """
    # Send a signal to publishers
    initialize_media.send(sender=models)


