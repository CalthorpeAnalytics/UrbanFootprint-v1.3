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
from tastypie.fields import ToManyField
from tastypie.resources import ModelResource
from footprint.main.models.config.policy_set import PolicySet
from footprint.main.models.config.policy import Policy
from footprint.main.resources.footprint_resource import FootprintResource
from footprint.main.resources.tag_resource import TagResource

__author__ = 'calthorpe_associates'

class PolicyResource(FootprintResource):
    policies = ToManyField('self', 'policies', full=True)
    tags = ToManyField(TagResource, 'tags', full=True)
    class Meta:
        always_return_data = True
        queryset = Policy.objects.all()

class PolicySetResource(ModelResource):
    policies = ToManyField(PolicyResource, 'policies', full=True)

    class Meta:
        always_return_data = True
        queryset = PolicySet.objects.all()
        resource_name = 'policy_set'

