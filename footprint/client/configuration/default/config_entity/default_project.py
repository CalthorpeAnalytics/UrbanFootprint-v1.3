from footprint.main.models.analysis.climate_zone_feature import ClimateZoneFeature
from footprint.main.models.analysis_module.analysis_module import AnalysisModuleConfiguration, AnalysisModuleKey, AnalysisModule
from footprint.main.models.analysis_module.analysis_tool import AnalysisToolKey
from footprint.main.models.base.base_demographic_feature import BaseDemographicFeature
from footprint.main.models.geospatial.behavior import Behavior, BehaviorKey
from footprint.main.models.geospatial.db_entity_configuration import update_or_create_db_entity
from footprint.main.models.geospatial.db_entity_keys import DbEntityKey
from footprint.main.models.geospatial.feature_behavior import FeatureBehavior
from footprint.main.models.geospatial.feature_class_configuration import FeatureClassConfiguration
from footprint.main.models.geospatial.feature_class_creator import FeatureClassCreator
from footprint.client.configuration.fixture import ProjectFixture, RegionFixture
from footprint.client.configuration.default.default_mixin import DefaultMixin
from footprint.client.configuration.utils import resolve_fixture
from footprint.main.lib.functions import merge
from footprint.main.models import CensusBlockgroup, CensusBlock, BaseFeature, DevelopableFeature, DbEntity, \
    AgricultureFeature
from footprint.main.models.analysis.vmt_features.vmt_trip_lengths_feature import VmtTripLengthsFeature
from footprint.main.models.base.census_tract import CensusTract
from footprint.main.models.base.cpad_holdings_feature import CpadHoldingsFeature
from footprint.main.models.geospatial.intersection import Intersection, IntersectionKey
from footprint.main.models.model_utils import uf_model
from footprint.main.utils.utils import get_property_path

__author__ = 'calthorpe_associates'


