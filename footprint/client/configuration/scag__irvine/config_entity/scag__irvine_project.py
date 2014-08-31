from footprint.client.configuration.scag.config_entity.scag_region import ScagDbEntityKey
from footprint.main.models.geospatial.behavior import Behavior, BehaviorKey
from footprint.client.configuration.fixture import ProjectFixture
from footprint.client.configuration.scag__irvine.base.scag_general_plan_parcel_feature import ScagGeneralPlanParcelFeature
from footprint.client.configuration.scag__irvine.base.scag_primary_spz_feature import ScagPrimarySPZFeature
from footprint.client.configuration.scag__irvine.base.scag_floodplain_feature import ScagFloodplainFeature
from footprint.client.configuration.scag__irvine.base.scag_tier1_taz_feature import ScagTier1TazFeature
from footprint.client.configuration.scag__irvine.base.scag_tier2_taz_feature import ScagTier2TazFeature
from footprint.client.configuration.scag__irvine.base.scag_parks_open_space_feature import ScagParksOpenSpaceFeature
from footprint.client.configuration.scag__irvine.base.scag_existing_land_use_parcel_feature import ScagExistingLandUseParcelFeature
from footprint.main.models.geospatial.db_entity import DbEntity
from footprint.main.models.geospatial.db_entity_configuration import update_or_create_db_entity
from footprint.main.models.geospatial.db_entity_keys import DbEntityKey
from footprint.main.models.geospatial.feature import Feature
from footprint.main.models.geospatial.feature_behavior import FeatureBehavior
from footprint.main.models.geospatial.feature_class_configuration import FeatureClassConfiguration

__author__ = 'calthorpe_associates'


class ScagIrvineProjectFixture(ProjectFixture):

    def default_db_entities(self):
        """
            Project specific SCAG additional db_entities
        :param default_dict:
        :return:
        """

        project = self.config_entity
        # The DbEntity keyspace. These keys have no prefix
        Key = ScagDbEntityKey
        # The Behavior keyspace
        behavior_key = BehaviorKey.Fab.ricate
        # Used to load Behaviors defined elsewhere
        get_behavior = lambda key: Behavior.objects.get(key=behavior_key(key))

        return super(ScagIrvineProjectFixture, self).default_db_entities() + [
            update_or_create_db_entity(project, DbEntity(
                key=Key.EXISTING_LAND_USE_PARCEL_SOURCE,
                feature_class_configuration=FeatureClassConfiguration(
                    abstract_class=ScagExistingLandUseParcelFeature,
                    primary_geography=True,
                    related_fields=dict(
                        land_use_definition=dict(
                            single=True,
                            related_class_name='footprint.client.configuration.sacog.built_form.scag_land_use_definition.ScagLandUseDefinition',
                            related_class_join_field_name='land_use',
                            source_class_join_field_name='land_use'
                        ),
                        census_blocks=dict(
                            single=True,
                            related_key=DbEntityKey.CENSUS_BLOCK,
                            related_class_join_field_name='block',
                            source_class_join_field_name='census_block'
                        )
                    )
                ),
                feature_behavior=FeatureBehavior(
                    get_behavior('base')
                )
            )),
            update_or_create_db_entity(project, DbEntity(
                key=Key.GENERAL_PLAN,
                feature_class_configuration=FeatureClassConfiguration(
                    abstract_class=ScagGeneralPlanParcelFeature,
                    related_fields=dict(
                        land_use_definition=dict(
                        single=True,
                        related_class_name='footprint.client.configuration.sacog.built_form.scag_land_use_definition.ScagLandUseDefinition',
                        related_class_join_field_name='land_use',
                        source_class_join_field_name='scag_general_plan_code')
                    )
                ),
                feature_behavior=FeatureBehavior(
                    get_behavior('base')
                )
            )),

            update_or_create_db_entity(project, DbEntity(
                key=Key.PRIMARY_SPZ_SOURCE,
                feature_class_configuration=FeatureClassConfiguration(
                    abstract_class=ScagPrimarySPZFeature,
                    primary_geography=True
                ),
                feature_behavior=FeatureBehavior(
                    get_behavior('base')
                )
            )),

            update_or_create_db_entity(project, DbEntity(
                key=Key.JURISDICTION_BOUNDARY,
                feature_class_configuration=FeatureClassConfiguration(
                    abstract_class=Feature
                ),
                feature_beahvior=FeatureBehavior(
                    get_behavior('base')
                )
            )),

            update_or_create_db_entity(project, DbEntity(
                key=Key.SPHERE_OF_INFLUENCE,
                feature_class_configuration=FeatureClassConfiguration(
                    abstract_class=Feature
                ),
                feature_behavior=FeatureBehavior(
                    get_behavior('base')
                )
            )),

            update_or_create_db_entity(project, DbEntity(
                key=Key.FLOODPLAIN,
                feature_class_configuration=FeatureClassConfiguration(
                    abstract_class=ScagFloodplainFeature
                ),
                feature_behavior=FeatureBehavior(
                    get_behavior('environmental_constraint')
                )
            )),

            update_or_create_db_entity(project, DbEntity(
                key=Key.TIER1_TAZ,
                feature_class_configuration=FeatureClassConfiguration(
                    abstract_class=ScagTier1TazFeature,
                ),
                feature_behavior=FeatureBehavior(
                    get_behavior('base')
                )
            )),
            update_or_create_db_entity(project, DbEntity(
                key=Key.TIER2_TAZ,
                feature_class_configuration=FeatureClassConfiguration(
                    abstract_class=ScagTier2TazFeature,
                ),
                feature_behavior=FeatureBehavior(
                    get_behavior('base')
                )
            )),

            update_or_create_db_entity(project, DbEntity(
                key=Key.PARKS_OPEN_SPACE,
                feature_class_configuration=FeatureClassConfiguration(
                    abstract_class=ScagParksOpenSpaceFeature
                ),
                feature_behavior=FeatureBehavior(
                    get_behavior('environmental_constraint')
                )
            )),

            update_or_create_db_entity(project, DbEntity(
                key=Key.TRANSIT_AREAS,
                feature_class_configuration=FeatureClassConfiguration(
                    abstract_class=Feature
                ),
                feature_behavior=FeatureBehavior(
                    get_behavior('transit')
                )
            ))

        ]
