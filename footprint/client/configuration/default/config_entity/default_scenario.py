from django.contrib.auth.models import User
from footprint import settings
from footprint.main.models.analysis.fiscal_feature import FiscalFeature
from footprint.main.models.analysis_module.analysis_module import AnalysisModuleKey, AnalysisModuleConfiguration
from footprint.main.models.analysis_module.analysis_tool import AnalysisToolKey
from footprint.main.models.future.core_end_state_demographic_feature import CoreEndStateDemographicFeature
from footprint.main.models.future.developable_feature import DevelopableFeature
from footprint.main.models.geospatial.behavior import Behavior, BehaviorKey
from footprint.main.models.geospatial.db_entity_configuration import update_or_create_db_entity
from footprint.main.models.geospatial.db_entity_keys import DbEntityKey
from footprint.main.models.geospatial.feature_behavior import FeatureBehavior
from footprint.main.models.geospatial.feature_class_configuration import FeatureClassConfiguration
from footprint.main.models.geospatial.feature_class_creator import FeatureClassCreator
from footprint.client.configuration.fixture import ScenarioFixture, project_specific_project_fixtures
from footprint.client.configuration.default.default_mixin import DefaultMixin
from footprint.main.lib.functions import merge
from footprint.main.models import FutureScenarioFeature, CoreIncrementFeature, CoreEndStateFeature, \
    VmtQuarterMileBufferFeature, VmtOneMileBufferFeature, VmtVariableBufferFeature, VmtFeature, LandConsumptionFeature,\
    WaterFeature, EnergyFeature, DbEntity, AgricultureFeature, Project
from footprint.main.models.config.scenario import FutureScenario, Scenario
from footprint.main.models.geospatial.intersection import Intersection, IntersectionKey
from footprint.main.models.model_utils import uf_model

__author__ = 'calthorpe_associates'


