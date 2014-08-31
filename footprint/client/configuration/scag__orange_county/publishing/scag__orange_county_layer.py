from footprint.client.configuration.fixture import LayerConfigurationFixture
from footprint.client.configuration.default.publishing.default_layer import built_form_template_context_dict
from footprint.main.publishing.layer_initialization import LayerLibraryKey, LayerTag, LayerSort
from footprint.main.models import Scenario
from footprint.main.models.keys.keys import Keys
from footprint.main.models.presentation.presentation_configuration import LayerConfiguration
from footprint.main.models.tag import Tag

__author__ = 'calthorpe_associates'



class ScagOrangeCountyLayerConfigurationFixtures(LayerConfigurationFixture):
    def layer_libraries(self, layers=None):
        return self.parent_fixture.layer_libraries(self.layers())

    def layers(self):
        return self.parent_fixture.layers() + [
            LayerConfiguration(
                scope=Scenario.__name__,
                layer_library_key=LayerLibraryKey.DEFAULT,
                db_entity_key=Key.BASE_PARCEL,
                visible=False,
                visible_attributes=['builtforms__builtform_id'],
                tags=[Tag.objects.get(tag=LayerTag.DEFAULT)],
                template_context_dict=built_form_template_context_dict(),
                sort_priority=LayerSort.BASE
            ),
            LayerConfiguration(
                scope=Scenario.__name__,
                db_entity_key=Key.TRANSIT_AREAS,
                visible=False,
                visible_attributes=['wkb_geometry'],
                template_context_dict={'attributes': {'wkb_geometry': {'unstyled': True}}}
            ),
        ]

    def import_layer_configurations(self):
        return self.parent_fixture.import_layer_configurations()
