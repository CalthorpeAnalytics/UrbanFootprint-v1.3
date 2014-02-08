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
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Assofrom footprint.resources.footprint_resource import FootprintResourceciates.
# Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709.
# Phone: (510) 548-6800. Web: www.calthorpe.com
from tastypie import fields
from tastypie.fields import ToManyField

from footprint.models.built_form.built_form import BuiltForm
from footprint.models.built_form.placetype import Placetype
from footprint.models.built_form.placetype_component import PlacetypeComponent
from footprint.models.built_form.primary_component import PrimaryComponent
from footprint.models.built_form.building_use_definition import BuildingUseDefinition
from footprint.models.built_form.building_use_percent import BuildingUsePercent
from footprint.models.built_form.primary_component_percent import PrimaryComponentPercent
from footprint.models.built_form.building_attribute_set import BuildingAttributeSet
from footprint.models.built_form.built_form_set import BuiltFormSet
from footprint.models.presentation.built_form_example import BuiltFormExample

from footprint.resources.category_resource import CategoryResource
from footprint.resources.medium_resources import MediumResource
from footprint.resources.mixins.mixins import TagResourceMixin, ToManyFieldWithSubclasses
from footprint.resources.footprint_resource import FootprintResource
from footprint.resources.pickled_dict_field import PickledDictField

__author__ = 'calthorpe'


class BuildingUseDefinitionResource(FootprintResource):
    category = fields.ToOneField(CategoryResource, 'category', null=True)

    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = BuildingUseDefinition.objects.all()
        resource_name = 'building_use_definition'


class BuildingUsePercentResource(FootprintResource):
    building_use_definition = fields.ToOneField(BuildingUseDefinitionResource, 'building_use_definition', null=True)

    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = BuildingUsePercent.objects.all()
        resource_name = 'building_use_percent'


class BuildingAttributeSetResource(FootprintResource):
    building_uses = ToManyField(BuildingUsePercentResource, 'building_uses')

    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = BuildingAttributeSet.objects.all()
        resource_name = 'building_attributes'


class BuildingResource(FootprintResource):
    building_attributes = fields.ToOneField(BuildingAttributeSetResource, 'building_attributes', full=True)

    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = PrimaryComponent.objects.all()
        resource_name = 'building'


class BuildingPercentResource(FootprintResource):
#    building = fields.ToOneField(BuildingResource, 'building')
#    buildingtype = fields.ToOneField(BuildingTypeResource, 'buildingtype', null=True)
    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = PrimaryComponentPercent.objects.all()
        resource_name = 'building_percent'


class BuildingTypeResource(FootprintResource):
    buildings = ToManyField(BuildingResource, 'buildings')
    category = fields.ToOneField(CategoryResource, 'category', null=True)
    #    placetype_query = lambda bundle: PlacetypeComponent.objects.filter(BuildingType__contains = bundle.obj)

    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = PlacetypeComponent.objects.all()
        resource_name = 'buildingtype'


class BuiltFormExampleResource(FootprintResource):
    content = PickledDictField(attribute='content', null=True, blank=True, default=lambda: {})

    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = BuiltFormExample.objects.all()
        resource_name = 'built_form_example'


class BuiltFormResource(FootprintResource, TagResourceMixin):
    medium = fields.ToOneField(MediumResource, 'medium', null=True, full=True)
    media = fields.ToManyField(MediumResource, 'media', null=True, full=True)
    examples = fields.ToManyField(BuiltFormExampleResource, 'examples', null=True, full=True)

    building_attributes = fields.ToOneField(BuildingAttributeSetResource, 'building_attributes', full=True, null=True)

    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = BuiltForm.objects.all().select_subclasses()
        resource_name = 'built_form'


class BuiltFormSetResource(FootprintResource):
    # These are readonly for now
    built_forms = ToManyFieldWithSubclasses(
        BuiltFormResource,
        attribute="built_forms",
        full=True,
        readonly=True)

    # built_forms = ToManyField(BuiltFormResource, 'built_forms', full=True)
    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = BuiltFormSet.objects.all()
        resource_name = 'built_form_set'


class PlacetypeComponentResource(FootprintResource):
    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = PlacetypeComponent.objects.all()
        resource_name = 'placetype_component'


class PlacetypeResource(FootprintResource):
    building_attributes = fields.ToOneField(BuildingAttributeSetResource, 'building_attributes')

    #    buildingtype = fields.ToOneField(PlacetypeComponentResource, 'buildingtype', null=True)
    buildingtype_query = PlacetypeComponentResource, lambda bundle: PlacetypeComponent.objects.filter(
        placetype_component__contains=bundle.obj)
    #    placetype_components = ToManyField(PlacetypeComponentResource, 'placetype_components')
    #    query_try = lambda bundle: Placetype.objects.filter(placetype_component__contains = bundle.obj)

    def buildingtype_query(bundle):
        PlacetypeComponent.objects.filter(placetype_component__contains=bundle.obj)
        return PlacetypeComponent.objects

    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = Placetype.objects.all()
        resource_name = 'placetype'

        #Outlined the infrastructure resources below,

#
# class InfrastructureResource(FootprintResource):
#     class Meta(FootprintResource.Meta):
#         always_return_data = True
#         queryset = Infrastructure.objects.all()
#         resource_name = 'infrastructure'
#
#
# class InfrastructureAttributeResource(FootprintResource):
#     class Meta(FootprintResource.Meta):
#         always_return_data = True
#         queryset = InfrastructureAttributeSet.objects.all()
#         resource_name = 'infrastructure_attribute_set'
#
#
# class InfrastructureTypeResource(FootprintResource):
# #    infrastructures = ToManyField(InfrastructureResource, 'infrastructurepercent')
#     class Meta(FootprintResource.Meta):
#         always_return_data = True
#         queryset = InfrastructureType.objects.all()
#         resource_name = 'infrastructure_type'
