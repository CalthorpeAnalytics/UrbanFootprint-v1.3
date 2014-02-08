# UrbanFootprint-California (v1.0), Land Use self.resource_class Development and Modeling System.
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
from django.db.models import Model
from tastypie.resources import Resource
from tastypie.test import ResourceTestCase
from footprint.lib.functions import map_dict_to_dict, remove_keys, is_list_or_tuple, map_to_dict, merge, dual_map, filter_keys
from footprint.resources.api import list_url, detail_url
from footprint.resources.resource_utils import unbundle
from footprint.tests.data_provider import DataProvider
from footprint.utils.utils import resolve_attribute, reduce_dict_to_difference

__author__ = 'calthorpe'

class ResourceTests(ResourceTestCase):
    # Use ``fixtures`` & ``urls`` as normal. See Django's ``TestCase``
    # documentation for the gory details.
    fixtures = ['test_entries.json']

    # Set this to the Model class of the Resource
    model_class = Model
    # Set this to the Resource class to test
    resource_class = Resource
    # If a modified Resource class is needed for dehydrated instance comparisons, set it here. Otherwise set this the same as resource_class
    comparison_resource_class = None
    # Override to generate a persisted list of instances of the model_class
    def list_generator(self):
        raise "Must override list_generator for class %s".format(self.__class__)
    # Override to generate a single unsaved item of model_class
    def item_generator(self):
        raise "Must override item_generator for class %s".format(self.__class__)
    # A list of query attributes to look up the posted item other than pk or id. For instance, if the instance has a name or key you could use one or both of these to identify the instance.
    posted_item_id_attributes = []
    # Optional operations to do on the posted instance after it is posted and reloaded
    def post_saved_update(self, instance):
        return instance

    expected_put_modified_attributes = []

    def __init__(self, *args, **kwargs):
        self.comparison_resource_class = self.create_resource_comparer()
        super(ResourceTests, self).__init__(*args, **kwargs)

    # Attribute collections of the model
    model_collections = []
    # List attributes of the instance that represent many-to-many collections that should be compared by counting instead of a detailed comparison. This is useful since it may be impossible to do a post and have the many-to-many items match those of self.first_instance, but it should be possible to match the count
    attributes_to_only_count = []
    # A list of attributes whose hydrated values are dicts and should only have the top-level keys compared
    attributes_to_only_compare_keys = ['selections']
    # A dict of many attributes names to Model ResourceClasses
    resource_lookups = {}
    format = 'json'

    def create_resource_comparer(self):
        """
            Optionally creates a subclass of the self.resource_class subclass that simplifies the resource hydration to aid comparison
            By default this returns self.resource_class
        :return:
        """
        return self.resource_class

    def modify_for_put(self, model_instance, dehydrated_instance):
        """
            Override to make changes to a dehydrated instance to test put. Put the equivalent actions in modify for put comparison
        :param model_instance: the regular model instance for reference
        :param dehydrated_instance: the dict instance to modify
        :return: the modified dehydrated_instance
        """
        return dehydrated_instance.copy()


    def revert_for_put_comparison(self, original_instance):
        """
            Override to make changes to a model instance to compare it the changes made to the dehydrated instance in modify_for_put()
        :param instance:
        :return: a lambda or def to which to pass the reference_instance and the dehydrated version of it
        """
        def revert(reference_instance, dehydrated_instance):
            return dehydrated_instance
        return revert

    def setUp(self):
        super(ResourceTests, self).setUp()
        # Forces the test to show a full diff on comparison errors
        self.maxDiff=None

        user = DataProvider().user()
        self.user = user['user']
        self.api_key = user['api_key']
        self.resource_instance = self.resource_class()
        self.resource_instance_comparer = self.comparison_resource_class()
        self.instances = self.list_generator()
        self.first_instance = self.instances[0]
        # This is used to make testing comparison simpler by using resource_uris for Many-to-Many fields
        self.resource_attributes =  self.resource_class.base_fields
        # We also build a detail URI, since we will be using it all over.
        # Some tests will create their own if they need overrides
        self.detail_url = detail_url(self.first_instance)
        self.list_url = list_url(self.model_class)
        self.new_instance = self.item_generator()
        self.post_data = self.create_post_data()

    def create_post_data(self):
        """
            Return an unsaved dehydrated instance based on self.new_instance (no id/pk present) that can be posted and compared to self.first_instance. Override this method to modify the dehydrated instance.
        :return:
        """
        return remove_keys(
            merge({
                'user': detail_url(self.user),
                },
                    # dehydrate the attributes, the many-to-many ones are overridden
                self.dehydrate(self.resource_instance, self.new_instance, clear_ids=True),
                # Since the Presentation is unsaved, Tastypie won't try to compute its Many-to-Many fields, even though they could be computed from the parent_config_entity's items. We'll simply copy those of the first_instance, including the adopted ones and personal ones.
                # Skip presentations and db_entities since the posted instance will make its own version of these
                map_to_dict(
                    lambda attribute: [attribute,
                                       map(
                                           lambda item: self.dehydrate(self.resource_lookups[attribute], item),
                                           self.first_instance._computed(attribute))],
                    set(self.model_collections) - set(self.attributes_to_only_count)),
                ),
            self.attributes_to_only_count
        )

    def dehydrate(self, resource_instance, instance, **kwargs):
        """
        Dehydrates the given instance, a model class, to a python dict, and optionally simplifies it to remove id properties. If the instance is already a dict the dehydration step is skipped
        :param resource_instance:
        :param instance:
        :param kwargs:
        'clear_ids': if True, clear ids for saving, comparison, etc.,
        'extra_attributes_to_clear': array of additional attributes to clear (used with 'clear_ids')
        :return:
        """

        dehydrated = unbundle(resource_instance.full_dehydrate(resource_instance.build_bundle(obj=instance))) if not isinstance(instance, dict) else instance
        return self.simplify_dehydrated_instance(dehydrated, **kwargs)

    def simplify_dehydrated_instance(self, instance, **kwargs):
        """
        :param resource_instance:
        :param instance:
        :param kwargs:
        'clear_ids': if True, clear ids for saving, comparison, etc.,
        'extra_fields_to_clear': array of additional attributes to clear (used with 'clear_ids')
        :return:
        """

        clear_ids = kwargs.get('clear_ids', False)
        extra_attributes_to_clear = kwargs.get('extra_attributes_to_clear', [])
        attributes_to_only_count = kwargs.get('attributes_to_only_count', [])
        attributes_to_only_compare_keys = kwargs.get('attributes_to_only_compare_keys', [])

        # Remove the following id attributes if 'clear_ids' set
        return map_dict_to_dict(
            # Change attributes_to_only_count attributes to a count
            lambda attr, value: [
                attr,
                len(value) if attr in attributes_to_only_count else
                    (sorted(value.keys()) if attr in attributes_to_only_compare_keys else
                    value)],
            remove_keys(
                instance,
                # Remove the following id attributes if 'clear_ids' set
                ['id','pk', 'resource_uri']+extra_attributes_to_clear if clear_ids else []))

    def teardown(self):
        pass

    def get_credentials(self):
        return self.create_apikey(self.user.username, self.api_key)

    def test_get_list_unauthorized(self):
        self.assertHttpUnauthorized(self.api_client.get(list_url(self.model_class), format=self.format))

    def test_get_list(self):
        response = self.api_client.get(list_url(self.model_class)+"&username={0}&api_key={1}".format(self.user.username, self.api_key), format=self.format) #, authentication=self.get_credentials())
        self.assertValidJSONResponse(response)

        # Scope out the data for correctness.
        deserialized_instances = self.deserialize(response)['objects']
        self.assertEqual(len(deserialized_instances), len(self.instances))

    def test_get_detail_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.get(self.detail_url, format=self.format))

    def test_get_detail(self):
        response = self.api_client.get(self.detail_url, format=self.format, authentication=self.get_credentials())
        self.assertValidJSONResponse(response)
        dehydrated_instance = self.serializer.from_json(response.content)
        # Compare the original instance to the dehydrated on from the get call. The comparison will dehydrate the first_instance in order to compare them
        self.assert_equal_contents(self.first_instance, dehydrated_instance)

    def test_post_list_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.post(list_url(self.model_class), format=self.format, data=self.post_data))

    def test_post(self):
        self.assertEqual(self.model_class.objects.count(), len(self.instances))
        http_response = self.api_client.post(
            list_url(self.model_class)+"&username={0}&api_key={1}".format(self.user.username, self.api_key),
            format=self.format,
            data=self.post_data,
            authentication=self.get_credentials())
        posted_instance = self.post_saved_update(
            self.model_class.objects.get(
                **map_to_dict(lambda attribute: [attribute, getattr(self.new_instance,attribute)],
                    self.posted_item_id_attributes)))

        self.assertHttpCreated(http_response)
        # Verify a new one has been added.
        self.assertEqual(self.model_class.objects.count(), len(self.instances)+1)
        # We expect the post instance to match the first_instance, except for ids
        self.assert_equal_contents(self.first_instance, posted_instance)

    def test_put_detail_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.put(self.detail_url, format=self.format, data=self.post_data))

    def prep_for_api_write(self, new_instance, update_method):
        """
            Prepares an instance for a put or post by deserializing it and making test updates using update_method
        :param new_instance:
        :param update_method:
        :return:
        """
        put_url = detail_url(new_instance)
        dehydrated_instance = self.deserialize(
            self.api_client.get(
                put_url,
                format=self.format, authentication=self.get_credentials()))
        new_data = update_method(new_instance, dehydrated_instance)
        return new_data

    def perform_put(self, new_instance, pre_write_update_method):
        new_instance_dehydrated = self.prep_for_api_write(new_instance, pre_write_update_method)
        instance_count = self.model_class.objects.count()
        self.assertHttpAccepted(
            self.api_client.put(
                detail_url(new_instance), format=self.format, data=new_instance_dehydrated, authentication=self.get_credentials()))
        # Make sure the count hasn't changed & we did an update.
        self.assertEqual(self.model_class.objects.count(), instance_count)
        return self.model_class.objects.get(pk=new_instance.pk)

    def perform_list_put(self, new_instances, pre_write_update_methods):
        new_instances_dehydrated = {'objects':dual_map(lambda new_instance, pre_write_update_method: self.prep_for_api_write(new_instance, pre_write_update_method),
            new_instances,
            pre_write_update_methods)}
        instance_count = self.model_class.objects.count()
        self.assertHttpAccepted(
            self.api_client.put(
                self.list_url, format=self.format, data=new_instances_dehydrated, authentication=self.get_credentials()))
        # Make sure the count hasn't changed & we did an update.
        self.assertEqual(self.model_class.objects.count(), instance_count)
        return map(lambda new_instance: self.model_class.objects.get(pk=new_instance.pk), new_instances)

    def test_put_detail(self):
        # Grab the current data & modify it slightly.
        new_instance = self.list_generator()[0]
        updated_instance = self.perform_put(new_instance, self.modify_for_put)
        self.assert_unequal_contents(new_instance, updated_instance, self.expected_put_modified_attributes)
        reverted_instance = self.perform_put(updated_instance, self.revert_for_put_comparison(new_instance))
        self.assert_equal_contents(new_instance, reverted_instance)

    def test_put_list(self):
        # Grab the current data & modify it slightly.
        new_instances = self.list_generator()
        updated_instances = self.perform_list_put(new_instances, map(lambda x: self.modify_for_put, new_instances))
        dual_map(
            lambda new_instance, updated_instance: self.assert_unequal_contents(new_instance, updated_instance, self.expected_put_modified_attributes),
            new_instances,
            updated_instances)
        reverted_instances = self.perform_list_put(updated_instances, map(lambda new_instance: self.revert_for_put_comparison(new_instance), new_instances))
        dual_map(lambda new_instance, reverted_instance: self.assert_equal_contents(new_instance, reverted_instance), new_instances, reverted_instances)

    def prep_for_api_patch(self, new_instance, update_method):
        """
            Prepares an instance for a put/post/patch by deserializing it and making test updates using update_method
        :param new_instance:
        :param update_method:
        :return:
        """
        put_url = detail_url(new_instance)
        dehydrated_instance, copy = map(lambda x: self.deserialize(
            self.api_client.get(
                put_url,
                format=self.format, authentication=self.get_credentials())), [1,2])
        return merge(
            # Take just the keys with changed values
            reduce_dict_to_difference(update_method(new_instance, dehydrated_instance), copy),
            # Also add in the resource_uri since we're updating data
            filter_keys(dehydrated_instance, ['resource_uri']))

    def perform_patch(self, new_instance, pre_write_update_method):
        """
            Simulates a PATCH call by sending just the updated parts of the dehydrated instance.
        :param new_instance:
        :param update_method:
        :return:
        """
        new_instance_dehydrated = self.prep_for_api_patch(new_instance, pre_write_update_method)
        instance_count = self.model_class.objects.count()
        self.assertHttpAccepted(
            self.api_client.patch(
                detail_url(new_instance), format=self.format, data=new_instance_dehydrated, authentication=self.get_credentials()))
        # Make sure the count hasn't changed & we did an update.
        self.assertEqual(self.model_class.objects.count(), instance_count)
        return self.model_class.objects.get(pk=new_instance.pk)

    def perform_list_patch(self, new_instances, pre_write_update_methods):
        new_instances_dehydrated = {'objects':dual_map(lambda new_instance, pre_write_update_method: self.prep_for_api_patch(new_instance, pre_write_update_method),
            new_instances,
            pre_write_update_methods)}
        instance_count = self.model_class.objects.count()
        self.assertHttpAccepted(
            self.api_client.patch(
                self.list_url, format=self.format, data=new_instances_dehydrated, authentication=self.get_credentials()))
        # Make sure the count hasn't changed & we did an update.
        self.assertEqual(self.model_class.objects.count(), instance_count)
        return map(lambda new_instance: self.model_class.objects.get(pk=new_instance.pk), new_instances)

    def test_patch_detail(self):
        # Grab the current data & modify it slightly.
        new_instance = self.list_generator()[0]
        updated_instance = self.perform_patch(new_instance, self.modify_for_put)
        self.assert_unequal_contents(new_instance, updated_instance, self.expected_put_modified_attributes)
        reverted_instance = self.perform_patch(updated_instance, self.revert_for_put_comparison(new_instance))
        self.assert_equal_contents(new_instance, reverted_instance)

    def test_patch_list(self):
        # Grab the current data & modify it slightly.
        new_instances = self.list_generator()
        updated_instances = self.perform_list_patch(new_instances, map(lambda x: self.modify_for_put, new_instances))
        dual_map(
            lambda new_instance, updated_instance: self.assert_unequal_contents(new_instance, updated_instance, self.expected_put_modified_attributes),
            new_instances,
            updated_instances)
        reverted_instances = self.perform_list_patch(updated_instances, map(lambda new_instance: self.revert_for_put_comparison(new_instance), new_instances))
        dual_map(lambda new_instance, reverted_instance: self.assert_equal_contents(new_instance, reverted_instance), new_instances, reverted_instances)


    def test_delete_detail(self):
        instance_count = self.model_class.objects.count()
        self.assertHttpAccepted(self.api_client.delete(self.detail_url, format=self.format, authentication=self.get_credentials()))
        self.assertEqual(instance_count-1, self.model_class.objects.count())

    def assert_equal_contents(self, expected, actual):
        """
            Compares two instances but ignores pk, id, and anything else related to identity
        :param expected:
        :param actual:
        :return:
        """
        self.assert_contents(expected, actual, self.assertEqual)

    def assert_unequal_contents(self, expected, actual, attributes):
        def resolve_type_for_comparison(value):
            if is_list_or_tuple(value):
                return len(value)
            elif isinstance(value, dict):
                return len(value.keys())
            else:
                return value
        for attribute in attributes:
            self.assertNotEqual(*map(lambda instance: resolve_type_for_comparison(resolve_attribute(instance, attribute.split('__'))), [expected, actual]))

        self.assert_contents(expected, actual, self.assertNotEqual)


    def assert_contents(self, expected, actual, assertMethod):
        filter_out = (['key'] if hasattr(expected.__class__, 'unique_key') and expected.__class__.unique_key() else [])
        assertMethod(
            *map (lambda instance: self.dehydrate(
                self.resource_instance_comparer,
                instance,
                clear_ids=True,
                extra_attributes_to_clear=filter_out,
                attributes_to_only_count=self.attributes_to_only_count,
                attributes_to_only_compare_keys=self.attributes_to_only_compare_keys),
                (expected, actual)))

