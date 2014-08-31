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
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Assofrom calthorpe.footprint.resources.footprint_resource import FootprintResourceciates.
# Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709.
# Phone: (510) 548-6800. Web: www.calthorpe.com
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.utils import dict_strip_unicode_keys
from footprint.main.lib.functions import get_first

from footprint.main.models.built_form.built_form import BuiltForm
from footprint.main.models.built_form.urban.urban_placetype import Placetype
from footprint.main.models.built_form.placetype_component import PlacetypeComponent, PlacetypeComponentCategory
from footprint.main.models.built_form.primary_component import PrimaryComponent
from footprint.main.models.built_form.urban.building_use_definition import BuildingUseDefinition
from footprint.main.models.built_form.urban.building_use_percent import BuildingUsePercent
from footprint.main.models.built_form.primary_component_percent import PrimaryComponentPercent
from footprint.main.models.built_form.urban.building_attribute_set import BuildingAttributeSet
from footprint.main.models.built_form.built_form_set import BuiltFormSet
from footprint.main.models.presentation.built_form_example import BuiltFormExample
from footprint.main.publishing.tilestache_publishing import on_post_save_built_form_tilestache
from footprint.main.resources.medium_resources import MediumResource
from footprint.main.resources.mixins.mixins import TagResourceMixin, ToManyFieldWithSubclasses, ToManyCustomAddField, PublisherControlMixin, \
    CloneableResourceMixin
from footprint.main.resources.footprint_resource import FootprintResource
from footprint.main.resources.pickled_dict_field import PickledDictField

from footprint.main.models import FlatBuiltForm, PlacetypeComponentPercent, AgricultureAttributeSet

from footprint.main.models.built_form.agriculture.crop import Crop
from footprint.main.models.built_form.agriculture.crop_type import CropType
from footprint.main.models.built_form.agriculture.landscape_type import LandscapeType

from footprint.main.models.built_form.urban.building import Building
from footprint.main.models.built_form.urban.building_type import BuildingType
from footprint.main.models.built_form.urban.urban_placetype import UrbanPlacetype
from footprint.main.resources.flat_built_form_resource import FlatBuiltFormResource

__author__ = 'calthorpe_associates'

class ComponentPercentMixin(ModelResource):
    """
        Generically describes ComponentPercent
    """
    component_class = fields.CharField(attribute='component_class', null=False, readonly=True)
    container_class = fields.CharField(attribute='container_class', null=False, readonly=True)

class BuildingUseDefinitionResource(FootprintResource):

    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = BuildingUseDefinition.objects.all()
        resource_name = 'building_use_definition'


class BuildingUsePercentResource(FootprintResource):

    building_attribute_set = fields.ToOneField('footprint.main.resources.built_form_resources.BuildingAttributeSetResource', 'building_attribute_set', full=False, null=False)
    building_use_definition = fields.ToOneField(BuildingUseDefinitionResource, 'building_use_definition', full=False, null=False)

    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = BuildingUsePercent.objects.all()
        resource_name = 'building_use_percent'


class AgricultureAttributeSetResource(FootprintResource):
    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = AgricultureAttributeSet.objects.all()
        resource_name = 'agriculture_attribute_set'


class BuildingAttributeSetResource(FootprintResource):

    building_use_percents_query = lambda bundle: bundle.obj.buildingusepercent_set.all()
    def hydrate_m2m(self, bundle):
        for building_use_percent in bundle.data['building_use_percents']:
            # Fill in the backreference to building_attribute_set for this nested instance
            # TODO there must be a better to handle this
            # One option is to just not set the foreign_key on the client, since it becomes 0, and then set it belowing in add_builidng_use_percents
            building_use_percent['building_attribute_set'] = building_use_percent['building_attribute_set'].replace('/0/', '/%s/' % bundle.obj.id)
        return super(BuildingAttributeSetResource, self).hydrate_m2m(bundle)

    def add_building_use_percents(bundle, *building_use_percents):
        # Save the instances explicitly since they are based on the set query
        for building_use_percent in building_use_percents:
            building_use_percent.save()
    def remove_building_use_percents(bundle, *building_use_percents):
        for building_use_percent in building_use_percents:
            building_use_percent.delete()

    # The BuildingUsePercents
    building_use_percents = ToManyCustomAddField(BuildingUsePercentResource,
            attribute=building_use_percents_query,
            add=add_building_use_percents,
            remove=remove_building_use_percents,
            full=True,
            null=True)


    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = BuildingAttributeSet.objects.all()
        resource_name = 'building_attribute_set'


