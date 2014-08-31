from footprint.client.configuration.sandag.config_entity.sandag_region import SandagDbEntityKey
from footprint.main.models.model_utils import uf_model
from footprint.main.models import DbEntity
from footprint.main.models.base.base_parcel_feature import BaseParcelFeature
from footprint.main.models.geospatial.behavior import Behavior, BehaviorKey
from footprint.main.models.geospatial.db_entity_configuration import update_or_create_db_entity
from footprint.main.models.geospatial.feature import Feature
from footprint.main.models.geospatial.feature_behavior import FeatureBehavior
from footprint.main.models.geospatial.feature_class_configuration import FeatureClassConfiguration
from footprint.main.models.geospatial.feature_class_creator import FeatureClassCreator
from footprint.client.configuration.fixture import ProjectFixture
from footprint.client.configuration.sandag.base.sandag_2050_rtp_transit_network_feature import Sandag2050RtpTransitNetworkFeature
from footprint.client.configuration.sandag.base.sandag_2050_rtp_transit_stop_feature import Sandag2050RtpTransitStopFeature
from footprint.main.lib.functions import merge
from footprint.main.models.geospatial.intersection import Intersection

__author__ = 'calthorpe_associates'


class SandagProjectFixture(ProjectFixture):
    def feature_class_lookup(self):
        """
            Adds mappings of custom Feature classes
        :return:
        """
        parent_fixture = self.parent_fixture
        feature_class_lookup = parent_fixture.feature_class_lookup()
        return merge(
            feature_class_lookup,
            FeatureClassCreator(self.config_entity).key_to_dynamic_model_class_lookup(self.default_db_entities())
        )

    def default_db_entities(self):
        """
            Project specific SACOG additional db_entities
        :param default_dict:
        :return:
        """

        project = self.config_entity
        # The DbEntity keyspace. These keys have no prefix
        Key = SandagDbEntityKey
        # The Behavior keyspace
        behavior_key = BehaviorKey.Fab.ricate
        # Used to load Behaviors defined elsewhere
        get_behavior = lambda key: Behavior.objects.get(key=behavior_key(key))

        return super(SandagProjectFixture, self).default_db_entities() + [
            update_or_create_db_entity(project, DbEntity(
                key=Key.SCENARIO_A_BOUNDARY,
                feature_class_configuration=FeatureClassConfiguration(
                    abstract_class=Feature
                ),
                feature_behavior=FeatureBehavior(
                    behavior=get_behavior('boundary'),
                    intersection=Intersection(from_type='polygon', to_type='centroid')
                )
            )),
            update_or_create_db_entity(project, DbEntity(
                key=Key.SCENARIO_B_BOUNDARY,
                feature_class_configuration=FeatureClassConfiguration(
                    abstract_class=Feature
                ),
                feature_behavior=FeatureBehavior(
                    behavior=get_behavior('boundary'),
                    intersection=Intersection(from_type='polygon', to_type='centroid')

                )
            )),
            update_or_create_db_entity(project, DbEntity(
                key=Key.SCENARIO_C_BOUNDARY,
                feature_class_configuration=FeatureClassConfiguration(
                    abstract_class=Feature
                ),
                feature_behavior=FeatureBehavior(
                    behavior=get_behavior('boundary'),
                    intersection=Intersection(from_type='polygon', to_type='centroid')
                )
            )),
            update_or_create_db_entity(project, DbEntity(
                key=Key.RTP_TRANSIT_NETWORK_2050,
                feature_class_configuration=FeatureClassConfiguration(
                    abstract_class=Sandag2050RtpTransitNetworkFeature,
                ),
                feature_behavior=FeatureBehavior(
                    behavior=get_behavior('transit_network')
                )
            )),
            update_or_create_db_entity(project, DbEntity(
                key=Key.RTP_TRANSIT_STOPS_2050,
                feature_class_configuration=FeatureClassConfiguration(
                    abstract_class=Sandag2050RtpTransitStopFeature,
                ),
                feature_behavior=FeatureBehavior(
                    behavior=get_behavior('transit_stop')
                )
            )),
            update_or_create_db_entity(project, DbEntity(
                key=Key.BASE_PARCEL,
                feature_class_configuration=FeatureClassConfiguration(
                    abstract_class=BaseParcelFeature,
                    related_fields=dict(built_form=dict(
                        single=True,
                        related_class_name=uf_model('built_form.built_form.BuiltForm'),
                        related_class_join_field_name='key',
                        source_class_join_field_name='built_form_key')
                    )
                ),
                feature_behavior=FeatureBehavior(
                    behavior=get_behavior('base'),
                    intersection=Intersection(from_type='centroid', to_type='polygon')
                )
            ))
        ]
