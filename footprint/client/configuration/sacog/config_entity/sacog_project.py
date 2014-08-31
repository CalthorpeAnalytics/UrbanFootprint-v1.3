from footprint.client.configuration.sacog.base.sacog_light_rail_feature import SacogLightRailFeature
from footprint.client.configuration.sacog.base.sacog_light_rail_stops_feature import SacogLightRailStopsFeature
from footprint.client.configuration.sacog.base.sacog_light_rail_stops_quarter_mile_feature \
    import SacogLightRailStopsQuarterMileFeature
from footprint.client.configuration.sacog.base.sacog_light_rail_stops_one_mile_feature \
    import SacogLightRailStopsOneMileFeature
from footprint.client.configuration.sacog.base.sacog_light_rail_stops_half_mile_feature \
    import SacogLightRailStopsHalfMileFeature
from footprint.client.configuration.sacog.config_entity.sacog_region import SacogDbEntityKey
from footprint.main.models import DbEntity
from footprint.main.models.geospatial.behavior import Behavior, BehaviorKey
from footprint.main.models.geospatial.db_entity_configuration import update_or_create_db_entity
from footprint.main.models.geospatial.feature_behavior import FeatureBehavior
from footprint.main.models.geospatial.feature_class_configuration import FeatureClassConfiguration
from footprint.main.models.geospatial.feature_class_creator import FeatureClassCreator
from footprint.client.configuration.fixture import ProjectFixture
from footprint.client.configuration.sacog.base.sacog_existing_land_use_parcel_feature import SacogExistingLandUseParcelFeature
from footprint.client.configuration.sacog.base.sacog_hardwood_feature import SacogHardwoodFeature
from footprint.client.configuration.sacog.base.sacog_stream_feature import SacogStreamFeature
from footprint.client.configuration.sacog.base.sacog_vernal_pool_feature import SacogVernalPoolFeature
from footprint.client.configuration.sacog.base.sacog_wetland_feature import SacogWetlandFeature
from footprint.main.lib.functions import merge
from footprint.main.models.geospatial.intersection import Intersection

__author__ = 'calthorpe_associates'


class SacogProjectFixture(ProjectFixture):
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
        Key = SacogDbEntityKey
        # The Behavior keyspace
        behavior_key = BehaviorKey.Fab.ricate
        # Used to load Behaviors defined elsewhere
        get_behavior = lambda key: Behavior.objects.get(key=behavior_key(key))

        return super(SacogProjectFixture, self).default_db_entities() + [
            update_or_create_db_entity(project, DbEntity(
                key=Key.EXISTING_LAND_USE_PARCEL_SOURCE,
                feature_class_configuration=FeatureClassConfiguration(
                    abstract_class=SacogExistingLandUseParcelFeature,
                    primary_key='geography_id',
                    primary_key_type='varchar',
                    fields=dict(),
                    related_fields=dict(land_use_definition=dict(
                        single=True,
                        related_class_name='footprint.client.configuration.sacog.built_form.sacog_land_use_definition.SacogLandUseDefinition',
                        # Use this for the resource type, since we don't want a client-specific resource URL
                        # TODO not wired up yet
                        resource_model_class_name='footprint.main.models.built_form.ClientLandUseDefinition',
                        related_class_join_field_name='land_use',
                        source_class_join_field_name='land_use')
                    )
                ),
                feature_behavior=FeatureBehavior(
                    behavior=get_behavior('base'),
                    intersection=Intersection(join_type='attribute')
                )
            )),
            update_or_create_db_entity(project, DbEntity(
                key=Key.VERNAL_POOL,
                feature_class_configuration=FeatureClassConfiguration(
                    abstract_class=SacogVernalPoolFeature
                ),
                feature_behavior=FeatureBehavior(
                    behavior=get_behavior('environmental_constraint')
                )
            )),
            update_or_create_db_entity(project, DbEntity(
                key=Key.WETLAND,
                feature_class_configuration=FeatureClassConfiguration(
                    abstract_class=SacogWetlandFeature
                ),
                feature_behavior=FeatureBehavior(
                    behavior=get_behavior('environmental_constraint')
                )
            )),
            update_or_create_db_entity(project, DbEntity(
                key=Key.STREAM,
                feature_class_configuration=FeatureClassConfiguration(
                    abstract_class=SacogStreamFeature
                ),
                feature_behavior=FeatureBehavior(
                    behavior=get_behavior('environmental_constraint')
                )
            )),
            # update_or_create_db_entity(project, DbEntity(
            #     key=Key.HARDWOOD,
            #     feature_class_configuration=FeatureClassConfiguration(
            #         abstract_class=SacogHardwoodFeature
            #     ),
            #     feature_behavior=FeatureBehavior(
            #         behavior=get_behavior('environmental_constraint')
            #     )
            # )),
            update_or_create_db_entity(project, DbEntity(
                key=Key.LIGHT_RAIL,
                feature_class_configuration=FeatureClassConfiguration(
                    abstract_class=SacogLightRailFeature
                ),
                feature_behavior=FeatureBehavior(
                    behavior=get_behavior('travel'),
                    intersection=Intersection(from_type='polygon', to_type='polygon')
                )
            )),
            update_or_create_db_entity(project, DbEntity(
                key=Key.LIGHT_RAIL_STOPS,
                feature_class_configuration=FeatureClassConfiguration(
                    abstract_class=SacogLightRailStopsFeature
                ),
                feature_behavior=FeatureBehavior(
                    behavior=get_behavior('transit_stop')
                )
            )),
            update_or_create_db_entity(project, DbEntity(
                key=Key.LIGHT_RAIL_STOPS_ONE_MILE,
                feature_class_configuration=FeatureClassConfiguration(
                    abstract_class=SacogLightRailStopsOneMileFeature,
                ),
                feature_behavior=FeatureBehavior(
                    behavior=get_behavior('transit_buffer')
                )
            )),
            update_or_create_db_entity(project, DbEntity(
                key=Key.LIGHT_RAIL_STOPS_HALF_MILE,
                feature_class_configuration=FeatureClassConfiguration(
                    abstract_class=SacogLightRailStopsHalfMileFeature
                ),
                feature_behavior=FeatureBehavior(
                    behavior=get_behavior('transit_buffer')
                )
            )),
            update_or_create_db_entity(project, DbEntity(
                key=Key.LIGHT_RAIL_STOPS_QUARTER_MILE,
                feature_class_configuration=FeatureClassConfiguration(
                    abstract_class=SacogLightRailStopsQuarterMileFeature
                ),
                feature_behavior=FeatureBehavior(
                    behavior=get_behavior('transit_buffer')
                )
            ))
        ]