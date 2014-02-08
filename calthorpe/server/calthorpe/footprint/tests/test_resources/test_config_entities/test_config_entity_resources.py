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

from tastypie import fields
from footprint.lib.functions import merge
from footprint.models import ConfigEntity, DbEntityInterest, Interest, Project, Scenario, Region
from footprint.models.keys.keys import Keys
from footprint.resources.built_form_resources import BuiltFormSetResource
from footprint.resources.config_entity_resources import ProjectResource, ScenarioResource, RegionResource
from footprint.resources.db_entity_resources import DbEntityInterestResource
from footprint.resources.policy_resources import PolicySetResource
from footprint.resources.presentation_resources import PresentationResource
from footprint.tests.test_resources.resource_tests import ResourceTests

__author__ = 'calthorpe'

class ConfigEntityResourceTest(ResourceTests):
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
    posted_item_id_attributes = ['key']
    attributes_to_only_count = ['presentations', 'db_entities']
    attributes_to_only_compare_keys = ['selections']
    expected_put_modified_attributes = [
        'name',
        'selections__sets__policy_sets',
        'db_entities',
        'built_form_sets']
    model_collections = ConfigEntity.INHERITABLE_COLLECTIONS

    def setUp(self):
        # Dehydrate the instance to create a dictionary that we can POST, PUT, or PATCH.
        self.resource_lookups = {'db_entities':DbEntityInterestResource(), 'policy_sets':PolicySetResource(), 'built_form_sets':BuiltFormSetResource(), 'presentations':PresentationResource()}
        super(ConfigEntityResourceTest, self).setUp()

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
            super(ConfigEntityResourceTest, self).create_post_data(),
            {'selections':self.resource_instance.selections.dehydrate(self.resource_instance.build_bundle(obj=self.first_instance))})

        # For some reason the dehydrate of the parent_config_entity sometimes fails above
        if post_data['parent_config_entity']=='':
            post_data['parent_config_entity'] = self.resource_instance.get_resource_uri(self.resource_instance.build_bundle(obj=self.new_instance.parent_config_entity))
        return post_data

    def post_saved_update(self, instance):
        """
            Because we can't do certain things to an unsaved instance, we do them here after saving.
        :param instance:
        :return:
        """
        return DataProvider().post_save_generated_config_entity(instance)

    def modify_for_put(self, reference_model_instance, dehydrated_instance):
        """
            Modify the deyhdrated_instance to test put
        :param reference_model_instance:
        :param dehydrated_instance:
        :return:
        """

        # Rename
        dehydrated_instance['name'] = 'A'
        # Change a selection
        dehydrated_instance['selections']['sets']['policy_sets'] = self.resource_lookups['policy_sets'].get_resource_uri(reference_model_instance.computed_policy_sets()[1])
        # Add a DbEntityInstance
        dehydrated_instance['db_entity_interests'].append(
            self.dehydrate(
                self.resource_lookups['db_entities'],
                DbEntityInterest(
                    db_entity=DataProvider().create_geojson_layer(reference_model_instance)['layer'],
                    interest=Interest.objects.get(key=Keys.INTEREST_OWNER),
                    id=0, # will be cleared
                    config_entity=self.instances[0] # will be cleared
                ),
                clear_ids=True, # clear id and config_entity dummy values
                extra_atrributes_to_clear=['config_entity']
            ))

        # Remove a BuiltFormSet
        dehydrated_instance['built_form_sets'].pop()
        return dehydrated_instance

    def revert_for_put_comparison(self, original_model_instance):
        def revert(reference_model_instance, updated_dehydrated_instance):
            # Reverse the modifications of modify_for_put
            updated_dehydrated_instance['name'] = original_model_instance
            updated_dehydrated_instance['selections']['sets']['policy_sets'] = self.resource_lookups['policy_sets'].get_resource_uri(original_model_instance.computed_policy_sets()[0])
            updated_dehydrated_instance['db_entity_interests'].pop()
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

        return get_dynamic_resource_class(
            self.resource_class,
            built_form_sets=fields.ToManyField(BuiltFormSetResource, attribute=built_from_sets_query, full=False, null=True),
            policy_sets=fields.ToManyField(PolicySetResource, attribute=policy_sets_query, full=False, null=True),
            db_entities=fields.ToManyField(DbEntityInterestResource, attribute=db_entity_interests_query, full=False, null=True),
            presentations=fields.ToManyField('resources.presentation_resources.PresentationResource', attribute=presentations_query, full=False, null=True))

class TestScenarioResource(ConfigEntityResourceTest):

    model_class = Scenario
    resource_class = ScenarioResource

    def list_generator(self):
        return DataProvider().scenarios()
    def item_generator(self):
        return DataProvider().generate_scenario()

class TestProjectResource(ConfigEntityResourceTest):

    model_class = Project
    resource_class = ProjectResource
    def list_generator(self):
        return DataProvider().projects()
    def item_generator(self):
        return DataProvider().generate_project()

class TestRegionResource(ConfigEntityResourceTest):

    model_class = Region
    resource_class = RegionResource
    def list_generator(self):
        return DataProvider().projects()
    def item_generator(self):
        return DataProvider().generate_project()

