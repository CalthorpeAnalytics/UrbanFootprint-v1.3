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
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates.
# Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709.
# Phone: (510) 548-6800. Web: www.calthorpe.com
from footprint.main.lib.functions import remove_keys
from footprint.main.models import Medium
from footprint.main.resources.pickled_dict_field import PickledDictField
from footprint.main.resources.footprint_resource import FootprintResource

__author__ = 'calthorpe_associates'

class MediumResource(FootprintResource):
    content = PickledDictField(attribute='content', null=True, blank=True, default=lambda:{})

    # def dehydrate_content(self, bundle):
    #     # Remove data that isn't needed by the API
    #     return remove_keys(bundle.data['content'], ['attributes'])

    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = Medium.objects.all()
