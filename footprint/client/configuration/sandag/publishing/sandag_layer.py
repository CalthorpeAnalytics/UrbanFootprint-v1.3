from footprint.client.configuration.default.publishing.default_layer import built_form_template_context_dict
from footprint.client.configuration.fixture import LayerConfigurationFixture
from footprint.client.configuration.sandag.config_entity.sandag_region import SandagDbEntityKey
from footprint.main.models import Scenario
from footprint.main.models.keys.keys import Keys
from footprint.main.models.presentation.presentation_configuration import LayerConfiguration
from footprint.main.models.tag import Tag
from footprint.main.publishing.layer_initialization import LayerLibraryKey, LayerSort, LayerTag

__author__ = 'calthorpe_associates'


class SandagLayerConfigurationFixture(LayerConfigurationFixture):
    def layer_libraries(self, layers=None):
        return self.parent_fixture.layer_libraries(
            self.matching_scope(self.layers(), class_scope=self.config_entity and self.config_entity.__class__))

    def layers(self):
        return self.parent_fixture.layers() + [
            LayerConfiguration(
                scope=Scenario.__name__,
                db_entity_key=SandagDbEntityKey.SCENARIO_A_BOUNDARY,
                visible=False,
                visible_attributes=['wkb_geometry'],
                template_context_dict={'attributes': {'wkb_geometry': {'unstyled': True}}}
            ),
            LayerConfiguration(
                scope=Scenario.__name__,
                db_entity_key=SandagDbEntityKey.SCENARIO_B_BOUNDARY,
                visible=False,
                visible_attributes=['wkb_geometry'],
                template_context_dict={'attributes': {'wkb_geometry': {'unstyled': True}}}
            ),
            LayerConfiguration(
                scope=Scenario.__name__,
                db_entity_key=SandagDbEntityKey.SCENARIO_C_BOUNDARY,
                visible=False,
                visible_attributes=['wkb_geometry'],
                template_context_dict={'attributes': {'wkb_geometry': {'unstyled': True}}}
            ),
            LayerConfiguration(
                scope=Scenario.__name__,
                db_entity_key=SandagDbEntityKey.RTP_TRANSIT_NETWORK_2050,
                visible=False,
                visible_attributes=['transit_mode'],
                template_context_dict={'attributes': {'transit_mode': {'unstyled': True}}}
            ),
            LayerConfiguration(
                scope=Scenario.__name__,
                db_entity_key=SandagDbEntityKey.RTP_TRANSIT_STOPS_2050,
                visible=False,
                visible_attributes=['transit_mode'],
                template_context_dict={'attributes': {'transit_mode': {'unstyled': True}}}
            ),
            LayerConfiguration(
                scope=Scenario.__name__,
                layer_library_key=LayerLibraryKey.DEFAULT,
                db_entity_key=SandagDbEntityKey.BASE_PARCEL,
                visible=True,
                visible_attributes=['built_form__id'],
                # The SQL column returned is normally builform_id, so alias it to our expected attribute string
                column_alias_lookup=dict(built_form__id='built_form_id'),
                tags=[Tag.objects.get(tag=LayerTag.DEFAULT)],
                template_context_dict=built_form_template_context_dict(),
                sort_priority=LayerSort.FUTURE+1
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
