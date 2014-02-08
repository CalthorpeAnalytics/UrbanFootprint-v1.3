# urbanfootprint-california (v1.0), land use scenario development and modeling system.
# 
# Copyright
# (C) 2012 Calthorpe Associates
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

from django.conf.urls import include, url, patterns
from django.views.generic.simple import direct_to_template

from tastypie.api import Api
from footprint.initialization.fixtures.client.sacog.resource.sacog_resource import SacogStreamFeatureResource, SacogWetlandFeatureResource, SacogVernalPoolFeatureResource, SacogExistingLandUseParcelFeatureResource
from footprint.initialization.fixtures.client.scag__irvine.resource.scag__irvine_resource import ScagExistingLandUseParcelFeatureResource, ScagGeneralPlanFeatureResource, ScagSpzFeatureResource
from footprint.publishing.data_export import export_layer, export_scenario, get_export_result
from footprint.resources.analytic_resources import CoreResource
from footprint.resources.base_resources import BaseFeatureResource, BaseParcelFeatureResource, CpadHoldingsFeatureResource
from footprint.resources.built_form_resources import BuiltFormResource, BuiltFormSetResource, PlacetypeResource, \
    PlacetypeComponentResource, BuildingResource, BuildingTypeResource, BuildingUseDefinitionResource, \
    BuildingUsePercentResource, BuildingAttributeSetResource, BuildingPercentResource, BuiltFormExampleResource
from footprint.resources.category_resource import CategoryResource
from footprint.resources.client.client_land_use_definition_resource import ClientLandUseDefinitionResource


from footprint.resources.config_entity_resources import GlobalConfigResource, RegionResource, ProjectResource, ScenarioResource, ConfigEntityResource, FutureScenarioResource, BaseScenarioResource
from footprint.resources.db_entity_resources import DbEntityResource, DbEntityInterestResource, InterestResource
from footprint.resources.flat_built_form_resource import FlatBuiltFormResource
from footprint.resources.future_resources import FutureScenarioFeatureResource, EndStateFeatureResource, IncrementFeatureResource
from footprint.resources.layer_resources import LayerResource, LayerSelectionResource, LayerLibraryResource
from footprint.resources.medium_resources import MediumResource
from footprint.resources.policy_resources import PolicyResource, PolicySetResource
from footprint.resources.presentation_resources import PresentationResource, PresentationMediumResource
from footprint.resources.result_resources import ResultLibraryResource, ResultResource
from footprint.resources.tag_resource import TagResource
from footprint.resources.user_resource import UserResource
from footprint.tilestache_views import tilestache_tiles

from views import api_authentication

from settings import API_VERSION

future_scenario_feature = FutureScenarioFeatureResource()

urlpatterns = patterns(
    '',
    url(r'^$', direct_to_template, {'template': 'footprint/index.html'}),
    url(r'^api_authentication$', api_authentication),
    url(r'^(?P<api_key>[^/]+)/export_layer/(?P<layer_id>[^/]+)', export_layer),
    url(r'^(?P<api_key>[^/]+)/get_export_result/(?P<hash_id>[^/]+)', get_export_result),

    url(r'^export_scenario/(?P<scenario_id>[^/])', export_scenario),

    url(r'^tiles/(?P<layer_name>[^/]+)/(?P<z>[^/]+)/(?P<x>[^/]+)/(?P<y>[^/]+)\.(?P<extension>.+)$', tilestache_tiles,
        name='tiles_url'),
)


# All tastypie resources need to be listed here
v1_api = Api(api_name="v{0}".format(API_VERSION))
v1_api.register(UserResource())
v1_api.register(ConfigEntityResource())
v1_api.register(GlobalConfigResource())
v1_api.register(RegionResource())
v1_api.register(ProjectResource())
v1_api.register(ScenarioResource())
v1_api.register(FutureScenarioResource())
v1_api.register(BaseScenarioResource())
v1_api.register(DbEntityResource())
v1_api.register(DbEntityInterestResource())
v1_api.register(InterestResource())
v1_api.register(BuiltFormSetResource())
v1_api.register(BuiltFormExampleResource())
v1_api.register(BuiltFormResource())
v1_api.register(PlacetypeResource())
v1_api.register(PlacetypeComponentResource())
v1_api.register(BuildingResource())
v1_api.register(BuildingTypeResource())
v1_api.register(BuildingUseDefinitionResource())
v1_api.register(BuildingUsePercentResource())
v1_api.register(BuildingAttributeSetResource())
v1_api.register(BuildingPercentResource())

v1_api.register(PolicyResource())
v1_api.register(PolicySetResource())

v1_api.register(PresentationResource())
v1_api.register(LayerLibraryResource())
v1_api.register(ResultLibraryResource())

v1_api.register(MediumResource())

v1_api.register(PresentationMediumResource())
v1_api.register(LayerResource())
v1_api.register(LayerSelectionResource())

v1_api.register(ResultResource())

v1_api.register(CategoryResource())
v1_api.register(TagResource())
v1_api.register(CoreResource())

#Built Form Resources
v1_api.register(ClientLandUseDefinitionResource())
v1_api.register(FlatBuiltFormResource())

#Default layer resources
v1_api.register(EndStateFeatureResource())
v1_api.register(IncrementFeatureResource())
v1_api.register(FutureScenarioFeatureResource())
v1_api.register(BaseFeatureResource())
v1_api.register(BaseParcelFeatureResource())
v1_api.register(CpadHoldingsFeatureResource())

#SACOG specfic layer resources
v1_api.register(SacogExistingLandUseParcelFeatureResource())
v1_api.register(SacogVernalPoolFeatureResource())
v1_api.register(SacogWetlandFeatureResource())
v1_api.register(SacogStreamFeatureResource())

#SCAG Irvine pilot specific layer resources
v1_api.register(ScagExistingLandUseParcelFeatureResource())
v1_api.register(ScagGeneralPlanFeatureResource())
v1_api.register(ScagSpzFeatureResource())





# Django Rest API
urlpatterns += patterns(
    '',
    (r'^api/', include(v1_api.urls)),
)

# Cross-domain proxying if we need it
#urlpatterns += patterns('',
#    (r'^(?P<url>.*)$', 'httpproxy.views.proxy'),
#)
#urlpatterns += staticfiles_urlpatterns() #this is meant for debug only

#from celery.task import PingTask
#from djcelery import views as celery_views

#celery webhook
#urlpatterns += patterns("",
#    url(r'^apply/(?P<task_name>.+?)/', celery_views.apply),
#    url(r'^ping/', celery_views.task_view(PingTask)),
#    url(r'^(?P<task_id>[\w\d\-]+)/done/?$', celery_views.is_task_successful,
#        name="celery-is_task_successful"),
#    url(r'^(?P<task_id>[\w\d\-]+)/status/?$', celery_views.task_status,
#        name="celery-task_status"),
#)
