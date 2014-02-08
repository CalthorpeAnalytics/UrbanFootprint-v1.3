from footprint.main.models.geospatial.db_entity_configuration import create_db_entity_configuration
from footprint.main.models.geospatial.feature_class_creator import FeatureClassCreator
from footprint.client.configuration.fixture import ProjectFixture
from footprint.client.configuration.sandag.base.sandag_2050_rtp_transit_network_feature import Sandag2050RtpTransitNetworkFeature
from footprint.client.configuration.sandag.base.sandag_2050_rtp_transit_stop_feature import Sandag2050RtpTransitStopFeature
from footprint.client.configuration.sandag.base.sandag_scenario_b_boundary import SandagScenarioBBoundaryFeature
from footprint.client.configuration.sandag.base.sandag_scenario_c_boundary import SandagScenarioCBoundaryFeature
from footprint.client.configuration.utils import resolve_default_fixture
from footprint.main.lib.functions import merge
from footprint.main.models.keys.keys import Keys

__author__ = 'calthorpe_associates'


class SandagProjectFixture(ProjectFixture):
    def feature_class_lookup(self):
        """
            Adds mappings of custom Feature classes
        :return:
        """
        default_project = resolve_default_fixture("config_entity", "project", ProjectFixture, config_entity=None)
        feature_class_lookup = default_project.feature_class_lookup()
        return merge(
            feature_class_lookup,
            FeatureClassCreator.db_entity_key_to_feature_class_lookup(self.config_entity, self.default_db_entity_configurations())
        )

    def default_db_entity_configurations(self):
        """
            Project specific SACOG additional db_entities
        :param default_dict:
        :return:
        """

        default_project_fixture = self.parent_fixture
        defaults = default_project_fixture.default_db_entity_configurations()
        config_entity = self.config_entity

        return super(SandagProjectFixture, self).default_db_entity_configurations() + [
            create_db_entity_configuration(config_entity,
                key=Keys.DB_ABSTRACT_SANDAG_SCENARIO_B_BOUNDARY,
                base_class=SandagScenarioBBoundaryFeature,
                intersection=dict(type='polygon', to='centroid'),
            ),
            create_db_entity_configuration(config_entity,
                key=Keys.DB_ABSTRACT_SANDAG_SCENARIO_C_BOUNDARY,
                base_class=SandagScenarioCBoundaryFeature,
                intersection=dict(type='polygon', to='centroid'),
            ),
            create_db_entity_configuration(config_entity,
                key=Keys.DB_ABSTRACT_SANDAG_2050_RTP_TRANSIT_NETWORK,
                base_class=Sandag2050RtpTransitNetworkFeature,
                intersection=dict(type='polygon')
            ),
            create_db_entity_configuration(config_entity,
                key=Keys.DB_ABSTRACT_SANDAG_2050_RTP_TRANSIT_STOPS,
                base_class=Sandag2050RtpTransitStopFeature,
                intersection=dict(type='polygon')
            ),
        ]
