from footprint.initialization.fixture import LayerConfigurationFixture
from footprint.models import Scenario
from footprint.models.keys.keys import Keys
from footprint.models.presentation.presentation_configuration import LayerConfiguration

__author__ = 'calthorpe'


class SandagLayerConfigurationFixture(LayerConfigurationFixture):
    def layer_libraries(self, layers=None):
        return self.parent_fixture.layer_libraries(self.layers())

    def layers(self):
        return self.parent_fixture.layers() + [
            LayerConfiguration(
                scope=Scenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_SANDAG_SCENARIO_B_BOUNDARY,
                visible=False,
                visible_attributes=['geography_id'],
                template_context_dict={'attributes': {'geography_id': {'unstyled': True}}}
            ),
            LayerConfiguration(
                scope=Scenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_SANDAG_SCENARIO_C_BOUNDARY,
                visible=False,
                visible_attributes=['geography_id'],
                template_context_dict={'attributes': {'geography_id': {'unstyled': True}}}
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
