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

from footprint.main.models.built_form.built_form import BuiltForm
from footprint.main.models.built_form.placetype import Placetype
from footprint.main.models.built_form.placetype_component import PlacetypeComponent
from footprint.main.models.built_form.primary_component import PrimaryComponent
from footprint.main.models.built_form.building_use_definition import BuildingUseDefinition
from footprint.main.models.built_form.building_use_percent import BuildingUsePercent
from footprint.main.models.built_form.primary_component_percent import PrimaryComponentPercent
from footprint.main.models.built_form.building_attribute_set import BuildingAttributeSet
from footprint.main.models.built_form.built_form_set import BuiltFormSet
from footprint.main.models.presentation.built_form_example import BuiltFormExample
from footprint.main.resources.medium_resources import MediumResource
from footprint.main.resources.mixins.mixins import TagResourceMixin, ToManyFieldWithSubclasses, ToManyCustomAddField
from footprint.main.resources.footprint_resource import FootprintResource
from footprint.main.resources.pickled_dict_field import PickledDictField

from footprint.main.models import FlatBuiltForm, PlacetypeComponentPercent
from footprint.main.resources.flat_built_form_resource import FlatBuiltFormResource

__author__ = 'calthorpe_associates'


class BuildingUseDefinitionResource(FootprintResource):

    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = BuildingUseDefinition.objects.all()
        resource_name = 'building_use_definition'


class BuildingUsePercentResource(FootprintResource):

    building_use_definition = fields.ToOneField(BuildingUseDefinitionResource, 'building_use_definition', full=True, null=True)

    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = BuildingUsePercent.objects.all()
        resource_name = 'building_use_percent'


class BuildingAttributeSetResource(FootprintResource):

    building_uses_query = lambda bundle: bundle.obj.buildingusepercent_set.all()
    building_uses = fields.ToManyField(BuildingUsePercentResource,
            attribute=building_uses_query,
            full=True,
            null=True)

    flat_building_densities_query = lambda bundle: FlatBuiltForm.objects.get(built_form_id=bundle.obj.id)
    flat_building_densities = fields.ToOneField(FlatBuiltFormResource,
        attribute=flat_building_densities_query,
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


class BuiltFormResource(FootprintResource, TagResourceMixin):
    medium = fields.ToOneField(MediumResource, 'medium', null=True, full=False)
    media = fields.ToManyField(MediumResource, 'media', null=True, full=False)
    examples = fields.ToManyField(BuiltFormExampleResource, 'examples', null=True, full=False)
    # TODO building_attributes on the Django model need to be renamed to building_attribute_set
    building_attribute_set = fields.ToOneField(BuildingAttributeSetResource, 'building_attributes', full=False, null=True)

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


# class PrimaryComponentPercentPlaceTypeComponentResource(BuiltFormResource):
#
#     class Meta(FootprintResource.Meta):
#         always_return_data = True
#         queryset = PrimaryComponentPercent.objects.all()
#         resource_name = 'primary_component_percent_place_type_component'


class PrimaryComponentResource(BuiltFormResource):
    primary_component_percent_query = lambda bundle: bundle.obj.primarycomponentpercent_set.all()
    primary_component_percent_set = fields.ToManyField(
        'footprint.main.resources.built_form_resources.PrimaryComponentPercentResource',
         attribute=primary_component_percent_query,
         full=False,
         null=True,
         readonly=True)

    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = PrimaryComponent.objects.filter(deleted=False)
        resource_name = 'primary_component'

class PrimaryComponentPercentResource(FootprintResource):
    primary_component = fields.ToOneField(PrimaryComponentResource, 'primary_component', full=False, null=True)

    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = PrimaryComponentPercent.objects.all()
        resource_name = 'primary_component_percent'



class PlacetypeComponentResource(BuiltFormResource):
    # The readonly through instances that show what primary components this placetyp component contains and at what percent
    primary_component_percent_query = lambda bundle: bundle.obj.primarycomponentpercent_set.all(),
    @staticmethod
    def add_primary_component_percents(bundle, *primary_component_percents):
        for primary_component_percent in primary_component_percents:
            primary_component_percent.save()

    primary_component_percents = ToManyCustomAddField(
        PrimaryComponentPercentResource,
        attribute=primary_component_percent_query,
        add=add_primary_component_percents,
        full=True,
        null=True)

    # The readonly through instances that show what placetypes contain this placetype component and at what percent
    placetype_component_percent_query = lambda bundle: bundle.obj.placetypecomponentpercent_set.all(),
    placetype_component_percent_set = fields.ToManyField(
       'footprint.main.resources.built_form_resources.PlacetypeComponentPercentResource',
       attribute=placetype_component_percent_query,
       full=False,
       null=True,
       readonly=True)

    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = PlacetypeComponent.objects.filter(deleted=False)
        resource_name = 'placetype_component'


class PlacetypeComponentPercentResource(FootprintResource):
    placetype_component = fields.ToOneField(PlacetypeComponentResource, 'placetype_component', full=False, null=True)
    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = PrimaryComponentPercent.objects.all()
        resource_name = 'placetype_component_percent'


class PlacetypeResource(BuiltFormResource):
    placetype_component_percent_query = lambda bundle: bundle.obj.placetypecomponentpercent_set.all()
    @staticmethod
    def add_placetype_component_percents(bundle, *placetype_component_percents):
        for placetype_component_percent in placetype_component_percents:
            placetype_component_percent.save()
    placetype_component_percents = ToManyCustomAddField(PlacetypeComponentPercentResource,
                                                      attribute=placetype_component_percent_query,
                                                      add=add_placetype_component_percents,
                                                      full=False,
                                                      null=True)

    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = Placetype.objects.filter(deleted=False)
        resource_name = 'placetype'


