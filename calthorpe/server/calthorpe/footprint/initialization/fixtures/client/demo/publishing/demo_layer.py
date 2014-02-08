from footprint.initialization.fixture import LayerConfigurationFixture
from footprint.initialization.fixtures.client.mixins.publishing.layer_primary_base import primary_base_template_context_dict
from footprint.initialization.fixtures.client.demo.base.demo_primary_parcel_feature import DemoPrimaryParcelFeature

from footprint.models.config.scenario import BaseScenario, FutureScenario, Scenario
from footprint.models.keys.keys import Keys
from footprint.models.presentation.presentation_configuration import LayerConfiguration

__author__ = 'calthorpe'


class DemoLayerConfigurationFixture(LayerConfigurationFixture):
    def layer_libraries(self, layers=None):
        return self.parent_fixture.layer_libraries(self.layers())

    def layers(self):
        return self.parent_fixture.layers() + [
            # Only used by BaseScenarios
            LayerConfiguration(
                scope=BaseScenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_PRIMARY_PARCEL_SOURCE,
                visible=True,
                visible_attributes=['land_use_definition_id'],
                built_form_set_key='sacog_land_use',
                template_context_dict=primary_base_template_context_dict(DemoPrimaryParcelFeature),
            ),
            LayerConfiguration(
                # Show in both base and future Scenarios!
                scope=FutureScenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_PRIMARY_PARCEL_SOURCE,
                visible=False,
                visible_attributes=['land_use_definition_id'],
                built_form_set_key='sacog_land_use',
                template_context_dict=primary_base_template_context_dict(DemoPrimaryParcelFeature),
            ),
            LayerConfiguration(
                scope=Scenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_STREAM_FEATURE,
                visible=False,
                visible_attributes=['geography_id'],
                template_context_dict={'attributes': {'geography_id': {'unstyled': True}}}
            ),
            LayerConfiguration(
                scope=Scenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_VERNAL_POOL_FEATURE,
                visible=False,
                visible_attributes=['geography_id'],
                template_context_dict={'attributes': {'geography_id': {'unstyled': True}}}
            ),

            LayerConfiguration(
                scope=Scenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_WETLAND_FEATURE,
                visible=False,
                visible_attributes=['geography_id'],
                template_context_dict={'attributes': {'geography_id': {'unstyled': True}}}
            ),
            LayerConfiguration(
                scope=Scenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_CPAD_HOLDINGS_FEATURE,
                visible=False,
                visible_attributes=['geography_id'],
                template_context_dict={'attributes': {'geography_id': {'unstyled': True}}}
            )
        ]

    def update_or_create_templates(self):
        """
            Delegates to default, which will also create templates for the client's custom layers
        :return:
        """
        self.parent_fixture.update_or_create_templates()
