import os
from django.utils import unittest
from nose import with_setup
from footprint.initialization.data_provider import DataProvider
from footprint.models.presentation.layer import Layer
from footprint.models.keys.keys import Keys
from footprint.models.presentation.tilestache_config import *
from footprint.publishing.tilestache_initialization import update_or_create_built_form_template


class TestTileStache(unittest.TestCase):
    """
    The TileStache classes will observe the layer library and the standard list of scenarios, and keep a
    config string to render all of the possible tables when they are requested. These tests make sure that
    system is working properly.
    :return:
    """

    def setup(self):
        # DataProvider().import_parcels()
        update_or_create_built_form_template()
        pass

    def teardown(self):
        pass

    @with_setup(setup, teardown)
    def fake_tilestache_config(self):
        """
        using a totally fake style and layer, generates the Mapnik config file for rendering a layer as raster.
        test makes sure that CartoCSS is working on its local Node.js
        """
        testXML_creation = sampleMapfile()
        assert os.path.exists(testXML_creation)
        pass

    def create_test_layer(self):
        """
        Creates a Layer object to use in tests
        :return: The Layer object
        """

        scenario = DataProvider().scenarios()[0]
        scenario.save()
        layer_db_entity = scenario.selections['db_entities'][Keys.DB_SCENARIO_BUILT_FORM_LAYER]
        layer_presentation = scenario.presentation_set(key=Keys.LAYER_LIBRARY_DEFAULT)[0]
        layer_presentationmedium = layer_presentation.presentationmedium_set.filter(
            db_entity_key=Keys.DB_SCENARIO_BUILT_FORM_LAYER)[0]

        table = '''"{0}"."{1}"'''.format(layer_db_entity.schema, layer_db_entity.table)
        layer, created, updated = Layer.objects.update_or_create(
            presentation=layer_presentation,
            medium=layer_presentationmedium.medium,
            db_entity_key=layer_db_entity.key,
            name="layer_{0}".format(layer_db_entity.key),
            configuration={'table': table, 'style': {}}
        )
        assert Layer.objects.all().exists() is True
        return layer


    @with_setup(setup, teardown)
    def config_object(self):
        scenario = DataProvider().scenarios()[0]
        config, created, updated = TileStacheConfig.objects.update_or_create(name='default')
        config.modify_config()
        x = config

    @with_setup(setup, teardown)
    def run_all_tests(self):
        self.fake_tilestache_config()
        self.config_object()

