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
from footprint.initialization.fixture import ConfigEntityFixture, InitFixture
from footprint.initialization.utils import resolve_fixture, resolve_client_module

from footprint.models.constants import Constants
from footprint.models.future.core_end_state_feature import CoreEndStateFeature
from footprint.models.future.core_increment_feature import CoreIncrementFeature
import geospatial
from footprint.models.database.information_schema import PGNamespace

# These import statements are compulsory. Models will not be recognized without them
# There are some tricks published online to import all classes dynamically, but doing so in
# practice has yet been unsuccessful
from footprint.models.built_form.built_form import BuiltForm
from footprint.models.geospatial.db_entity import DbEntity
from footprint.models.config.config_entity import ConfigEntity
from footprint.models.analysis.energy_water_feature import EnergyWaterFeature

from footprint.models.tasks.async_job import Job

from footprint.models.analysis.vmt_config import VMTConfig
from footprint.models.base.base_feature import BaseFeature
from footprint.models.base.developable_feature import DevelopableFeature
from footprint.models.presentation.layer import Layer
from footprint.models.future.future_scenario_feature import FutureScenarioFeature
from footprint.models.built_form.flat_built_forms import FlatBuiltForm
from footprint.models.base.census_blockgroup import CensusBlockgroup
from footprint.models.base.census_block import CensusBlock
from footprint.models.base.census_tract import CensusTract

from footprint.models.analysis_module.analysis_module import AnalysisModule
from footprint.models.analysis_module.celery_task import CeleryTask
from footprint.models.analysis_module.core import Core

# from footprint.models.built_form.building import Building
# from footprint.models.built_form.building_percent import BuildingPercent
# from footprint.models.built_form.buildingtype import BuildingType
# from footprint.models.built_form.infrastructure import Infrastructure
# from footprint.models.built_form.infrastructure_type import InfrastructureType
# from footprint.models.built_form.infrastructure_percent import InfrastructurePercent

from footprint.models.built_form.building_attribute_set import BuildingAttributeSet
from footprint.models.built_form.building_use_definition import BuildingUseDefinition
from footprint.models.built_form.building_use_percent import BuildingUsePercent
from footprint.models.built_form.primary_component import PrimaryComponent
from footprint.models.built_form.primary_component_percent import PrimaryComponentPercent
from footprint.models.built_form.placetype_component import PlacetypeComponent
from footprint.models.built_form.placetype_component_percent import PlacetypeComponentPercent
from footprint.models.built_form.placetype import Placetype

from footprint.models.config.db_entity_interest import DbEntityInterest
from footprint.models.config.engine_plugin import EnginePlugin
from footprint.models.config.global_config import GlobalConfig
from footprint.models.config.interest import Interest
from footprint.models.config.policy_set import PolicySet
from footprint.models.config.region import Region
from footprint.models.config.project import Project
from footprint.models.config.scenario import Scenario
from footprint.models.base.base_feature import BaseFeature
from footprint.models.geographies.geography import Geography
from footprint.models.geographies.parcel import Parcel
from footprint.models.geographies.grid_cell import GridCell
from footprint.models.geographies.taz import Taz
from footprint.models.geospatial.geojson_feature import GeoJsonFeature
from footprint.models.presentation.chart import Chart
from footprint.models.presentation.geo_library import GeoLibrary
from footprint.models.presentation.geo_library_catalog import GeoLibraryCatalog
from footprint.models.presentation.grid import Grid
from footprint.models.presentation.layer_chart import LayerChart
from footprint.models.presentation.layer_library import LayerLibrary
from footprint.models.presentation.map import Map
from footprint.models.presentation.medium import Medium
from footprint.models.presentation.painting import Painting
from footprint.models.presentation.presentation import Presentation
from footprint.models.presentation.presentation_medium import PresentationMedium
from footprint.models.presentation.report import Report
from footprint.models.presentation.result import Result
from footprint.models.presentation.result_library import ResultLibrary
from footprint.models.presentation.style import Style
from footprint.models.presentation.template import Template
from footprint.models.presentation.presentation_configuration import PresentationConfiguration
from footprint.models.sort_type import SortType
from footprint.models.presentation.layer_selection import LayerSelection
from footprint.models.presentation.tilestache_config import TileStacheConfig

# Import all client models that have static tables so that we have a single migration path
import settings

# Load all client modules into the system, even though we only will configure one CLIENT
# This forces South to create all client specific table definitions
for client in settings.ALL_CLIENTS:
    client_init = resolve_fixture(None, "init", InitFixture, client)
    #client_init.import_database()
    for module_tuple in client_init.model_class_modules():
        # Load the module so that Django and South find the classes
        resolve_client_module(module_tuple[0], module_tuple[1], client)

# Initialize publishing signal receivers
import footprint.initialization.publishing
