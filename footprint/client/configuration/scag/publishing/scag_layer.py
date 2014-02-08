from footprint.client.configuration.fixture import LayerConfigurationFixture


__author__ = 'calthorpe_associates'


class ScagLayerConfigurationFixtures(LayerConfigurationFixture):
    def layer_libraries(self, layers=None):
        return self.parent_fixture.layer_libraries(
            self.matching_scope(
                layers or self.layers,
                class_scope=self.config_entity and self.config_entity.__class__))

    def layers(self):
        return self.parent_fixture.layers() + [

        ]