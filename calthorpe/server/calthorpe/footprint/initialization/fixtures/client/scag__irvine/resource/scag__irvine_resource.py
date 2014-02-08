# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2013 Calthorpe Associates
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
from tastypie import fields
from tastypie.fields import ToOneField
from footprint.initialization.fixtures.client.scag__irvine.base.scag_primary_spz_feature import ScagPrimarySPZFeature
from footprint.initialization.fixtures.client.scag__irvine.base.scag_general_plan_parcel_feature import ScagGeneralPlanFeature
from footprint.initialization.fixtures.client.scag__irvine.base.scag_existing_land_use_parcel_feature import ScagExistingLandUseParcelFeature
from footprint.models.analysis_module.core import executePrimary
from footprint.resources.base_resources import CensusBlockResource
from footprint.resources.client.client_land_use_definition_resource import ClientLandUseDefinitionResource
from footprint.resources.feature_resources import FeatureResource
from footprint.resources.geography_resource import GeographyResource
from footprint.utils.dynamic_subclassing import get_dynamic_resource_class


class ScagExistingLandUseParcelFeatureResource(FeatureResource):

    """
        Resource representing SCAG's Existing Land Use parcel features
    """

    # TODO dynamically create this resource field specific to the client's LandUseDefinitionResource
    #land_use_definiton = ToOneField(ClientLandUseDefinitionResource, 'land_use_definiton', full=False, null=True)

    geography = ToOneField(GeographyResource, 'geography', full=True)
    census_block = ToOneField(CensusBlockResource, 'census_block', full=False, null=True, readonly=True)

    def dynamic_resource_class(self, params, feature_class):
        census_block_resource_class = CensusBlockResource().create_subclass(params,
                                                                            primary_base_feature_class=feature_class)
        land_use_definition_resource_class = ClientLandUseDefinitionResource().create_subclass(params)
        return get_dynamic_resource_class(
            self.__class__,
            feature_class,
            census_block=fields.ToOneField(census_block_resource_class, 'census_block', full=True, readonly=True,
                                           null=True),
            land_use_definition=ToOneField(land_use_definition_resource_class, 'land_use_definition', full=False,
                                           null=True)
        )

    def post_save(self, request, **kwargs):
        executePrimary(self.resolve_config_entity(kwargs['GET']))

    class Meta(FeatureResource.Meta):
        abstract = True
        # Override the limited fields of the FeatureResource to allow all fields through
        fields = []
        # Except for these fields
        excludes = FeatureResource.Meta.excludes
        always_return_data = False
        resource_name = 'existing_land_use_parcel'
        queryset = ScagExistingLandUseParcelFeature.objects.all() # Just for model_class initialization, should never be called


class ScagSpzFeatureResource(FeatureResource):
    """
        Resource representing SCAG SPZ
    """
    geography = ToOneField(GeographyResource, 'geography', full=True)

    def dynamic_resource_class(self, params, feature_class):
        return get_dynamic_resource_class(
            self.__class__,
            feature_class,
        )

    def post_save(self, request, **kwargs):
        executePrimary(self.resolve_config_entity(kwargs['GET']))

    class Meta(FeatureResource.Meta):
        abstract = True
        # Override the limited fields of the FeatureResource to allow all fields through
        fields = []
        # Except for these fields
        excludes = FeatureResource.Meta.excludes
        always_return_data = False
        resource_name = 'scag_primary_spz_feature'
        queryset = ScagPrimarySPZFeature.objects.all() # Just for model_class initialization, should never be called


class ScagGeneralPlanFeatureResource(FeatureResource):
    geography = ToOneField(GeographyResource, 'geography', full=True)

    def dynamic_resource_class(self, params, feature_class):

        land_use_definition_resource_class = ClientLandUseDefinitionResource().create_subclass(params)
        return get_dynamic_resource_class(
            self.__class__,
            feature_class,
            land_use_definition=ToOneField(land_use_definition_resource_class, 'land_use_definition', full=False,
                                           null=True)
        )

    def post_save(self, request, **kwargs):
        executePrimary(self.resolve_config_entity(kwargs['GET']))

    class Meta(FeatureResource.Meta):
        abstract = True
        # Override the limited fields of the FeatureResource to allow all fields through
        fields = []
        # Except for these fields
        excludes = FeatureResource.Meta.excludes
        always_return_data = False
        resource_name = 'scag_general_plan_feature'
        queryset = ScagGeneralPlanFeature.objects.all() # Just for model_class initialization, should never be called