class DefaultProjectFixture(DefaultMixin, ProjectFixture):

    def feature_class_lookup(self):
        # Get the client region fixture (or the default region if the former doesn't exist)
        client_region = resolve_fixture("config_entity", "region", RegionFixture)
        region_class_lookup = client_region.feature_class_lookup()
        return merge(
            region_class_lookup,
            FeatureClassCreator(self.config_entity).key_to_dynamic_model_class_lookup(self.default_db_entities())
        )

    def default_behaviors(self):
        """
            Initialize Behavior instances that are not created within a preconfigured DbEntity configuration.
        """
        client_region = resolve_fixture("config_entity", "region", RegionFixture)
        return merge(
            client_region.default_behaviors(),
            # Any project scoped Behavior not defined in default_db_entities
            []
        )

    def default_db_entities(self, **kwargs):
        """
            Projects define DbEntities specific to the Project config_entity instance.
            Each DbEntity configured here should be persisted using update_or_clone_db_entity so that this code
            can be run many times without creating duplicates. The instances configured here are configurations--
            a persisted instance with an id will be returned for each. Similarly the FeatureClassConfiguration
            instances and FeatureBehavior instances configured will be updated or cloned.

            kwargs: overrides can be supplied to override certain values. The override behavior must be hand-crafted
            below
        :return: a dictionary of
        """

        # Always expect a Project instnace
        project = self.config_entity
        # The DbEntity keyspace. These keys have no prefix
        Key = DbEntityKey
        key = DbEntityKey.Fab.ricate
        # The Behavior keyspace
        behavior_key = BehaviorKey.Fab.ricate
        # Used to load Behaviors defined elsewhere
        get_behavior = lambda key: Behavior.objects.get(key=behavior_key(key))
        polygon = IntersectionKey.POLYGON
        centroid = IntersectionKey.CENTROID

        return [
            update_or_create_db_entity(project, DbEntity(
                key=DbEntityKey.BASE,
                extent_authority=True,
                # Override. If a name override is supplied, put it in. Otherwise leave null to derive it from the key
                name=get_property_path(kwargs, 'overrides.%s.name' % Key.BASE),
                feature_class_configuration=FeatureClassConfiguration(
                    abstract_class=BaseFeature,
                    # The Base Feature is normally considered a primary_geography unless overridden
                    primary_geography=get_property_path(kwargs, 'overrides.%s.primary_geography' % Key.BASE) or True,
                    primary_key='geography_id',
                    primary_key_type='varchar',

                    # The Base Feature is normally associated to a subclass of Geography unless overridden
                    geography_class_name=get_property_path(kwargs, 'overrides.%s.geography_class_name' % Key.BASE) or
                                         'footprint.main.models.geographies.parcel.Parcel',
                    # Create a built_form ForeignKey to a single BuiltForm,
                    # by initially joining our 'built_form_key' attribute to its 'key' attribute
                    related_fields=dict(built_form=dict(
                        single=True,
                        related_class_name=uf_model('built_form.built_form.BuiltForm'),
                        source_class_join_field_name='built_form_key',
                        related_class_join_field_name='key',
                    ))
                ),
                feature_behavior=FeatureBehavior(
                    behavior=get_behavior('base'),
                ),
            )),

            update_or_create_db_entity(project, DbEntity(
                key=Key.CENSUS_TRACT,
                feature_class_configuration=FeatureClassConfiguration(
                    abstract_class=CensusTract
                ),
                feature_behavior=FeatureBehavior(
                    behavior=get_behavior('census')
                )
            )),

            update_or_create_db_entity(project, DbEntity(
                key=Key.CENSUS_BLOCKGROUP,
                feature_class_configuration=FeatureClassConfiguration(
                    abstract_class=CensusBlockgroup,
                    related_fields=dict(census_tract=dict(
                        # Relate to a single CensusTract from our tract attribute to theirs
                        single=True,
                        related_key=key('census_tract'),
                        related_class_join_field_name='tract',
                        source_class_join_field_name='tract'))
                ),
                feature_behavior=FeatureBehavior(
                    behavior=get_behavior('census')
                )
            )),

            update_or_create_db_entity(project, DbEntity(
                key=Key.CENSUS_BLOCK,
                feature_class_configuration=FeatureClassConfiguration(
                    abstract_class=CensusBlock,
                    related_fields=dict(census_blockgroup=dict(
                        # Relate to a single CensusBlockgroup from our blockgroup attribute to theirs
                        single=True,
                        related_key=key('census_blockgroup'),
                        related_class_join_field_name='blockgroup',
                        source_class_join_field_name='blockgroup'))
                ),
                feature_behavior=FeatureBehavior(
                    behavior=get_behavior('census')
                )
            )),

            update_or_create_db_entity(project, DbEntity(
                key=Key.DEFAULT_DEVELOPABLE,
                feature_class_configuration=FeatureClassConfiguration(
                    abstract_class=DevelopableFeature,
                    primary_key='geography_id',
                    primary_key_type='varchar'
                ),
                feature_behavior=FeatureBehavior(
                    # Use developable behavior (defined elsewhere)
                    behavior=get_behavior('base'),
                    intersection=Intersection(join_type=IntersectionKey.ATTRIBUTE),
                ),
            )),

            update_or_create_db_entity(project, DbEntity(
                key=DbEntityKey.CPAD_HOLDINGS,
                # Override default name to be more friendly
                name='CPAD Holdings',
                feature_class_configuration=FeatureClassConfiguration(
                    abstract_class=CpadHoldingsFeature
                ),
                feature_behavior=FeatureBehavior(
                    # Use cpad for behavior (defined elsewhere)
                    behavior=get_behavior('environmental_constraint'),
                    intersection=Intersection(from_type=polygon, to_type=polygon),
                )
            )),

            update_or_create_db_entity(project, DbEntity(
                key=DbEntityKey.BASE_DEMOGRAPHIC,
                feature_class_configuration=FeatureClassConfiguration(
                    abstract_class=BaseDemographicFeature,
                    primary_key='geography_id',
                    primary_key_type='varchar'
                ),
                feature_behavior=FeatureBehavior(
                    behavior=get_behavior('base'),
                    # Join by pk attribute to base_feature Features
                    intersection=Intersection(join_type='attribute')
                ),
            )),

            update_or_create_db_entity(project, DbEntity(
                key=DbEntityKey.BASE_AGRICULTURE,
                feature_class_configuration=FeatureClassConfiguration(
                    abstract_class=AgricultureFeature,
                    primary_key='geography_id',
                    primary_key_type='varchar',
                    # Create a built_form ForeignKey to a single BuiltForm, 
                    # by initially joining our 'built_form_key' attribute to its 'key' attribute
                    related_fields=dict(built_form=dict(
                        single=True,
                        related_class_name='footprint.main.models.built_form.built_form.BuiltForm',
                        related_class_join_field_name='key',
                        source_class_join_field_name='built_form_key')
                    )
                ),
                feature_behavior=FeatureBehavior(
                    behavior=get_behavior('base'),
                    intersection=Intersection(join_type=IntersectionKey.ATTRIBUTE)
                )
            )),

            # TODO why is a future defined at the project scope?
            update_or_create_db_entity(project, DbEntity(
                key=DbEntityKey.VMT_FUTURE_TRIP_LENGTHS,
                feature_class_configuration=FeatureClassConfiguration(
                    abstract_class=VmtTripLengthsFeature
                ),
                feature_behavior=FeatureBehavior(
                    behavior=get_behavior('travel'),
                    intersection=Intersection(from_type=IntersectionKey.POLYGON, to_type=IntersectionKey.CENTROID)
                )
            )),

            update_or_create_db_entity(project, DbEntity(
                key=DbEntityKey.VMT_BASE_TRIP_LENGTHS,
                feature_class_configuration=FeatureClassConfiguration(
                    abstract_class=VmtTripLengthsFeature
                ),
                feature_behavior=FeatureBehavior(
                    behavior=get_behavior('travel'),
                    intersection=Intersection(from_type=IntersectionKey.POLYGON, to_type=IntersectionKey.CENTROID)
                )
            )),

            update_or_create_db_entity(project, DbEntity(
                key=DbEntityKey.CLIMATE_ZONE,
                feature_class_configuration=FeatureClassConfiguration(
                    abstract_class=ClimateZoneFeature,
                    related_fields=dict(
                        evapotranspiration_zone=dict(
                            single=True,
                            related_class_name=uf_model('policy.water.evapotranspiration_baseline.EvapotranspirationBaseline'),
                            related_class_join_field_name='zone',
                            source_class_join_field_name='evapotranspiration_zone_id'),

                        forecasting_climate_zone=dict(
                            single=True,
                            related_class_name=uf_model('policy.energy.commercial_energy_baseline.CommercialEnergyBaseline'),
                            related_class_join_field_name='zone',
                            source_class_join_field_name='forecasting_climate_zone_id'),

                        title_24_zone=dict(
                            single=True,
                            related_class_name=uf_model('policy.energy.residential_energy_baseline.ResidentialEnergyBaseline'),
                            related_class_join_field_name='zone',
                            source_class_join_field_name='title_24_zone_id')
                    )
                ),
                feature_behavior=FeatureBehavior(
                    behavior=get_behavior('climate'),
                    intersection=Intersection(from_type=IntersectionKey.POLYGON, to_type=IntersectionKey.CENTROID)
                ),
            ))
        ]

    def import_db_entity_configurations(self, **kwargs):
        return []


    def default_analysis_module_configurations(self, **kwargs):
        config_entity = self.config_entity
        uf_analysis_module = lambda module: 'footprint.main.models.analysis_module.%s' % module

        behavior_key = BehaviorKey.Fab.ricate
        get_behavior = lambda key: Behavior.objects.get(key=behavior_key(key))

        return [
            AnalysisModuleConfiguration.analysis_module_configuration(config_entity,
                key=AnalysisModuleKey.ENVIRONMENTAL_CONSTRAINT,
                name='Environmental Constraints',
                analysis_tools=[
                    dict(
                          class_name=uf_analysis_module('environmental_constraint_module.environmental_constraint_union_tool.EnvironmentalConstraintUnionTool'),
                          key=AnalysisToolKey.ENVIRONMENTAL_CONSTRAINT_UNION_TOOL,
                          behavior=get_behavior('environmental_constraint')
                        )
                ]
            )
        ]
