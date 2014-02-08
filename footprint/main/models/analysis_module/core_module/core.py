# coding=utf-8
# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2012 Calthorpe Associates # # This program is free software: you can redistribute it and/or modify it under the terms of the # GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; # without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
#
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates.
# Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709.
# Phone: (510) 548-6800. Web: www.calthorpe.com

import logging
from footprint.celery import app
from footprint.common.utils.websockets import send_message_to_client
from footprint.main.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.main.models import Job
from footprint.main.models.analysis_module.core_module.core_update_end_state_demographic_feature import update_end_state_demographic_feature
from footprint.main.models.analysis_module.core_module.core_update_end_state_feature import update_end_state_feature
from footprint.main.models.analysis_module.core_module.core_update_future_scenario_feature import update_future_scenario_feature
from footprint.main.models.analysis_module.core_module.core_update_increment_feature import update_increment_feature
from footprint.main.models.analysis_module.analysis_module import AnalysisModule
from footprint.main.models.geospatial.feature_class_creator import FeatureClassCreator
logger = logging.getLogger(__name__)

class Core(AnalysisModule):
    objects = GeoInheritanceManager()

    def start(self):
        job = Job.objects.create(
            type="core",
            status="New",
            user=self.user
        )
        job.save()

        task = executeCore.apply_async(
            args=[job.hashid, self.user, self.config_entity.subclassed_config_entity],
            soft_time_limit=3600,
            time_limit=3600,
            countdown=1
        )

        job = Job.objects.get(hashid=job.hashid)
        job.task_id = task.id

    class Meta(object):
        app_label = 'main'

# Temporary until we figure out CeleryTask
@app.task
def executeCore(hash_id, user, config_entity):
    # Make sure all related models have been created before querying
    FeatureClassCreator(config_entity).ensure_dynamic_models()
    logger.info("Executing Core using {0}".format(config_entity))
    run_core(config_entity)
    logger.info("Done executing Core")
    logger.info("Executed Core using {0}".format(config_entity))
    send_message_to_client(user.id,
                           dict(event='analyticModule{0}Completed'.format(Core.__name__),
                                config_entity_id=config_entity.id)
    )


def run_core(config_entity):
    update_future_scenario_feature(config_entity)
    update_end_state_feature(config_entity)
    update_end_state_demographic_feature(config_entity)
    update_increment_feature(config_entity)
    from footprint.main.publishing.config_entity_publishing import post_save_config_entity_analytic_run
    post_save_config_entity_analytic_run.send(sender=config_entity.__class__, config_entity=config_entity, module='core')
