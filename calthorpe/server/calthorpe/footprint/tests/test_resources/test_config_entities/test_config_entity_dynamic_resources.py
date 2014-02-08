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

from footprint.lib.functions import merge
from footprint.models import BaseFeature
from footprint.models.keys.keys import Keys
from footprint.resources.base_resources import BaseFeatureResource
from footprint.tests.data_provider import DataProvider
from footprint.tests.test_resources.resource_tests import ResourceTests
from footprint.utils.utils import get_dynamic_resource_class

__author__ = 'calthorpe'

class ConfigEntityDynamicResourceTest(ResourceTests):
    """
        An abstract test class that is used by ConfigEntity subclasses to test their interaction with the Tastypie API
    """

    # The following must be subclassed
    model_class = None
    resource_class = None
    comparison_resource_class = None
    def list_generator(self):
        return []
    def item_generator(self):
        return None

    # Overrides common to all ConfigEntity classes
    posted_item_id_attributes = ['wkb_geometry']
    attributes_to_only_count = []
    attributes_to_only_compare_keys = []
    expected_put_modified_attributes = []
    model_collections = []

    def setUp(self):
        # This holds any attribute resource definitions we might need for ForeignKey or toOne, to Many attributes
        self.resource_lookups = {}
        super(ConfigEntityDynamicResourceTest, self).setUp()

    def create_post_data(self):
        """
            Post an instance that matches self.first_instance as much as possible. We'll compare the saved instance via to self.first_instance
        :return:
        """

        # Dehydrate the instance to create a dictionary that we can POST, PUT, or PATCH. t= {'db_entities':DbEntityInterestResource(), 'policy_sets':PolicySetResource(), 'built_form_sets':BuiltFormSetResource(), 'presentations':PresentationResource()}
        # Make the new_instance match the properties of the first_instance for comparison
        self.new_instance.name = self.first_instance.name

        # Indicates which attributes should be compared by dehydrating to resource_uris for assertion comparison
        post_data = merge(
            super(ConfigEntityDynamicResourceTest, self).create_post_data(),
            {})

        return post_data

    def post_saved_update(self, instance):
        """
            Because we can't do certain things to an unsaved instance, we do them here after saving.
        :param instance:
        :return:
        """
        #return DataProvider().post_save_generated_config_entity(instance)
        pass

class TestBaseFeatureResource(ConfigEntityDynamicResourceTest):

    model_class = BaseFeature
    # This class will be subclassed when the request is being processed
    resource_class = BaseFeatureResource

    def setUp(self):
        self.project = DataProvider().projects()[0]
        self.BaseFeatureClass = self.project.feature_class_of_db_entity(Keys.DB_ABSTRACT_BASE_FEATURE)
        super(TestBaseFeatureResource, self).setUp()
        # Override these urls to include the config_entity. This triggers our custom wrapper to create a dynamic resource based on the config_entity_id
        self.detail_url = ''.join([self.detail_url, '&config_entity_id=', self.project.id])
        self.list_url = ''.join([self.list_url, '&config_entity_id=', self.project.id])

    expected_put_modified_attributes = ['sqft_parcel']

    def list_generator(self):
        return self.BaseFeatureClass.objects.all()[:5]
    def item_generator(self):
        return self.BaseFeatureClass.objects.all()[0]

    def modify_for_put(self, reference_model_instance, dehydrated_instance):
        """
            Modify the deyhdrated_instance to test put
        :param reference_model_instance:
        :param dehydrated_instance:
        :return:
        """

        # Rename
        dehydrated_instance['sqft_parcel'] = 100.5
        return dehydrated_instance

    def revert_for_put_comparison(self, original_model_instance):
        def revert(reference_model_instance, updated_dehydrated_instance):
            # Reverse the modifications of modify_for_put
            updated_dehydrated_instance['name'] = original_model_instance['sqft_parcel']
            return updated_dehydrated_instance
        return revert

