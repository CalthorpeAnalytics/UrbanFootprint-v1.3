from django.contrib.auth.models import User
from footprint import settings
from footprint.main.models.analysis.fiscal_feature import FiscalFeature
from footprint.main.models.future.core_end_state_demographic_feature import CoreEndStateDemographicFeature
from footprint.main.models.geospatial.db_entity_configuration import create_db_entity_configuration
from footprint.main.models.geospatial.feature_class_creator import FeatureClassCreator
from footprint.client.configuration.fixture import ScenarioFixture, project_specific_project_fixtures
from footprint.client.configuration.default.default_mixin import DefaultMixin
from footprint.main.lib.functions import merge
from footprint.main.models import FutureScenarioFeature, CoreIncrementFeature, CoreEndStateFeature, \
    VmtQuarterMileBufferFeature, VmtOneMileBufferFeature, VmtVariableBufferFeature, VmtFeature
from footprint.main.models.config.scenario import FutureScenario, Scenario
from footprint.main.models.keys.keys import Keys

__author__ = 'calthorpe_associates'


class DefaultScenarioFixture(DefaultMixin, ScenarioFixture):
    def feature_class_lookup(self):
        # Get the client project fixture (or the default region if the former doesn't exist)
        project_class_lookup = merge(*map(lambda project_fixture: project_fixture.feature_class_lookup(),
                                          project_specific_project_fixtures(config_entity=self.config_entity)))
        return merge(
            project_class_lookup,
            FeatureClassCreator.db_entity_key_to_feature_class_lookup(self.config_entity, self.default_db_entity_configurations())
        )

    def default_db_entity_configurations(self):
        """
            Scenarios define DbEntities specific to the Scenario. Creates a list a dictionary of configuration functionality. Some DbEntities have associated base classes for
            which a dynamic model subclass is created. Some of these subclasses also have associated fields which
            refer to other dynamically created subclasses
        :return:
        """
        config_entity = self.config_entity

        return map(lambda configuration: create_db_entity_configuration(config_entity, **configuration),
            self.matching_scope([
               dict(
                   class_scope=FutureScenario,
                   key=Keys.DB_ABSTRACT_FUTURE_SCENARIO_FEATURE,
                   base_class=FutureScenarioFeature,
                   import_from_db_entity_key=Keys.DB_ABSTRACT_BASE_FEATURE,
                   import_ids_only=True,
                   related_fields=dict(built_form=dict(
                       single=True,
                       related_class_name='footprint.main.models.built_form.built_form.BuiltForm'
                   ))
               ),
               dict(
                   class_scope=FutureScenario,
                   key=Keys.DB_ABSTRACT_INCREMENT_FEATURE,
                   base_class=CoreIncrementFeature,
                   import_from_db_entity_key=Keys.DB_ABSTRACT_BASE_FEATURE,
                   import_ids_only=True
               ),
               dict(
                   class_scope=FutureScenario,
                   key=Keys.DB_ABSTRACT_END_STATE_FEATURE,
                   base_class=CoreEndStateFeature,
                   import_from_db_entity_key=Keys.DB_ABSTRACT_BASE_FEATURE,
                   related_fields=dict(built_form=dict(
                       single=True,
                       related_class_name='footprint.main.models.built_form.built_form.BuiltForm'
                   ))
               ),
               dict(
                   class_scope=FutureScenario,
                   key=Keys.DB_ABSTRACT_END_STATE_DEMOGRAPHIC_FEATURE,
                   base_class=CoreEndStateDemographicFeature,
                   import_from_db_entity_key=Keys.DB_ABSTRACT_BASE_DEMOGRAPHIC_FEATURE
               ),
               dict(
                   class_scope=FutureScenario,
                   key=Keys.DB_ABSTRACT_FISCAL_FEATURE,
                   base_class=FiscalFeature,
                   import_from_db_entity_key=Keys.DB_ABSTRACT_BASE_FEATURE,
                   import_ids_only=True
               ),
               dict(
                   class_scope=Scenario,
                   key=Keys.DB_ABSTRACT_VMT_QUARTER_MILE_BUFFER_FEATURE,
                   base_class=VmtQuarterMileBufferFeature,
                   import_from_db_entity_key=Keys.DB_ABSTRACT_BASE_FEATURE,
                   import_ids_only=True
               ),
               dict(
                   class_scope=Scenario,
                   key=Keys.DB_ABSTRACT_VMT_ONE_MILE_BUFFER_FEATURE,
                   base_class=VmtOneMileBufferFeature,
                   import_from_db_entity_key=Keys.DB_ABSTRACT_BASE_FEATURE,
                   import_ids_only=True
               ),
               dict(
                   class_scope=Scenario,
                   key=Keys.DB_ABSTRACT_VMT_VARIABLE_BUFFER_FEATURE,
                   base_class=VmtVariableBufferFeature,
                   import_from_db_entity_key=Keys.DB_ABSTRACT_BASE_FEATURE,
                   import_ids_only=True
               ),
               dict(
                   class_scope=Scenario,
                   key=Keys.DB_ABSTRACT_VMT_FEATURE,
                   base_class=VmtFeature,
                   import_from_db_entity_key=Keys.DB_ABSTRACT_BASE_FEATURE,
                   import_ids_only=True
               )
            ],
            class_scope=self.config_entity and self.config_entity.__class__))

    def import_db_entity_configurations(self, **kwargs):
        """
            This is to simulate layer upload
        """
        config_entity = self.config_entity

        def new_db_entity_configuration(config_entity, **configuration):
            db_entity_configuration = create_db_entity_configuration(config_entity, **configuration)
            # Wipe this out so to simulate an upload condition
            db_entity_configuration['feature_class_configuration'] = None
            return db_entity_configuration

        return map(lambda configuration: new_db_entity_configuration(config_entity, **configuration),
            self.matching_scope([
                # dict(
                #     class_scope=FutureScenario,
                #     name='Import Test',
                #     key='import_test',
                #     url='file://%s/samples/feature_sample.json' % settings.STATIC_ROOT
                # ),
                dict(
                    class_scope=FutureScenario,
                    name='TAZ Import Test',
                    key='taz_import_test',
                    url='file://%s/TAZ07_w_tahoe.zip' % settings.STATIC_ROOT,
                    creator=User.objects.all()[0],
                    srid=102642,
                ),
                dict(
                    class_scope=FutureScenario,
                    name='California Import Test',
                    key='california_import_test',
                    url='file://%s/Sutter_Cities.zip' % settings.STATIC_ROOT,
                    creator=User.objects.all()[0],
                    srid=102642,
                )
             ],
             class_scope=self.config_entity and self.config_entity.__class__))
