# coding=utf-8
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
from django.db import models
from picklefield import PickledObjectField
from footprint.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.mixins.key import Key
from footprint.mixins.scoped_key import ScopedKey
from footprint.mixins.shared_key import SharedKey
from footprint.mixins.tags import Tags
from footprint.mixins.name import Name

__author__ = 'calthorpe'

class Policy(Key, Name, Tags):
    """
        A Policy is a loosely defined data structure. That represents a policy of a policy set. Policies may be shared across sets. Their semantic meaning may be determined by their shared key and they may be categorized by their tags. A policy has a range of possible values, anything from True/False to a number range or anything else that can be selected and have meaning. The range is serialized by the values attribute. Classes that have PolicySet attributes, namely ConfigEntity instances, should store the actual selected value of each Policy in a separate data structure ConfigEntity instances store policy settings in ConfigEntity.selections.policy_sets. See that attribute to understand how policy value selections are stored.

    """
    objects = GeoInheritanceManager()
    policies = models.ManyToManyField('Policy', default=lambda: [])
    # Pickle the set of values into a single string field
    # The allowed values of the policy. This should be anything that can be serialized and represented on the client
    values = PickledObjectField()

    class Meta(object):
        app_label = 'footprint'

