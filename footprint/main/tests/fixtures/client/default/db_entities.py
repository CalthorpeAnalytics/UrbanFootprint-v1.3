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
import glob
import datetime
import os
import geojson
from footprint.main.models.geospatial.geojson_feature import GeoJsonFeature
from django.contrib.gis.geos import GEOSGeometry
from jsonify.templatetags.jsonify import jsonify
from django.conf import settings
from footprint.main.utils.dynamic_subclassing import dynamic_model_class

__author__ = 'calthorpe_associates'

class SampleDbEntityData():
    def geojson_feature_classes(self, schema='public', **kwargs):
        """
            Creates various GeojsonFeature classes by importing geojson and saving it to the database via a dynamic subclass of GeojsonFeature
        :schema: The optional schema to use for the dynamic subclass's meta db_table attribute, which will allow the class's table to be saved in the specified schema. Defaults to public
        :param kwargs use 'limit' to limit the number of classes created
        :return: a list of lists. Each list is a list of features of distinct subclass of GeoJsonFeature that is created dynamically. To persist these features, you must first create the subclass's table in the database using create_table_for_dynamic_class(). You should also register the table as a DbEntity.
        """
        def parse(file):
            """
                Parses a geojosn file and dynamically creates a subclass of GeoJsonFeature
            :param file: a filepath
            :return: a list of instances of the dynamically created subclass. The class must be saved to the database using create_table_for_dynamic_class() prior to persisting the instances. To access the class, simply get the class of the first instance, since they are all identical
            """

            fp = open(file)
            data = geojson.load(fp, object_hook=geojson.GeoJSON.to_instance)
            dynamic_table_name = "{0}{1}".format(os.path.splitext(os.path.basename(file))[0], formatted_timestamp())
            GeoJsonFeatureSubclass = dynamic_model_class(
                GeoJsonFeature,
                schema,
                dynamic_table_name,
                {})

            def instantiate_sub_class(feature):
                """
                    Instantiates an instance of the dynamic subclass of GeoJsonFeature based on the given feature.
                :param feature: A feature parsed django-geojson. The feature is actually reserialized to json in order to construct a GEOSGeometry instance.
                :return: An instance of the GeoJsonFeature subclass, which contains the geometry, properties of the feature, and perhaps the crs
                """
                # TODO, crs should be read from the geojson when present.
                # This crs isn't actually picked up by the GEOSGeometry constructor
                srid = settings.SRID_PREFIX.format(settings.DEFAULT_SRID)
                crs = {
                    "type": "name",
                    "properties": {
                        "name": srid
                    }
                }
                # Ironically, we have to rejsonify the data so that GEOSGeometry can parse the feature as json
                json = jsonify({'type':feature.geometry.type, 'coordinates':feature.geometry.coordinates, 'crs':crs})
                geometry = GEOSGeometry(json)
                properties = feature.properties
                return GeoJsonFeatureSubclass(geometry=geometry, properties=properties)

            return map(lambda feature: instantiate_sub_class(feature), data.features)

        return map(lambda file: parse(file), glob.glob("main/tests/test_data/sample_geojson/*.json")[:kwargs.get('limit',None)])

def formatted_timestamp():
    return datetime.datetime.now().strftime("%S%f")

