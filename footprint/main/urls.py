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

from tastypie.api import Api
from footprint.main.publishing.data_export_publishing import export_layer, get_export_result
from footprint.main.resources.analysis_module_resource import AnalysisModuleResource
from footprint.main.resources.analysis_tool_resource import AnalysisToolResource
from footprint.main.resources.behavior_resources import BehaviorResource, FeatureBehaviorResource, IntersectionResource
from footprint.main.resources.built_form_resources import BuiltFormResource, BuiltFormSetResource, PlacetypeResource, \
    PlacetypeComponentResource, BuildingUseDefinitionResource, \
    BuildingUsePercentResource, BuildingAttributeSetResource, BuiltFormExampleResource, \
    PlacetypeComponentPercentResource, PrimaryComponentResource, PrimaryComponentPercentResource, \
    PlacetypeComponentCategoryResource, BuildingResource, BuildingTypeResource, UrbanPlacetypeResource, CropResource, \
    CropTypeResource, LandscapeTypeResource, AgricultureAttributeSetResource

from footprint.main.resources.category_resource import CategoryResource
from footprint.main.resources.client.client_land_use_definition_resource import ClientLandUseDefinitionResource


from footprint.main.resources.config_entity_resources import GlobalConfigResource, RegionResource, ProjectResource, \
    ScenarioResource, ConfigEntityResource, FutureScenarioResource, BaseScenarioResource
from footprint.main.resources.db_entity_resources import DbEntityResource, DbEntityInterestResource, InterestResource
from footprint.main.resources.environmental_constraint_resources import EnvironmentalConstraintUpdaterToolResource, \
    EnvironmentalConstraintPercentResource

from footprint.main.resources.feature_resources import FeatureResource, PaintingFeatureResource
from footprint.main.resources.flat_built_form_resource import FlatBuiltFormResource
from footprint.main.resources.layer_resources import LayerResource, LayerLibraryResource
from footprint.main.resources.layer_selection_resource import LayerSelectionResource
from footprint.main.resources.medium_resources import MediumResource
from footprint.main.resources.policy_resources import PolicyResource, PolicySetResource
from footprint.main.resources.presentation_medium_resource import PresentationMediumResource
from footprint.main.resources.presentation_resources import PresentationResource
from footprint.main.resources.result_resources import ResultLibraryResource, ResultResource
from footprint.main.resources.tag_resource import TagResource
from footprint.main.resources.user_resource import UserResource
from footprint.main.tilestache_views import tilestache_tiles
from footprint.main.views import upload

from django.views.generic import TemplateView
from django.conf import settings

urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name='footprint/index.html')),
    url(r'^(?P<api_key>[^/]+)/export_layer/(?P<layer_id>[^/]+)', export_layer),
    url(r'^(?P<api_key>[^/]+)/get_export_result/(?P<hash_id>[^/]+)', get_export_result),

    url(r'^tiles/(?P<layer_name>[^/]+)/(?P<z>[^/]+)/(?P<x>[^/]+)/(?P<y>[^/]+)\.(?P<extension>.+)$', tilestache_tiles,
        name='tiles_url'),
    url(r'^upload/.*', upload),
)


# All tastypie resources need to be listed here
v1_api = Api(api_name="v{0}".format(settings.API_VERSION))
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


v1_api.register(PlacetypeResource())
v1_api.register(PlacetypeComponentResource())
v1_api.register(PlacetypeComponentCategoryResource())
v1_api.register(PlacetypeComponentPercentResource())
v1_api.register(PrimaryComponentResource())
v1_api.register(PrimaryComponentPercentResource())

v1_api.register(BuildingUseDefinitionResource())
v1_api.register(BuildingUsePercentResource())
v1_api.register(BuildingAttributeSetResource())
v1_api.register(BuiltFormSetResource())
v1_api.register(BuiltFormExampleResource())
v1_api.register(BuiltFormResource())

v1_api.register(EnvironmentalConstraintUpdaterToolResource())
v1_api.register(EnvironmentalConstraintPercentResource())

v1_api.register(BuildingResource())
v1_api.register(BuildingTypeResource())
v1_api.register(UrbanPlacetypeResource())

v1_api.register(AgricultureAttributeSetResource())
v1_api.register(CropResource())
v1_api.register(CropTypeResource())
v1_api.register(LandscapeTypeResource())

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

#Built Form Resources
v1_api.register(ClientLandUseDefinitionResource())
v1_api.register(FlatBuiltFormResource())

v1_api.register(FeatureResource())
v1_api.register(PaintingFeatureResource())
v1_api.register(AnalysisModuleResource())
v1_api.register(AnalysisToolResource())
v1_api.register(FeatureBehaviorResource())
v1_api.register(IntersectionResource())
v1_api.register(BehaviorResource())

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
