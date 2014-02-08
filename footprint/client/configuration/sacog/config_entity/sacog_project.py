from footprint.client.configuration.sacog.base.sacog_light_rail_feature import SacogLightRailFeature
from footprint.client.configuration.sacog.base.sacog_light_rail_stops_feature import SacogLightRailStopsFeature
from footprint.client.configuration.sacog.base.sacog_light_rail_stops_quarter_mile_feature \
    import SacogLightRailStopsQuarterMileFeature
from footprint.client.configuration.sacog.base.sacog_light_rail_stops_one_mile_feature \
    import SacogLightRailStopsOneMileFeature
from footprint.client.configuration.sacog.base.sacog_light_rail_stops_half_mile_feature \
    import SacogLightRailStopsHalfMileFeature
from footprint.main.models.geospatial.db_entity_configuration import create_db_entity_configuration
from footprint.main.models.geospatial.feature_class_creator import FeatureClassCreator
from footprint.client.configuration.fixture import ProjectFixture
from footprint.client.configuration.sacog.base.sacog_existing_land_use_parcel_feature import SacogExistingLandUseParcelFeature
from footprint.client.configuration.sacog.base.sacog_hardwood_feature import SacogHardwoodFeature
from footprint.client.configuration.sacog.base.sacog_stream_feature import SacogStreamFeature
from footprint.client.configuration.sacog.base.sacog_vernal_pool_feature import SacogVernalPoolFeature
from footprint.client.configuration.sacog.base.sacog_wetland_feature import SacogWetlandFeature
from footprint.main.lib.functions import merge
from footprint.main.models.keys.keys import Keys

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
            FeatureClassCreator.db_entity_key_to_feature_class_lookup(self.config_entity, self.default_db_entity_configurations())
        )

    def default_db_entity_configurations(self):
        """
        Project specific SACOG additional db_entities
        :param default_dict:
        :return:
        """

        config_entity = self.config_entity
        parent_fixture = self.parent_fixture
        defaults = parent_fixture.default_db_entity_configurations()

        return super(SacogProjectFixture, self).default_db_entity_configurations() + [
            create_db_entity_configuration(config_entity,
                key=Keys.DB_ABSTRACT_SACOG_EXISTING_LAND_USE_PARCEL_SOURCE,
                base_class=SacogExistingLandUseParcelFeature,
                intersection=dict(type='attribute',  db_entity_key=Keys.DB_ABSTRACT_BASE_FEATURE),
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
                    source_class_join_field_name='land_use')),
            ),
            create_db_entity_configuration(config_entity,
                key=Keys.DB_ABSTRACT_VERNAL_POOL_FEATURE,
                base_class=SacogVernalPoolFeature,
                intersection=dict(type='polygon')
            ),
            create_db_entity_configuration(config_entity,
                key=Keys.DB_ABSTRACT_WETLAND_FEATURE,
                base_class=SacogWetlandFeature,
                intersection=dict(type='polygon')
            ),
            create_db_entity_configuration(config_entity,
                key=Keys.DB_ABSTRACT_STREAM_FEATURE,
                base_class=SacogStreamFeature,
                intersection=dict(type='polygon')
            ),
            create_db_entity_configuration(config_entity,
                key=Keys.DB_ABSTRACT_HARDWOOD_FEATURE,
                base_class=SacogHardwoodFeature,
                intersection=dict(type='polygon')
            ),
            create_db_entity_configuration(config_entity,
                key=Keys.DB_ABSTRACT_LIGHT_RAIL_FEATURE,
                base_class=SacogLightRailFeature,
                intersection=dict(type='polygon')
            ),
            create_db_entity_configuration(config_entity,
                key=Keys.DB_ABSTRACT_LIGHT_RAIL_STOPS_FEATURE,
                base_class=SacogLightRailStopsFeature,
                intersection=dict(type='polygon')
            ),
            create_db_entity_configuration(config_entity,
                key=Keys.DB_ABSTRACT_LIGHT_RAIL_STOPS_ONE_MILE_FEATURE,
                base_class=SacogLightRailStopsOneMileFeature,
                intersection=dict(type='polygon', to='centroid')
            ),
            create_db_entity_configuration(config_entity,
                key=Keys.DB_ABSTRACT_LIGHT_RAIL_STOPS_HALF_MILE_FEATURE,
                base_class=SacogLightRailStopsHalfMileFeature,
                intersection=dict(type='polygon', to='centroid')
            ),
            create_db_entity_configuration(config_entity,
                key=Keys.DB_ABSTRACT_LIGHT_RAIL_STOPS_QUARTER_MILE_FEATURE,
                base_class=SacogLightRailStopsQuarterMileFeature,
                intersection=dict(type='polygon', to='centroid')
            )
        ]