# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2012 Calthorpe Associates
#
# This program is free software: you can redistribute it and/or modify it under the terms of the
 # GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
#
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates.
# Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709.
# Phone: (510) 548-6800. Web: www.calthorpe.com
from django.utils import unittest
from nose import with_setup
from footprint.models.geospatial.geojson_feature import GeoJsonFeature
from footprint.tests.data_provider import DataProvider
from footprint.tests.test_models.test_config_entity.test_config_entity import TestConfigEntity
from footprint.utils.utils import get_dynamic_model_class

__author__ = 'calthorpe'

class TestProject(TestConfigEntity):

    def setup(self):
        super(TestProject, self).__init__()

    def teardown(self):
        super(TestProject, self).__init__()

    @with_setup(setup, teardown)
    def test_project_creation(self):
        """
            Tests project creation
        :return:
        """
        projects = DataProvider().projects()
        enhanced_project = projects[0]
        # Assert that the enhanced_project has references to the layers
        geojson_layers = enhanced_project.computed_db_entities(tags__tag='geojson')
        assert(len(geojson_layers)>0)

        for geojson_layer in geojson_layers:

            # Create a subclass to access the layer and a model class
            GeoJsonFeatureSubclass = get_dynamic_model_class(
                GeoJsonFeature,
                '"{0}"."{1}"'.format(geojson_layer.schema, geojson_layer.table),
                {})

            assert len(enhanced_project.db_entities.filter(table=geojson_layer.table))==1
            # Load all the features of the layer that are within the bounds of the enhanced_project. We expect the geojson features to all be within the bounds of the enhanced_project
            matched_enhanced_features = GeoJsonFeatureSubclass.objects.filter(geometry__contained=enhanced_project.bounds)
            assert len(matched_enhanced_features) > 0

