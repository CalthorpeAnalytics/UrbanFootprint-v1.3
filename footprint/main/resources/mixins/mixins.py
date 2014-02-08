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
from tastypie.fields import ToManyField, NOT_PROVIDED
from tastypie.resources import ModelResource
from footprint.main.lib.functions import map_to_keyed_collections, flatten, map_to_dict, merge, unique, flat_map_values, get_first
from footprint.main.models import ResultLibrary, LayerLibrary
from footprint.main.resources.category_resource import CategoryResource
from footprint.main.resources.policy_resources import PolicySetResource
import logging
from footprint.main.resources.tag_resource import TagResource

__author__ = 'calthorpe_associates'

class ToManyCustomAddField(ToManyField):
    """
        Adds the ability to place an add attribute on the field definition. The add attribute points to a lambda that specifies how to add many-to-many items to a collection. The default Tastypie method just clears the collection and adds all the items, which doesn't work for explicit through class m2ms or our RelatedCollectionAdoption sets. The add lambda accepts the bundle, which should have a reference to the fully hydrated base object at bundle.obj.
    """

    def __init__(self, to, attribute, related_name=None, default=NOT_PROVIDED,
                 null=False, blank=False, readonly=False, full=False,
                 unique=False, help_text=None, add=None):
        super(ToManyCustomAddField, self).__init__(
            to, attribute, related_name=related_name, default=default,
            null=null, blank=blank, readonly=readonly, full=full,
            unique=unique, help_text=help_text
        )
        self.add = add


class SubclassRelatedResourceMixin(object):
    """
        Mixin that allows related items to be subclasses by fetching the resource subclass instead of the base resource
        Make sure that the query is actually returning subclasses by using select_subclasses()
    """
    def get_related_resource(self, related_instance):
        """
        Instantiates the related resource. Override this method to subclass according to the related instance, rather
        than just using the to class of the Field
        """
        related_resource_class = get_first(filter(lambda resource_class: issubclass(related_instance.__class__, resource_class._meta.object_class),
                                  self.to_class().__class__.__subclasses__()), None)
        related_resource = related_resource_class() if related_resource_class else self.to_class()

        if related_resource._meta.api_name is None:
            if self._resource and not self._resource._meta.api_name is None:
                related_resource._meta.api_name = self._resource._meta.api_name

        # Try to be efficient about DB queries.
        related_resource.instance = related_instance
        return related_resource

class ToManyFieldWithSubclasses(SubclassRelatedResourceMixin, ToManyField):
    """
        Mixes in the ability to subclass items
    """
    pass

class ToManyCustomAddFieldWithSubclasses(SubclassRelatedResourceMixin, ToManyCustomAddField):
    """
        Mixes in the ability to subclass items
    """
    pass

class BuiltFormSetsResourceMixin(ModelResource):
    built_from_sets_query = lambda bundle: bundle.obj.computed_built_form_sets()
    add_built_form_sets = lambda bundle, *built_form_sets: bundle.obj.add_built_form_sets(*built_form_sets)
    built_form_sets = ToManyCustomAddField('footprint.main.resources.built_form_resources.BuiltFormSetResource', attribute=built_from_sets_query, add=add_built_form_sets, full=False, null=True)

class PolicySetsResourceMixin(ModelResource):
    policy_sets_query = lambda bundle: bundle.obj.computed_policy_sets()
    add_policy_sets = lambda bundle, *policy_sets: bundle.obj.add_policy_sets(*policy_sets)
    policy_sets = ToManyCustomAddField(PolicySetResource, attribute=policy_sets_query, add=add_policy_sets, full=False, null=True)

class DbEntityResourceMixin(ModelResource):
    db_entity_interests_query = lambda bundle: bundle.obj.computed_db_entity_interests()
    add_db_entity_interests = lambda bundle, *db_entity_interests: bundle.obj.add_db_entity_interests(*db_entity_interests)
    db_entity_interests = ToManyCustomAddField('footprint.main.resources.db_entity_resources.DbEntityInterestResource', attribute=db_entity_interests_query, add=add_db_entity_interests, full=False, null=True)

