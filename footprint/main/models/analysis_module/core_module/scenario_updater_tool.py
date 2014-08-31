# coding=utf-8
# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 20.2, **kwargs Calthorpe Associates # # This program is free software: you can redistribute it and/or modify it under the terms of the # GNU General Public License as published by the Free Software Foundation, version 3 of the License.
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
from footprint.common.utils.websockets import send_message_to_client
from footprint.main.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.main.models.analysis_module.analysis_tool import AnalysisTool
from footprint.main.models.analysis_module.core_module.core_update_end_state_demographic_feature import update_end_state_demographic_feature
from footprint.main.models.analysis_module.core_module.core_update_end_state_feature import update_end_state_feature
from footprint.main.models.analysis_module.core_module.core_update_future_scenario_feature import update_future_scenario_feature
from footprint.main.models.analysis_module.core_module.core_update_increment_feature import update_increment_feature
from footprint.main.models.geospatial.db_entity_keys import DbEntityKey
from footprint.main.utils.query_parsing import annotated_related_feature_class_pk_via_geographies

logger = logging.getLogger(__name__)

class ScenarioUpdaterTool(AnalysisTool):

    objects = GeoInheritanceManager()

    class Meta(object):
        app_label = 'main'
        abstract = False


    def progress(self, proportion, **kwargs):
        send_message_to_client(
            kwargs['user'].id,
            dict(
                event='postSavePublisherProportionCompleted',
                job_id=str(kwargs['job'].hashid),
                config_entity_id=self.config_entity.id,
                id=kwargs['analysis_module'].id,
                class_name='AnalysisModule',
                key=kwargs['analysis_module'].key,
                proportion=proportion))

    def update(self, **kwargs):
        """
            :param: kwargs 'ids' is required. They contain the EndStateFeature ids
            that were updated
        """
        logger.info("Executing Scenario Updater (aka Core) using {0}".format(self.config_entity))

        # Get the EndState Feature ids
        ids = kwargs['ids']
        config_entity = kwargs['analysis_module'].config_entity
        feature_class = config_entity.db_entity_feature_class(DbEntityKey.END_STATE)
        features = feature_class.objects.filter(id__in=ids)
        annotated_features = annotated_related_feature_class_pk_via_geographies(features, config_entity, [
            DbEntityKey.END_STATE_DEMOGRAPHIC,
            DbEntityKey.CENSUS_BLOCK,
            DbEntityKey.BASE_DEMOGRAPHIC,
            DbEntityKey.INCREMENT,
            DbEntityKey.BASE,
            DbEntityKey.DEVELOPABLE,
            DbEntityKey.FUTURE_SCENARIO])

        self.progress(0.2, **kwargs)
        update_future_scenario_feature(self.config_entity, annotated_features)
        self.progress(0.2, **kwargs)
        update_end_state_feature(self.config_entity, annotated_features)
        self.progress(0.2, **kwargs)
        update_end_state_demographic_feature(self.config_entity, annotated_features)
        self.progress(0.2, **kwargs)
        update_increment_feature(self.config_entity, annotated_features)
        self.progress(0.2, **kwargs)

        logger.info("Executed Scenario Updater using {0}".format(self.config_entity))

