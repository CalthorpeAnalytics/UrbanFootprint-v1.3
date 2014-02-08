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
from footprint.main.models.analysis_module.vmt_module.vmt import Vmt
from footprint.main.models.analysis_module.fiscal_module.fiscal import Fiscal
from footprint.main.models.analysis_module.core_module.core import Core
from footprint.main.models.config.scenario import FutureScenario

__author__ = 'calthorpe_associates'

logger = logging.getLogger(__name__)

def get_or_create_analysis_modules(config_entity):
    """
        Creates a results library and Result instances upon saving a config_entity if they do not yet exist.
    :param config_entity
    :return:
    """
    if isinstance(config_entity, FutureScenario):
        for analysis_module_class in [Core, Fiscal, Vmt]:
            analysis_module_class.objects.update_or_create(
                config_entity=config_entity
            )


def on_config_entity_post_save_analysis_modules(sender, **kwargs):
    """
        Sync a ConfigEntity's ResultPage presentation
    """
    config_entity = kwargs['instance']
    logger.debug("\t\tHandler: on_config_entity_post_save_analysis_module. ConfigEntity: %s" % config_entity.name)
    get_or_create_analysis_modules(config_entity)

def on_db_entity_save():
    """
    respond to whenever a db entity is added or updated
    :return:
    """

def on_config_entity_pre_delete_analysis_modules(sender, **kwargs):
    """
        Sync geoserver to a ConfigEntity class after the latter is saved
    """
    pass