class BuiltFormExampleResource(FootprintResource):
    content = PickledDictField(attribute='content', null=True, blank=True, default=lambda: {})

    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = BuiltFormExample.objects.all()
        resource_name = 'built_form_example'


class BuiltFormResource(FootprintResource, TagResourceMixin, PublisherControlMixin, CloneableResourceMixin):
    medium = fields.ToOneField(MediumResource, 'medium', null=True, full=False)
    media = fields.ToManyField(MediumResource, 'media', null=True, full=False)
    examples = fields.ToManyField(BuiltFormExampleResource, 'examples', null=True, full=False)
    flat_building_densities_query = lambda bundle: get_first(FlatBuiltForm.objects.filter(built_form_id=bundle.obj.id))
    flat_building_densities = fields.ToOneField(FlatBuiltFormResource,
        attribute=flat_building_densities_query,
        full=False,
        null=True,
        readonly=True)
    built_form_set_query = lambda bundle: bundle.obj.builtformset_set.all()
    built_form_sets = fields.ToManyField(
        'footprint.main.resources.built_form_resources.BuiltFormSetResource',
        attribute=built_form_set_query,
        full=False,
        null=True,
        readonly=True)

    def hydrate(self, bundle):
        """
            Set the user who created the ConfigEntity
        :param bundle:
        :return:
        """
        if not bundle.obj.id:
            bundle.obj.creator = self.resolve_user(bundle.request.GET)
        bundle.obj.updater = self.resolve_user(bundle.request.GET)
        return super(BuiltFormResource, self).hydrate(bundle)

    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = BuiltForm.objects.filter(deleted=False).all().select_subclasses()
        resource_name = 'built_form'


class BuiltFormSetResource(FootprintResource):
    # These are readonly for now
    built_forms = ToManyFieldWithSubclasses(
        BuiltFormResource,
        attribute="built_forms",
        full=False,
        readonly=False)

    # built_forms = ToManyField(BuiltFormResource, 'built_forms', full=True)
    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = BuiltFormSet.objects.filter(deleted=False)
        resource_name = 'built_form_set'


class PrimaryComponentResource(BuiltFormResource):
    # Reverse Lookup of the each PlacetypeComponent that uses the PrimaryComponent and its percent of use
    primary_component_percent_query = lambda bundle: bundle.obj.primarycomponentpercent_set.all()
    primary_component_percent_set = fields.ToManyField(
        'footprint.main.resources.built_form_resources.PrimaryComponentPercentResource',
         attribute=primary_component_percent_query,
         full=True,
         null=True,
         readonly=True)

    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = PrimaryComponent.objects.filter(deleted=False)
        resource_name = 'primary_component'


class PrimaryComponentPercentResource(FootprintResource, ComponentPercentMixin):
    primary_component = fields.ToOneField('footprint.main.resources.built_form_resources.PrimaryComponentResource', 'primary_component', full=False, null=True)
    placetype_component = fields.ToOneField(
        'footprint.main.resources.built_form_resources.PlacetypeComponentResource', 'placetype_component',
        full=False, null=True, readonly=True)

    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = PrimaryComponentPercent.objects.all()
        resource_name = 'primary_component_percent'


class PlacetypeComponentCategoryResource(FootprintResource):
    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = PlacetypeComponentCategory.objects.filter()
        resource_name = 'placetype_component_category'