class DefaultScenarioFixture(DefaultMixin, ScenarioFixture):
    def feature_class_lookup(self):
        # Get the client project fixture (or the default region if the former doesn't exist)
        project_class_lookup = merge(*map(lambda project_fixture: project_fixture.feature_class_lookup(),
                                          project_specific_project_fixtures(config_entity=self.config_entity)))
        return merge(
            project_class_lookup,
            FeatureClassCreator(self.config_entity).key_to_dynamic_model_class_lookup(self.default_db_entities())
        )

    def default_db_entities(self):
        """
            Scenarios define DbEntities specific to the Scenario. Creates a list a dictionary of configuration functionality.
            These are filtered based on whether the given scenario matches the scope in the configuration
        :return:
        """
        scenario = self.config_entity
        # The DbEntity keyspace. These keys have no prefix
        Key = DbEntityKey
        # The Behavior keyspace
        behavior_key = BehaviorKey.Fab.ricate
        # Used to load Behaviors defined elsewhere
        get_behavior = lambda key: Behavior.objects.get(key=behavior_key(key))

        return map(
            lambda db_entity_dict: update_or_create_db_entity(scenario, db_entity_dict['value']),
            self.matching_scope([
                dict(
                    class_scope=FutureScenario,
                    value=DbEntity(
                        key=DbEntityKey.FUTURE_SCENARIO,
                        feature_class_configuration=FeatureClassConfiguration(
                            abstract_class=FutureScenarioFeature,
                            import_from_db_entity_key=DbEntityKey.BASE,
                            import_ids_only=True,
                            # Create a built_form ForeignKey to a single BuiltForm
                            # This is initially populated by the import of the BASE_FEATURE built_form
                            related_fields=dict(built_form=dict(
                                single=True,
                                related_class_name=uf_model('built_form.built_form.BuiltForm')
                            ))
                        ),
                        feature_behavior=FeatureBehavior(
                            behavior=get_behavior('future'),
                            intersection=Intersection(join_type=IntersectionKey.ATTRIBUTE)
                        )
                    )
                ),
                dict(
                    class_scope=FutureScenario,
                    value=DbEntity(
                        key=DbEntityKey.INCREMENT,
                        feature_class_configuration=FeatureClassConfiguration(
                            abstract_class=CoreIncrementFeature,
                            import_from_db_entity_key=DbEntityKey.BASE,
                            import_ids_only=True,
                            related_fields=dict(built_form=dict(
                                single=True,
                                related_class_name=uf_model('built_form.built_form.BuiltForm')
                            ))
                        ),
                        feature_behavior=FeatureBehavior(
                            behavior=get_behavior('future'),
                            intersection=Intersection(join_type=IntersectionKey.ATTRIBUTE)
                        )
                    )
                ),
                dict(
                    class_scope=FutureScenario,
                    value=DbEntity(
                        key=DbEntityKey.END_STATE,
                        feature_class_configuration=FeatureClassConfiguration(
                            abstract_class=CoreEndStateFeature,
                            import_from_db_entity_key=DbEntityKey.BASE,
                            related_fields=dict(built_form=dict(
                                single=True,
                                related_class_name=uf_model('built_form.built_form.BuiltForm')
                            ))
                        ),
                        feature_behavior=FeatureBehavior(
                            behavior=get_behavior('future'),
                            intersection=Intersection(join_type=IntersectionKey.ATTRIBUTE)
                        )
                    )
                ),
                dict(
                    class_scope=FutureScenario,
                    value=DbEntity(
                        key=DbEntityKey.FUTURE_AGRICULTURE,
                        feature_class_configuration=FeatureClassConfiguration(
                            abstract_class=AgricultureFeature,
                            import_from_db_entity_key=DbEntityKey.BASE_AGRICULTURE,
                            import_ids_only=False,
                            related_fields=dict(built_form=dict(
                                single=True,
                                related_class_name=uf_model('built_form.built_form.BuiltForm'),
                                related_class_join_field_name='key',
                                source_class_join_field_name='built_form_key'
                            ))
                        ),
                        feature_behavior=FeatureBehavior(
                            behavior=get_behavior('future'),
                            intersection=Intersection(join_type=IntersectionKey.ATTRIBUTE)
                        )
                    )
                ),
                dict(
                    class_scope=Scenario,
                    value=DbEntity(
                        key=DbEntityKey.DEVELOPABLE,
                        feature_class_configuration=FeatureClassConfiguration(
                            abstract_class=DevelopableFeature,
                            import_from_db_entity_key=DbEntityKey.DEFAULT_DEVELOPABLE,
                            import_ids_only=False
                        ),
                        feature_behavior=FeatureBehavior(
                            behavior=get_behavior('future'),
                            intersection=Intersection(join_type=IntersectionKey.ATTRIBUTE)
                        )
                    )
                ),
                dict(
                    class_scope=FutureScenario,
                    value=DbEntity(
                        key=DbEntityKey.END_STATE_DEMOGRAPHIC,
                        feature_class_configuration=FeatureClassConfiguration(
                            abstract_class=CoreEndStateDemographicFeature,
                            import_from_db_entity_key=DbEntityKey.BASE_DEMOGRAPHIC
                        ),
                        feature_behavior=FeatureBehavior(
                            behavior=get_behavior('future'),
                            intersection=Intersection(join_type=IntersectionKey.ATTRIBUTE)
                        )
                    )
                ),
                dict(
                    class_scope=FutureScenario,
                    value=DbEntity(
                        key=DbEntityKey.FISCAL,
                        feature_class_configuration=FeatureClassConfiguration(
                            abstract_class=FiscalFeature,
                            import_from_db_entity_key=DbEntityKey.BASE,
                            empty_table=True
                        ),
                        feature_behavior=FeatureBehavior(
                            behavior=get_behavior('future'),
                            intersection=Intersection(join_type=IntersectionKey.ATTRIBUTE)
                        )
                    )
                ),
                dict(
                    class_scope=Scenario,
                    value=DbEntity(
                        key=DbEntityKey.VMT_QUARTER_MILE_BUFFER,
                        feature_class_configuration=FeatureClassConfiguration(
                            abstract_class=VmtQuarterMileBufferFeature,
                            import_from_db_entity_key=DbEntityKey.BASE,
                            empty_table=True,
                        ),
                        feature_behavior=FeatureBehavior(
                            behavior=get_behavior('internal_analysis'),
                            intersection=Intersection(join_type=IntersectionKey.ATTRIBUTE)
                        )
                    )
                ),
                dict(
                    class_scope=Scenario,
                    value=DbEntity(
                        key=DbEntityKey.VMT_ONE_MILE_BUFFER,
                        feature_class_configuration=FeatureClassConfiguration(
                            abstract_class=VmtOneMileBufferFeature,
                            import_from_db_entity_key=DbEntityKey.BASE,
                            empty_table=True
                        ),
                        feature_behavior=FeatureBehavior(
                            behavior=get_behavior('internal_analysis'),
                            intersection=Intersection(join_type=IntersectionKey.ATTRIBUTE)
                        )
                    )
                ),
                dict(
                    class_scope=Scenario,
                    value=DbEntity(
                        key=DbEntityKey.VMT_VARIABLE_BUFFER,
                        feature_class_configuration=FeatureClassConfiguration(
                            abstract_class=VmtVariableBufferFeature,
                            import_from_db_entity_key=DbEntityKey.BASE,
                            empty_table=True
                        ),
                        feature_behavior=FeatureBehavior(
                            behavior=get_behavior('internal_analysis'),
                            intersection=Intersection(join_type=IntersectionKey.ATTRIBUTE)
                        )
                    )
                ),
                dict(
                    class_scope=Scenario,
                    value=DbEntity(
                        key=DbEntityKey.VMT,
                        feature_class_configuration=FeatureClassConfiguration(
                            abstract_class=VmtFeature,
                            import_from_db_entity_key=DbEntityKey.BASE,
                            empty_table=True
                        ),
                        feature_behavior=FeatureBehavior(
                            behavior=get_behavior('travel'),
                            intersection=Intersection(join_type=IntersectionKey.ATTRIBUTE)
                        )
                    )
                ),
                dict(
                    class_scope=Scenario,
                    value=DbEntity(
                        key=DbEntityKey.ENERGY,
                        feature_class_configuration=FeatureClassConfiguration(
                            abstract_class=EnergyFeature,
                            import_from_db_entity_key=DbEntityKey.BASE,
                            empty_table=True
                        ),
                        feature_behavior=FeatureBehavior(
                            behavior=get_behavior('energy'),
                            intersection=Intersection(join_type=IntersectionKey.ATTRIBUTE)
                        )
                    )
                ),
                dict(
                    class_scope=Scenario,
                    value=DbEntity(
                        key=DbEntityKey.WATER,
                        feature_class_configuration=FeatureClassConfiguration(
                            abstract_class=WaterFeature,
                            import_from_db_entity_key=DbEntityKey.BASE,
                            empty_table=True
                        ),
                        feature_behavior=FeatureBehavior(
                            behavior=get_behavior('water'),
                            intersection=Intersection(join_type=IntersectionKey.ATTRIBUTE)
                        )
                    )
                )
            ], class_scope=self.config_entity and self.config_entity.__class__))

    def import_db_entity_configurations(self, **kwargs):
        """
            This is to simulate layer upload
        """
        scenario = self.config_entity

        return map(
            lambda db_entity_dict: update_or_create_db_entity(scenario, db_entity_dict['value']),
            self.matching_scope([
                dict(
                    class_scope=FutureScenario,
                    value=DbEntity(
                        name='TAZ Import Test',
                        key='taz_import_test',
                        url='file://%s/TAZ07_w_tahoe.zip' % settings.STATIC_ROOT,
                        creator=User.objects.all()[0],
                        srid=102642,
                        # feature_behavior=FeatureBehavior(
                        #     behavior=Behavior.objects.get(key=BehaviorKey.Fab.ricate('future')),
                        #     intersection=Intersection(join_type=IntersectionKey.POLYGON)
                        # )
                )),
                dict(
                    class_scope=FutureScenario,
                    value=DbEntity(
                        name='California Import Test',
                        key='california_import_test',
                        url='file://%s/Sutter_Cities.zip' % settings.STATIC_ROOT,
                        creator=User.objects.all()[0],
                        srid=102642,
                        # feature_behavior=FeatureBehavior(
                        #     behavior=Behavior.objects.get(key=BehaviorKey.Fab.ricate('future')),
                        #     intersection=Intersection(join_type=IntersectionKey.POLYGON)
                        # )
                )),
            ], class_scope=self.config_entity and self.config_entity.__class__))

    def default_analysis_module_configurations(self, **kwargs):
        config_entity = self.config_entity
        uf_analysis_module = lambda module: 'footprint.main.models.analysis_module.%s' % module

        behavior_key = BehaviorKey.Fab.ricate
        get_behavior = lambda key: Behavior.objects.get(key=behavior_key(key))

        return map(
            lambda configuration:
            AnalysisModuleConfiguration.analysis_module_configuration(config_entity, **configuration),
            self.matching_scope([
                dict(
                    class_scope=FutureScenario,
                    key=AnalysisModuleKey.SCENARIO_BUILDER,
                    name='Scenario Builder',
                    analysis_tools=[
                        dict(
                            class_name=uf_analysis_module('core_module.scenario_updater_tool.ScenarioUpdaterTool'),
                            key=AnalysisToolKey.SCENARIO_UPDATER_TOOL
                        )
                    ],
                    task_name=uf_analysis_module('core_module.core.execute_core'),
                ),
                dict(
                    class_scope=Scenario,
                    key=AnalysisModuleKey.ENVIRONMENTAL_CONSTRAINT,
                    name='Environmental Constraints',
                    analysis_tools=[
                        dict(
                            class_name=uf_analysis_module('environmental_constraint_module.environmental_constraint_updater_tool.EnvironmentalConstraintUpdaterTool'),
                            key=AnalysisToolKey.ENVIRONMENTAL_CONSTRAINT_UPDATER_TOOL,
                            behavior=get_behavior('environmental_constraint'),
                        )
                    ],
                ),
                dict(
                    class_scope=Scenario,
                    key=AnalysisModuleKey.ENERGY,
                    name='Energy Module',
                    analysis_tools=[
                        dict(
                            class_name=uf_analysis_module('energy_module.energy_updater_tool.EnergyUpdaterTool'),
                            key=AnalysisToolKey.ENERGY_UPDATER_TOOL
                        )
                    ],
                ),
                dict(
                    class_scope=Scenario,
                    key=AnalysisModuleKey.WATER,
                    name='Water Module',
                    analysis_tools=[
                        dict(
                            class_name=uf_analysis_module('water_module.water_updater_tool.WaterUpdaterTool'),
                            key=AnalysisToolKey.WATER_UPDATER_TOOL
                        )
                    ]
                ),
                dict(
                    class_scope=Scenario,
                    key=AnalysisModuleKey.VMT,
                    name='Vehicle Miles Traveled',
                    analysis_tools=[
                        dict(
                            class_name=uf_analysis_module('vmt_module.vmt_updater_tool.VmtUpdaterTool'),
                            key=AnalysisToolKey.VMT_UPDATER_TOOL
                        )
                    ]
                ),
                dict(
                    class_scope=FutureScenario,
                    key=AnalysisModuleKey.FISCAL,
                    name='Fiscal Module',
                    analysis_tools=[
                        dict(
                            class_name=uf_analysis_module('fiscal_module.fiscal_updater_tool.FiscalUpdaterTool'),
                            key=AnalysisToolKey.FISCAL_UPDATER_TOOL
                        )
                    ]
                ),
                dict(
                    class_scope=Scenario,
                    key=AnalysisModuleKey.AGRICULTURE,
                    name='Agriculture',
                    analysis_tools=[
                        dict(
                            class_name=uf_analysis_module('agriculture_module.agriculture_updater_tool.AgricultureUpdaterTool'),
                            key=AnalysisToolKey.AGRICULTURE_UPDATER_TOOL
                        )
                    ]
                ),
            ], class_scope=self.config_entity and self.config_entity.__class__)
        )
