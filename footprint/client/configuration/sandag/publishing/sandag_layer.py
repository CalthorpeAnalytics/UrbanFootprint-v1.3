from footprint.client.configuration.fixture import LayerConfigurationFixture
from footprint.main.models import Scenario
from footprint.main.models.keys.keys import Keys
from footprint.main.models.presentation.presentation_configuration import LayerConfiguration

__author__ = 'calthorpe_associates'


class SandagLayerConfigurationFixture(LayerConfigurationFixture):
    def layer_libraries(self, layers=None):
        return self.parent_fixture.layer_libraries(
            self.matching_scope(self.layers(), class_scope=self.config_entity and self.config_entity.__class__))

    def layers(self):
        return self.parent_fixture.layers() + [
            LayerConfiguration(
                scope=Scenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_SANDAG_SCENARIO_A_BOUNDARY,
                visible=False,
                visible_attributes=['geography_id'],
                template_context_dict={'attributes': {'geography_id': {'unstyled': True}}}
            ),
            LayerConfiguration(
                scope=Scenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_SANDAG_SCENARIO_B_BOUNDARY,
                visible=False,
                visible_attributes=['wkb_geometry'],
                template_context_dict={'attributes': {'wkb_geometry': {'unstyled': True}}}
            ),
            LayerConfiguration(
                scope=Scenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_SANDAG_SCENARIO_C_BOUNDARY,
                visible=False,
                visible_attributes=['wkb_geometry'],
                template_context_dict={'attributes': {'wkb_geometry': {'unstyled': True}}}
            ),
            LayerConfiguration(
                scope=Scenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_SANDAG_2050_RTP_TRANSIT_NETWORK,
                visible=False,
                visible_attributes=['transit_mode'],
                template_context_dict={'attributes': {'transit_mode': {'unstyled': True}}}
            ),
            LayerConfiguration(
                scope=Scenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_SANDAG_2050_RTP_TRANSIT_STOPS,
                visible=False,
                visible_attributes=['transit_mode'],
                template_context_dict={'attributes': {'transit_mode': {'unstyled': True}}}
            ),
        ]

    def update_or_create_templates(self):
        """
            Delegates to default, which will also create templates for the client's custom layers
        :return:
        """
        self.parent_fixture.update_or_create_templates()

    def import_layer_configurations(self):
        return self.parent_fixture.import_layer_configurations()
