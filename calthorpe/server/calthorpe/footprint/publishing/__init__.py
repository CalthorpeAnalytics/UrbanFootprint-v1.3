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
from footprint.models import LayerSelection, GlobalConfig

__author__ = 'calthorpe'

from django.db.models.signals import pre_delete, post_save
from footprint.models.signals import post_post_save_config_entity, post_analytic_run
from footprint.models.config.scenario import Scenario, FutureScenario, BaseScenario
from footprint.models.config.project import Project
from footprint.models.config.region import Region

# List the following imports because they have Django signal receivers that need to fire
from footprint.publishing import layer_publishing, analysis_module, result, data_import, built_form_publishing, tilestache

# For now we only publish built_forms for GlobalConfig. All other ConfigEntities will adopt from GlobalConfig
#post_post_save_config_entity.connect(built_form_publishing.on_config_entity_post_save_built_form, GlobalConfig, True, "built_form_on_config_entity_post_save")
#pre_delete.connect(built_form_publishing.on_config_entity_pre_delete_built_form, GlobalConfig, True, "built_form_on_config_entity_pre_delete")

# Register receivers for only the lineage classes of Scenario
for cls in [FutureScenario, BaseScenario, Project, Region]:
    post_post_save_config_entity.connect(data_import.on_config_entity_post_save_data_import, cls, True, "data_import_on_config_entity_post_save")
    pre_delete.connect(data_import.on_config_entity_pre_delete_data_import, cls, True, "data_import_on_config_entity_pre_delete")

    post_post_save_config_entity.connect(layer_publishing.on_config_entity_post_save_layer, cls, True, "layer_on_config_entity_post_save")
    pre_delete.connect(layer_publishing.on_config_entity_pre_delete_layer, cls, True, "layer_on_config_entity_pre_delete")

    post_post_save_config_entity.connect(tilestache.on_config_entity_post_save_tilestache, cls, True, "tilestache_on_config_entity_post_save")
    pre_delete.connect(tilestache.on_config_entity_pre_delete_tilestache, cls, True, "tilestache_on_config_entity_pre_delete")

    post_analytic_run.connect(layer_publishing.on_post_analytic_run, cls, True, "layer_on_post_analytic_result")


    post_post_save_config_entity.connect(result.on_config_entity_post_save_result, cls, True, "result_on_config_entity_post_save")
    pre_delete.connect(result.on_config_entity_pre_delete_results, cls, True, "result_on_config_entity_pre_delete")

    post_post_save_config_entity.connect(analysis_module.on_config_entity_post_save_analysis_modules, cls, True, "analysis_module_on_config_entity_post_save")
    pre_delete.connect(analysis_module.on_config_entity_pre_delete_analysis_modules, cls, True, "analysis_module_on_config_entity_pre_delete")

    # Just to set the default selected built_form_set
    post_post_save_config_entity.connect(built_form_publishing.on_config_entity_post_save_built_form, cls, True, "built_form_publishing_on_config_entity_post_save")

# Create all built_form_sets and built_forms data after the GlobalConfig is saved
post_post_save_config_entity.connect(built_form_publishing.on_config_entity_post_save_built_form, GlobalConfig, True, "built_form_publishing_on_config_entity_post_save")
