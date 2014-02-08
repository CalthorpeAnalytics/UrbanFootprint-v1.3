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
from django.db import models
from django.db.models import DateField
from picklefield import PickledObjectField
from footprint.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.models.config.config_entity import ConfigEntity

__author__ = 'calthorpe'

class AnalysisModule(models.Model):

    config_entity = models.ForeignKey(ConfigEntity, null=False)
    # Stores the last celery_task
    celery_task = PickledObjectField(null=True)
    previous_celery_task = PickledObjectField(null=True)
    started = DateField(null=True)
    completed = DateField(null=True)
    failed = DateField(null=True)

    @property
    def task_class(self):
        return None

    def start(self):
        """
            Runs the module in celery
        :return:
        """
        self.previous_celery_task = self.celery_task
        self.celery_task = self.task_class()
        # Call run
        self.celery_task.apply_async(kwargs=dict(
            analysis_module_id=self.id,
            analysis_moudel_class=self.__class__))

    def cancel_and_restart(self):
        pass

    def status(self):
        return self.celery_task.status

    def time_since_completion(self):
        return datetime.utcnow() - self.completed

    class Meta(object):
        abstract = True
        app_label = 'footprint'
