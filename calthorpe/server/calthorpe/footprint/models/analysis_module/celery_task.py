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
from datetime import datetime
import logging
from celery import Task
from footprint.models.config.config_entity import ConfigEntity

__author__ = 'calthorpe'

logger = logging.getLogger(__name__)

class CeleryTask(Task):

    def resolve_analyis_module(self, **kwargs):
        analysis_module_id = kwargs['analysis_module_id']
        analysis_module_class = kwargs['analysis_module_class']
        return analysis_module_class.objects.get(analysis_module_id)

    def on_success(self, retval, task_id, args, kwargs):
        analysis_module = self.resolve_analyis_module(**kwargs)
        analysis_module.completed = datetime.utcnow()
        analysis_module.save()
        logger.info("Done executing task %s for ConfigEntity: %s".format(analysis_module, analysis_module.config_entity))

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        analysis_module = self.resolve_analyis_module(**kwargs)
        analysis_module.failed = datetime.utcnow()
        analysis_module.save()
        logger.info("Failed executing task %s for ConfigEntity: %s".format(analysis_module, analysis_module.config_entity))

    def run(self, *args, **kwargs):
        """
        Run by when apply_async is called or a similar starter. Fetches the anlysis_module and config_entity and
        calls start with those arguments
        :param args:
        :param kwargs:
        :return:
        """
        analysis_module = self.resolve_analyis_module(**kwargs)
        config_entity = ConfigEntity.objects.get(analysis_module.config_entity.id).select_subclasses()
        logger.info("Executing task %s for ConfigEntity: %s".format(analysis_module, analysis_module.config_entity))
        analysis_module.started = datetime.utcnow()
        analysis_module.save()
        task = self()
        analysis_module.celery_task = task
        self.start(analysis_module=analysis_module, config_entity=config_entity)

    def start(self, **kwargs):
        pass
