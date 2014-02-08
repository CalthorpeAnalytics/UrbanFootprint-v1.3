from footprint.initialization.fixture import LayerConfigurationFixture

__author__ = 'calthorpe'



class ScagOrangeCountyLayerConfigurationFixtures(LayerConfigurationFixture):
    def layer_libraries(self, layers=None):
        return self.parent_fixture.layer_libraries(self.layers())

    def layers(self):
        return self.parent_fixture.layers() + []