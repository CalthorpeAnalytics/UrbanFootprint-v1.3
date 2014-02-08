from footprint.client.configuration.fixture import LayerConfigurationFixture
from footprint.client.configuration.mixins.publishing.layer_primary_base import primary_base_template_context_dict
from footprint.main.models.config.scenario import BaseScenario, FutureScenario, Scenario
from footprint.main.models.keys.keys import Keys
from footprint.main.models.presentation.presentation_configuration import LayerConfiguration
from footprint.client.configuration.sacog.built_form.sacog_land_use_definition import SacogLandUseDefinition



__author__ = 'calthorpe_associates'


class SacogLayerConfigurationFixture(LayerConfigurationFixture):
    def layer_libraries(self, layers=None):
        return self.parent_fixture.layer_libraries(
            self.matching_scope(self.layers(), class_scope=self.config_entity and self.config_entity.__class__))

    def layers(self):
        return self.parent_fixture.layers() + [
            # Only used by BaseScenarios
            LayerConfiguration(
                scope=BaseScenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_SACOG_EXISTING_LAND_USE_PARCEL_SOURCE,
                visible=True,
                visible_attributes=['land_use_definition__id'],
                column_alias_lookup=dict(land_use_definition__id='land_use_definition_id'),
                built_form_set_key='sacog_land_use',
                template_context_dict=primary_base_template_context_dict(SacogLandUseDefinition)
            ),
            LayerConfiguration(
                # Show in both base and future Scenarios!
                scope=FutureScenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_SACOG_EXISTING_LAND_USE_PARCEL_SOURCE,
                visible=False,
                visible_attributes=['land_use_definition__id'],
                column_alias_lookup=dict(land_use_definition__id='land_use_definition_id'),
                built_form_set_key='sacog_land_use',
                template_context_dict=primary_base_template_context_dict(SacogLandUseDefinition)
            ),
            LayerConfiguration(
                scope=Scenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_STREAM_FEATURE,
                visible=False,
                visible_attributes=['wkb_geometry'],
                template_context_dict={'attributes': {'wkb_geometry': {'unstyled': True}}}
            ),
            LayerConfiguration(
                scope=Scenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_VERNAL_POOL_FEATURE,
                visible=False,
                visible_attributes=['wkb_geometry'],
                template_context_dict={'attributes': {'wkb_geometry': {'unstyled': True}}}
            ),

            LayerConfiguration(
                scope=Scenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_WETLAND_FEATURE,
                visible=False,
                visible_attributes=['wkb_geometry'],
                template_context_dict={'attributes': {'wkb_geometry': {'unstyled': True}}}
            ),

            LayerConfiguration(
                scope=Scenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_HARDWOOD_FEATURE,
                visible=False,
                visible_attributes=['wkb_geometry'],
                template_context_dict={'attributes': {'wkb_geometry': {'unstyled': True}}}
            ),

            LayerConfiguration(
                scope=Scenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_LIGHT_RAIL_FEATURE,
                visible=False,
                visible_attributes=['line'],
                template_context_dict={'attributes': {'line': {'unstyled': True}}}
            ),

            LayerConfiguration(
                scope=Scenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_LIGHT_RAIL_STOPS_FEATURE,
                visible=False,
                visible_attributes=['color'],
                template_context_dict={'attributes': {'color': {'unstyled': True}}}
            ),

            LayerConfiguration(
                scope=Scenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_LIGHT_RAIL_STOPS_ONE_MILE_FEATURE,
                visible=False,
                visible_attributes=['wkb_geometry'],
                template_context_dict={'attributes': {'wkb_geometry': {'unstyled': True}}}
            ),

            LayerConfiguration(
                scope=Scenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_LIGHT_RAIL_STOPS_HALF_MILE_FEATURE,
                visible=False,
                visible_attributes=['wkb_geometry'],
                template_context_dict={'attributes': {'wkb_geometry': {'unstyled': True}}}
            ),

            LayerConfiguration(
                scope=Scenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_LIGHT_RAIL_STOPS_QUARTER_MILE_FEATURE,
                visible=False,
                visible_attributes=['wkb_geometry'],
                template_context_dict={'attributes': {'wkb_geometry': {'unstyled': True}}}
            )

        ]

    def update_or_create_templates(self):
        """
            Delegates to default, which will also create templates for the client's custom layers
        :return:
        """
        self.parent_fixture.update_or_create_templates()

    def import_layer_configurations(self):
        return self.parent_fixture.import_layer_configurations()