class PresentationResourceMixin(ModelResource):
    # Select the subclasses since we divide up Presentations by their subclass to help the API user and Sproutcore
    presentations_query = lambda bundle: bundle.obj.presentation_set.all().select_subclasses()
    # Read-only subclassed presentations
    presentations = ToManyFieldWithSubclasses('footprint.main.resources.presentation_resources.PresentationResource', attribute=presentations_query, full=True, null=True, readonly=True)

    def map_uri_to_class_key(self, instances_by_id, uri):
        instance = instances_by_id[uri.split('/')[-2]]
        if isinstance(instance, ResultLibrary):
            return 'results'
        if isinstance(instance, LayerLibrary):
            return 'layers'
        else:
            raise Exception("Unknown Presentation class {0}".format(instance.__class__.__name__()))

    def map_instance_to_class_key(self, instance):
        if isinstance(instance, ResultLibrary):
            return 'results'
        if isinstance(instance, LayerLibrary):
            return 'layers'
        else:
            raise Exception("Unknown Presentation class {0}".format(instance.__class__.__name__()))

    def dehydrate_presentations(self, bundle):
        """
            Separates the presentations by type into a dict to make them easier to digest on the client.
            Any Presentation of type Presentations goes under 'maps'. Any of type ResultPage goes under 'results'. This
            is done because Sproutcore can't easily handle having multiple classes in a single list. But really, it's
            better for an API consumer to see them separated anyway.
        :param bundle:
        :return:
        """
        return map_to_keyed_collections(lambda presentation: self.map_instance_to_class_key(presentation.obj), bundle.data['presentations'])

    def hydrate_presentations(self, bundle):
        """
            Does the reverse of dehydrate_presentations. If the user actually wanted to create new presentations via the
            API they'd simply save a presentation pointing to the correct configEntity, so we could probably just
            disregard this list on post/patch/put.
        :param bundle:
        :return:
        """
        if bundle.data.get('id', 0) == 0:
            # We can't handle presentations on new config_entities yet.
            # One problem is that tastypie/django doesn't like presentations that are actually
            # layer_libraries and result_libraries that have layers and results, respectively
            bundle.data['presentations'] = None
            return bundle

        if bundle.data.get('presentations', None):
            bundle.data['presentations'] = flatten(bundle.data['presentations'].values()) if isinstance(bundle.data['presentations'], dict) else bundle.data['presentations']
        else:
            bundle.data['presentations'] = []
        return bundle


def add_categories(bundle, *submitted_categories):
    """
            When the user updates the values of one or more categories, we assume that they want to delete the current Category instances with the same keys and replace them with the selected Category value. For instance, if a scenario has the Category key:'category' value:'smart' and the user chooses 'dumb' for the new value, we want to delete the Category instance valued by 'smart' and insert the one valued by 'dumb'. But we don't want to mess with Category instances that have different keys
    """
    logger = logging.getLogger(__name__)
    try:
        submitted_categories_by_key = map_to_keyed_collections(lambda category: category.key, submitted_categories)
        existing_categories_by_key = map_to_keyed_collections(lambda category: category.key, bundle.obj.categories.all())
        categories_to_add_or_maintain = flat_map_values(lambda key, categories: unique(categories, lambda category: category.value),
                                                        merge(existing_categories_by_key, submitted_categories_by_key))
        bundle.obj.categories.clear()
        bundle.obj.categories.add(*categories_to_add_or_maintain)
    except Exception, e:
        logger.critical(e.message)


class CategoryResourceMixin(ModelResource):
    # Allow this to be null since categories are currently copied on the server when cloning.
    # They could easily be done on the client
    categories = ToManyCustomAddField(CategoryResource, 'categories', null=True, full=True, add=add_categories)


class TagResourceMixin(ModelResource):
    # TODO setting this read only because its causing permission problems on update!!!
    tags = ToManyField(TagResource, 'tags', full=True, null=True, readonly=True)


