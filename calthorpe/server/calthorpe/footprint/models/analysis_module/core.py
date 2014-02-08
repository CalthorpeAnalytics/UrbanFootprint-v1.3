# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2012 Calthorpe Associates
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
from celery.task import task
from footprint.engines.models.core import run_core
from footprint.managers.geo_inheritance_manager import GeoInheritanceManager

from footprint.models.analysis_module.analysis_module import AnalysisModule
from footprint.models.analysis_module.celery_task import CeleryTask

from common.utils.websockets import send_message_to_client

__author__ = 'calthorpe'


class CoreTask(CeleryTask):
    def start(self, **kwargs):
        run_core(kwargs['config_entity'])


class Core(AnalysisModule):
    objects = GeoInheritanceManager()

    @property
    def task_class(self):
        return CoreTask

    class Meta(object):
        app_label = 'footprint'


# Temporary until we figure out CeleryTask
@task
def executeCore(user, config_entity):
    logger = executeCore.get_logger()
    logger.info("Executing Core using {0}".format(config_entity))
    run_core(config_entity)
    logger.info("Done executing Core")
    logger.info("Executed Core using {0}".format(config_entity))
    send_message_to_client(user.id,
                           dict(event='{0}_complete'.format(Core.__name__.lower()),
                                config_entity_id=config_entity.id)
    )


@task
def executePrimary(config_entity):
    logger = executePrimary.get_logger()
    logger.info("Executing Primary using {0}".format(config_entity))
    # TODO enable after setting this up to work with multiple clients
    # update_primary_parcels(config_entity)
    logger.info("Done executing Primary")
    logger.info("Executed Core using {0}".format(config_entity))

