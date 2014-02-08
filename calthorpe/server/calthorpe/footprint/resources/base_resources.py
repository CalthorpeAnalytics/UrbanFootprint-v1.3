# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2012 Calthorpe Associates
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
from footprint.models import CensusBlock, CensusBlockgroup
from footprint.models.analysis_module.core import executePrimary
from footprint.models.base.base_feature import BaseFeature
from footprint.models.base.base_parcel_feature import BaseParcelFeature
from footprint.models.base.cpad_holdings_feature import CpadHoldingsFeature
from footprint.models.base.developable_feature import DevelopableFeature
from footprint.resources.built_form_resources import BuiltFormResource
from footprint.resources.feature_resources import FeatureResource
from footprint.resources.geography_resource import GeographyResource
from footprint.resources.mixins.dynamic_resource import DynamicResource
from footprint.utils.dynamic_subclassing import get_dynamic_resource_class

__author__ = 'calthorpe'


class BaseFeatureResource(FeatureResource):
    built_form = ToOneField(BuiltFormResource, 'built_form', full=False, null=True)

    class Meta(FeatureResource.Meta):
        abstract = True
        # Override the limited fields of the FeatureResource to allow all fields through
        fields = []
        always_return_data = False
        resource_name = 'base_feature'
        # The following is set in the subclass based upon the dynamic model class passed into the class creator
        queryset = BaseFeature.objects.all() # Just for model_class initialization, should never be called


class BaseParcelFeatureResource(FeatureResource):
    built_form = ToOneField(BuiltFormResource, 'built_form', full=False, null=True)

    class Meta(FeatureResource.Meta):
        abstract = True
        # Override the limited fields of the FeatureResource to allow all fields through
        fields = []
        always_return_data = False
        resource_name = 'base_parcel_feature'
        # The following is set in the subclass based upon the dynamic model class passed into the class creator
        queryset = BaseParcelFeature.objects.all() # Just for model_class initialization, should never be called


class DevelopableFeatureResource(FeatureResource):
    class Meta(FeatureResource.Meta):
        abstract = True
        # Override the limited fields of the FeatureResource to allow all fields through
        fields = []
        always_return_data = False
        resource_name = 'developable_feature'
        # The following is set in the subclass based upon the dynamic model class passed into the class creator
        queryset = DevelopableFeature.objects.all() # Just for model_class initialization, should never be called


class CpadHoldingsFeatureResource(FeatureResource):

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
        resource_name = 'cpad_holdings_feature'
        queryset = CpadHoldingsFeature.objects.all() # Just for model_class initialization, should never be called



class CensusBlockgroupResource(DynamicResource):
    # TODO just bass the census_blockgroup_class instead
    def create_subclass(self, params, census_block_class=None, **kwargs):
        census_blockgroup_class = census_block_class.census_blockgroup.field.rel.to
        DynamicResourceClass = get_dynamic_resource_class(self.__class__, census_blockgroup_class)
        return DynamicResourceClass

    class Meta(DynamicResource.Meta):
        abstract = True
        queryset = CensusBlockgroup.objects.all()
        excludes = ['wkb_geometry']


class CensusBlockResource(DynamicResource):
    # TODO just bass the census_block_class instead
    def create_subclass(self, params, primary_base_feature_class=None, **kwargs):
        census_block_class = primary_base_feature_class.census_block.field.rel.to
        DynamicResourceClass = self.dynamic_resource_class(params, census_block_class)
        return DynamicResourceClass

    def dynamic_resource_class(self, params, census_block_class):
        census_blockgroup_resource_class = CensusBlockgroupResource().create_subclass(params,
                                                                                      census_block_class=census_block_class)
        return get_dynamic_resource_class(
            self.__class__,
            census_block_class,
            census_blockgroup=fields.ToOneField(census_blockgroup_resource_class, 'census_blockgroup', full=True,
                                                readonly=True, null=True))

    class Meta(DynamicResource.Meta):
        abstract = True
        queryset = CensusBlock.objects.all()
        excludes = ['wkb_geometry']