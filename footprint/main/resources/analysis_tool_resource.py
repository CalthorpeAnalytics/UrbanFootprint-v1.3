from tastypie.constants import ALL_WITH_RELATIONS
from tastypie.fields import ToOneField
from footprint.main.models.analysis_module.analysis_tool import AnalysisTool
from footprint.main.resources.behavior_resources import BehaviorResource
from footprint.main.resources.config_entity_resources import ConfigEntityResource
from footprint.main.resources.footprint_resource import FootprintResource
from footprint.main.resources.mixins.dynamic_resource import DynamicResource

__author__ = 'calthorpe'

class AnalysisToolResource(FootprintResource):

    config_entity = ToOneField(ConfigEntityResource, attribute='config_entity', full=False, null=False)
    behavior = ToOneField(BehaviorResource, attribute='behavior', full=False, null=True)

    class Meta(FootprintResource.Meta):
        always_return_data = True,
        filtering = {
            "config_entity": ALL_WITH_RELATIONS
        }
        queryset = AnalysisTool.objects.all()
        resource_name = 'analysis_tool'
