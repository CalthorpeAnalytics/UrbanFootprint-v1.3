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
from tastypie.constants import ALL_WITH_RELATIONS
from tastypie.fields import ToOneField, CharField, DateField, ToManyField
from footprint.main.models import AnalysisModule
from footprint.main.resources.analysis_tool_resource import AnalysisToolResource
from footprint.main.resources.footprint_resource import FootprintResource

__author__ = 'calthorpe_associates'

class AnalysisModuleResource(FootprintResource):

    config_entity = ToOneField('footprint.main.resources.config_entity_resources.ConfigEntityResource', attribute='config_entity', full=False, null=False, readonly=True)
    analysis_tools = ToManyField(AnalysisToolResource, attribute='analysis_tools', full=True)

    started = DateField(readonly=True)
    completed = DateField(readonly=True)
    failed = DateField(readonly=True)

    class Meta(FootprintResource.Meta):
        always_return_data = True,
        excludes = ('creator', 'updater')
        filtering = {
            "config_entity": ALL_WITH_RELATIONS
        }
        queryset = AnalysisModule.objects.all()
        resource_name = 'analysis_module'

    def hydrate(self, bundle):
        if not bundle.obj.id:
            bundle.obj.creator = self.resolve_user(bundle.request.GET)
        bundle.obj.updater = self.resolve_user(bundle.request.GET)
        return bundle
