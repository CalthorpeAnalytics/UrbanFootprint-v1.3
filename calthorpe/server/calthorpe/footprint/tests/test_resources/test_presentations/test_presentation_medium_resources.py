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
from tastypie.contrib.contenttypes import fields
from footprint.initialization.data_provider import DataProvider
from footprint.resources.built_form_resources import BuiltFormSetResource
from footprint.resources.config_entity_resources import ScenarioResource, ProjectResource
from footprint.resources.db_entity_resources import DbEntityInterestResource
from footprint.resources.medium_resources import MediumResource
from footprint.models import Presentation, Scenario, Project
from footprint.resources.policy_resources import PolicySetResource
from footprint.resources.presentation_resources import PresentationResource
from footprint.tests.test_resources.resource_tests import ResourceTests
from footprint.tests.test_resources.test_config_entities.test_config_entity_resources import ConfigEntityResourceTest
from footprint.tests.test_resources.test_presentations.test_presentation_resources import PresentationResourceTest
from footprint.utils.dynamic_subclassing import get_dynamic_resource_class

__author__ = 'calthorpe'

class PresentationMediumResourceTest(ResourceTests):
    """
        An abstract test class that is used by Presentation subclasses to test their interaction with the Tastypie API
    """

    # The following must be subclassed
    model_class = Presentation
    resource_class = PresentationResource
    comparison_resource_class = None
    def list_generator(self):
        # Create a sample PresentationConfig and return all of its presentations
        # TODO fix
        #return DataProvider().presentation_config().computed_presentations()
        pass
    def item_generator(self):
        #TODO fix
        #return DataProvider().generate_scenario().presentations[0]
        pass

    # Since Presentations use shared keys, we'll use the combination of name and key to identify a newly posted Presentation
    posted_item_id_attributes = ['name', 'key']
    attributes_to_only_count = []
    attributes_to_only_compare_keys = []
    expected_put_modified_attributes = ['name', 'media']
    model_collections = ['media']

    def setUp(self):
    # Dehydrate the instance to create a dictionary that we can POST, PUT, or PATCH.
        self.resource_lookups = {'db_entities':DbEntityInterestResource(), 'medium':MediumResource()}
        super(PresentationResourceTest, self).setUp()


    def create_post_data(self):
        """
            Post an instance that matches self.first_instance as much as possible. We'll compare the saved instance via to self.first_instance
        :return:
        """

        # Make the new_instance match the properties of the first_instance for comparison
        self.new_instance.name = self.first_instance.name
        # Indicates which attributes should be compared by dehydrating to resource_uris for assertion comparison
        post_data = super(PresentationResourceTest, self).create_post_data()
        return post_data

    def modify_for_put(self, reference_model_instance, dehydrated_instance):
        """
            Modify the deyhdrated_instance to test put
        :param reference_model_instance:
        :param dehydrated_instance:
        :return:
        """

        # Rename
        dehydrated_instance['name'] = 'A'
        # Add a Medium
        medium = DataProvider().generate_medium()
        medium.id = 0
        dehydrated_instance['media'].append(
            self.dehydrate(
                self.resource_lookups['media'],
                medium,
                clear_ids=True, # clear id and config_entity dummy values
                extra_atrributes_to_clear=['config_entity']
            ))
        return dehydrated_instance

    def revert_for_put_comparison(self, original_model_instance):
        def revert(reference_model_instance, updated_dehydrated_instance):
            # Reverse the modifications of modify_for_put
            updated_dehydrated_instance['name'] = original_model_instance
            updated_dehydrated_instance['selections']['sets']['policy_sets'] = self.resource_lookups['policy_sets'].get_resource_uri(original_model_instance.computed_policy_sets()[0])
            updated_dehydrated_instance['db_entities'].pop()
            updated_dehydrated_instance['built_form_sets'].append(
                self.dehydrate(self.resource_lookups['built_form_sets'], list(original_model_instance.computed_db_entities())[-1]))
            return updated_dehydrated_instance
        return revert

    def create_resource_comparer(self):
        """
            Creates a subclass of the self.resource_class subclass that simplifies the resource hydration to aid comparison
        :return:
        """
        built_from_sets_query = lambda bundle: bundle.obj.computed_built_form_sets().order_by('pk')
        policy_sets_query = lambda bundle: bundle.obj.computed_policy_sets().order_by('pk')
        presentations_query = lambda bundle: bundle.obj.presentation_set.all().order_by('pk')
        db_entity_interests_query = lambda bundle: bundle.obj.computed_db_entity_interests().order_by('db_entity__pk')

        return get_dynamic_resource_class(self.resource_class,
            built_form_sets = fields.ToManyField(BuiltFormSetResource, attribute=built_from_sets_query, full=False, null=True),
            policy_sets = fields.ToManyField(PolicySetResource, attribute=policy_sets_query, full=False, null=True),
            db_entities = fields.ToManyField(DbEntityInterestResource, attribute=db_entity_interests_query, full=False, null=True),
            presentations = fields.ToManyField('resources.presentation_resources.PresentationResource', attribute=presentations_query, full=False, null=True))

class TestLayerResource(ConfigEntityResourceTest):

    model_class = Scenario
    resource_class = ScenarioResource
    def list_generator(self):
        return DataProvider().scenarios()
    def item_generator(self):
        return DataProvider().generate_scenario()

class TestResultResource(ConfigEntityResourceTest):

    model_class = Project
    resource_class = ProjectResource
    def list_generator(self):
        return DataProvider().projects()
    def item_generator(self):
        return DataProvider().generate_project()
