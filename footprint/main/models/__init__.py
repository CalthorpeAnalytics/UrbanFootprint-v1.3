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
# from constants import Constants

from south.modelsinspector import add_introspection_rules
add_introspection_rules([],  [r"^footprint.main.models.config.model_pickled_object_field.ModelPickledObjectField",
                              r"^footprint.main.models.config.model_pickled_object_field.SelectionModelsPickledObjectField"])

from footprint.main.models.config.model_pickled_object_field import ModelPickledObjectField
from footprint.main.models.config.model_pickled_object_field import SelectionModelsPickledObjectField

import geospatial
from footprint.main.models.future.core_end_state_feature import CoreEndStateFeature
from footprint.main.models.future.core_end_state_demographic_feature import CoreEndStateDemographicFeature
from footprint.main.models.future.core_increment_feature import CoreIncrementFeature
from footprint.main.models.analysis.fiscal_feature import FiscalFeature

from footprint.main.models.analysis.vmt_features.vmt_feature import VmtFeature
from footprint.main.models.analysis.vmt_features.vmt_quarter_mile_buffer_feature import VmtQuarterMileBufferFeature
from footprint.main.models.analysis.vmt_features.vmt_one_mile_buffer_feature import VmtOneMileBufferFeature
from footprint.main.models.analysis.vmt_features.vmt_variable_buffer_feature import VmtVariableBufferFeature
from footprint.main.models.analysis.vmt_features.vmt_feature import VmtFeature
from footprint.main.models.analysis.vmt_features.vmt_trip_lengths_feature import VmtTripLengthsFeature

from footprint.main.models.database.information_schema import PGNamespace

# These import statements are compulsory. Models will not be recognized without them
# There are some tricks published online to import all classes dynamically, but doing so in
# practice has yet been unsuccessful
from footprint.main.models.built_form.built_form import BuiltForm
from footprint.main.models.geospatial.db_entity import DbEntity
from footprint.main.models.config.config_entity import ConfigEntity
from footprint.main.models.analysis.energy_water_feature import EnergyWaterFeature
from footprint.main.models.tasks.async_job import Job

from footprint.main.models.base.base_feature import BaseFeature
from footprint.main.models.base.developable_feature import DevelopableFeature
from footprint.main.models.presentation.layer import Layer
from footprint.main.models.future.future_scenario_feature import FutureScenarioFeature
from footprint.main.models.built_form.flat_built_forms import FlatBuiltForm
from footprint.main.models.base.census_blockgroup import CensusBlockgroup
from footprint.main.models.base.census_block import CensusBlock
from footprint.main.models.base.census_tract import CensusTract

from footprint.main.models.analysis_module.analysis_module import AnalysisModule
from footprint.main.models.analysis_module.celery_task import CeleryTask
from footprint.main.models.analysis_module.core_module.core import Core
from footprint.main.models.analysis_module.fiscal_module.fiscal import Fiscal
from footprint.main.models.analysis_module.vmt_module.vmt import Vmt

from footprint.main.models.built_form.building_attribute_set import BuildingAttributeSet
from footprint.main.models.built_form.building_use_definition import BuildingUseDefinition
from footprint.main.models.built_form.building_use_percent import BuildingUsePercent
from footprint.main.models.built_form.primary_component import PrimaryComponent
from footprint.main.models.built_form.primary_component_percent import PrimaryComponentPercent
from footprint.main.models.built_form.placetype_component import PlacetypeComponent
from footprint.main.models.built_form.placetype_component_percent import PlacetypeComponentPercent
from footprint.main.models.built_form.placetype import Placetype

from footprint.main.models.config.db_entity_interest import DbEntityInterest

from footprint.main.models.config.global_config import GlobalConfig
from footprint.main.models.config.interest import Interest
from footprint.main.models.config.policy_set import PolicySet
from footprint.main.models.config.region import Region
from footprint.main.models.config.project import Project
from footprint.main.models.config.scenario import Scenario
from footprint.main.models.base.base_feature import BaseFeature
from footprint.main.models.base.base_demographic_feature import BaseDemographicFeature
from footprint.main.models.base.cpad_holdings_feature import CpadHoldingsFeature
from footprint.main.models.geographies.geography import Geography
from footprint.main.models.geographies.parcel import Parcel
from footprint.main.models.geographies.grid_cell import GridCell
from footprint.main.models.geographies.taz import Taz
from footprint.main.models.presentation.chart import Chart
from footprint.main.models.presentation.geo_library import GeoLibrary
from footprint.main.models.presentation.geo_library_catalog import GeoLibraryCatalog
from footprint.main.models.presentation.grid import Grid
from footprint.main.models.presentation.layer_chart import LayerChart
from footprint.main.models.presentation.layer_library import LayerLibrary
from footprint.main.models.presentation.map import Map
from footprint.main.models.presentation.medium import Medium
from footprint.main.models.presentation.painting import Painting
from footprint.main.models.presentation.presentation import Presentation
from footprint.main.models.presentation.presentation_medium import PresentationMedium
from footprint.main.models.presentation.report import Report
from footprint.main.models.presentation.result import Result
from footprint.main.models.presentation.result_library import ResultLibrary
from footprint.main.models.presentation.style import Style
from footprint.main.models.presentation.template import Template
from footprint.main.models.presentation.presentation_configuration import PresentationConfiguration
from footprint.main.models.sort_type import SortType
from footprint.main.models.presentation.layer_selection import LayerSelection
from footprint.main.models.presentation.tilestache_config import TileStacheConfig

