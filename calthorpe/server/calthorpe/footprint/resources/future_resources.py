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
from footprint.models import FutureScenarioFeature, CoreEndStateFeature, CoreIncrementFeature
from footprint.models.analysis_module.core import executeCore
from footprint.resources.built_form_resources import BuiltFormResource
from footprint.resources.feature_resources import FeatureResource

__author__ = 'calthorpe'


class FutureScenarioFeatureResource(FeatureResource):
    built_form = ToOneField(BuiltFormResource, 'built_form', full=False, null=True)

    def hydrate(self, bundle):
        bundle.obj.dirty = True
        return bundle

    def post_save(self, request, **kwargs):
        #TODO invalidate cache after painting
        executeCore(self.resolve_user(request.GET), self.resolve_config_entity(kwargs['GET']))

    class Meta(FeatureResource.Meta):
        abstract = True
        # Override the limited fields of the FeatureResource to allow all fields through
        fields = []
        always_return_data = False
        resource_name = 'future_scenario_feature'
        # The following is set in the subclass based upon the dynamic model class passed into the class creator
        queryset = FutureScenarioFeature.objects.all()

    def resource_uri_kwargs(self, bundle_or_obj=None):
        kwargs = super(FutureScenarioFeatureResource, self).resource_uri_kwargs(bundle_or_obj)
        kwargs['resource_name'] = FutureScenarioFeatureResource.Meta.resource_name
        return kwargs


class EndStateFeatureResource(FeatureResource):
    built_form = ToOneField(BuiltFormResource, 'built_form', full=False, null=True)

    class Meta(FeatureResource.Meta):
        abstract = True
        # Override the limited fields of the FeatureResource to allow all fields through
        fields = []
        always_return_data = False
        resource_name = 'end_state_feature'
        # The following is set in the subclass based upon the dynamic model class passed into the class creator
        queryset = CoreEndStateFeature.objects.all() # Just for model_class initialization, should never be called


class IncrementFeatureResource(FeatureResource):
    class Meta(FeatureResource.Meta):
        abstract = True
        # Override the limited fields of the FeatureResource to allow all fields through
        fields = []
        always_return_data = False
        resource_name = 'increment_feature'
        # The following is set in the subclass based upon the dynamic model class passed into the class creator
        queryset = CoreIncrementFeature.objects.all() # Just for model_class initialization, should never be called