class PlacetypeComponentResource(BuiltFormResource):

    component_category = fields.ToOneField(PlacetypeComponentCategoryResource, attribute='component_category')

    # The readonly through instances that show what primary components this placetype component contains and at what percent
    primary_component_percent_query = lambda bundle: bundle.obj.primarycomponentpercent_set.all()

    def add_primary_component_percents(bundle, *primary_component_percents):
        for primary_component_percent in primary_component_percents:
            primary_component_percent.placetype_component = bundle.obj
            primary_component_percent.save()

    def remove_primary_component_percents(bundle, *primary_component_percents):
        for primary_component_percent in primary_component_percents:
            primary_component_percent.delete()

    primary_component_percents = ToManyCustomAddField(
        PrimaryComponentPercentResource,
        attribute=primary_component_percent_query,
        add=add_primary_component_percents,
        remove=remove_primary_component_percents,
        full=True,
        null=True)

    # The readonly through instances that show what placetypes contain this placetype component and at what percent
    placetype_component_percent_query = lambda bundle: bundle.obj.placetypecomponentpercent_set.all()
    placetype_component_percent_set = fields.ToManyField(
       'footprint.main.resources.built_form_resources.PlacetypeComponentPercentResource',
       attribute=placetype_component_percent_query,
       full=True,
       null=True,
       readonly=True)

    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = PlacetypeComponent.objects.filter(deleted=False)
        resource_name = 'placetype_component'


class PlacetypeComponentPercentResource(FootprintResource, ComponentPercentMixin):
    placetype_component = fields.ToOneField('footprint.main.resources.built_form_resources.PlacetypeComponentResource', 'placetype_component', full=False, null=True)
    placetype = fields.ToOneField('footprint.main.resources.built_form_resources.PlacetypeResource', 'placetype',
                                  full=False, null=True, readonly=True)

    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = PlacetypeComponentPercent.objects.all()
        resource_name = 'placetype_component_percent'


class PlacetypeResource(BuiltFormResource):
    placetype_component_percent_query = lambda bundle: bundle.obj.placetypecomponentpercent_set.all()

    def add_placetype_component_percents(bundle, *placetype_component_percents):
        for placetype_component_percent in placetype_component_percents:
            placetype_component_percent.placetype = bundle.obj
            placetype_component_percent.save()

    def remove_placetype_component_percents(bundle, *placetype_component_percents):
        for placetype_component_percent in placetype_component_percents:
            placetype_component_percent.delete()

    placetype_component_percents = ToManyCustomAddField(PlacetypeComponentPercentResource,
                                                      attribute=placetype_component_percent_query,
                                                      add=add_placetype_component_percents,
                                                      remove=remove_placetype_component_percents,
                                                      full=True,
                                                      null=True)

    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = Placetype.objects.filter(deleted=False)
        resource_name = 'placetype'


class BuildingResource(PrimaryComponentResource):
    building_attribute_set = fields.ToOneField(BuildingAttributeSetResource, 'building_attribute_set', full=False, null=True)
    class Meta(PrimaryComponentResource.Meta):
        always_return_data = True
        queryset = Building.objects.filter(deleted=False)
        resource_name = 'building'


class BuildingTypeResource(PlacetypeComponentResource):
    building_attribute_set = fields.ToOneField(BuildingAttributeSetResource, 'building_attribute_set', full=False, null=True)
    class Meta(PlacetypeComponentResource.Meta):
        always_return_data = True
        queryset = BuildingType.objects.filter(deleted=False)
        resource_name = 'building_type'


class UrbanPlacetypeResource(PlacetypeResource):
    building_attribute_set = fields.ToOneField(BuildingAttributeSetResource, 'building_attribute_set', full=False, null=True)
    class Meta(PlacetypeResource.Meta):
        always_return_data = True
        queryset = UrbanPlacetype.objects.filter(deleted=False)
        resource_name = 'urban_placetype'


class CropResource(PrimaryComponentResource):
    agriculture_attribute_set = fields.ToOneField(AgricultureAttributeSetResource, 'agriculture_attribute_set', full=False, null=True)
    class Meta(PrimaryComponentResource.Meta):
        always_return_data = True
        queryset = Crop.objects.filter(deleted=False)
        resource_name = 'crop'


class CropTypeResource(PlacetypeComponentResource):
    agriculture_attribute_set = fields.ToOneField(AgricultureAttributeSetResource, 'agriculture_attribute_set', full=False, null=True)
    class Meta(PlacetypeComponentResource.Meta):
        always_return_data = True
        queryset = CropType.objects.filter(deleted=False)
        resource_name = 'crop_type'


class LandscapeTypeResource(PlacetypeResource):
    agriculture_attribute_set = fields.ToOneField(AgricultureAttributeSetResource, 'agriculture_attribute_set', full=False, null=True)
    class Meta(PlacetypeResource.Meta):
        always_return_data = True
        queryset = LandscapeType.objects.filter(deleted=False)
        resource_name = 'landscape_type'



