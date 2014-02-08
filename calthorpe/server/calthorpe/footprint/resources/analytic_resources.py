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
from tastypie.fields import ToOneField
from tastypie.resources import ModelResource
from footprint.models.analysis_module.core import Core
from footprint.resources.config_entity_resources import ConfigEntityResource

__author__ = 'calthorpe'

class CoreResource(ModelResource):

    config_entity = ToOneField(ConfigEntityResource, attribute='config_entity', full=False, null=False)
    class Meta():
        always_return_data = False
        # TODO not sure what this should be
        queryset = Core.objects.all()
        resource_name = 'core'

    def hydrate(self, bundle):
        """
            Hydrate indicates the desire to run the AnalysisModule
        :param bundle:
        :return:
        """
        if bundle.data.start:
            # Start the analysis module
            bundle.obj.start()

