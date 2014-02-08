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
from tastypie.constants import ALL_WITH_RELATIONS
from tastypie.fields import ToOneField
from footprint.main.models.analysis_module.vmt_module.vmt import Vmt
from footprint.main.models.analysis_module.core_module.core import Core
from footprint.main.models.analysis_module.fiscal_module.fiscal import Fiscal
from footprint.main.resources.config_entity_resources import ConfigEntityResource
from footprint.main.resources.footprint_resource import FootprintResource
from footprint.main.resources.user_resource import UserResource

__author__ = 'calthorpe_associates'

class AnalysisModuleResource(FootprintResource):
    config_entity = ToOneField(ConfigEntityResource, attribute='config_entity', full=False, null=False)
    user = fields.ToOneField(UserResource, 'user', readonly=True, full=False)

    def hydrate(self, bundle):
        """
            Hydrate indicates the desire to run the AnalysisModule
        :param bundle:
        :return:
        """
        self.user = self.resolve_user(bundle.request.GET)
        if bundle.data.start:
            # Start the analysis module
            bundle.obj.start()

    class Meta(FootprintResource.Meta):
        abstract = True
        always_return_data = True
        filtering = {
            "config_entity": ALL_WITH_RELATIONS
        }

class CoreResource(AnalysisModuleResource):

    class Meta(AnalysisModuleResource.Meta):
        abstract = False
        queryset = Core.objects.all()


class FiscalResource(AnalysisModuleResource):

    class Meta(AnalysisModuleResource.Meta):
        abstract = False
        queryset = Fiscal.objects.all()

class VmtResource(AnalysisModuleResource):

    class Meta(AnalysisModuleResource.Meta):
        abstract = False
        queryset = Vmt.objects.all()