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
from footprint.main.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.main.mixins.key import Key
from footprint.main.mixins.scoped_key import ScopedKey
from footprint.main.mixins.shared_key import SharedKey
from footprint.main.mixins.tags import Tags
from footprint.main.mixins.name import Name
from footprint.main.models.config.model_pickled_object_field import ModelPickledObjectField

__author__ = 'calthorpe_associates'

class PolicyLookup(object):
    def policy_by_key(self, key_path):
        """
            Retrieve a policy by key path. Recurses into the policies to match the given path.
        :param key_path:
        :return: The matching policy value or none
        """
        keys = key_path.split('.') if key_path else []

        if len(keys) == 0:
            # The path resolved to a policy or policy_set
            return self

        # Try to find a policy that matches the first key
        child_policies = self.policies.filter(key=keys[0])
        if len(child_policies) != 1:
            # If not found
            if len(keys) == 1:
                # Try to find a value that matches the key
                return self.values.get(keys[0], None)
            return None
        # If found, recurse on the remaining keys
        return child_policies[0].policy_by_key('.'.join(keys[1:]))

class Policy(SharedKey, Name, Tags, PolicyLookup):
    """
        A Policy is a loosely defined data structure. That represents a policy of a policy set. Policies may be shared across sets. Their semantic meaning may be determined by their shared key and they may be categorized by their tags. A policy has a range of possible values, anything from True/False to a number range or anything else that can be selected and have meaning. The range is serialized by the values attribute. Classes that have PolicySet attributes, namely ConfigEntity instances, should store the actual selected value of each Policy in a separate data structure ConfigEntity instances store policy settings in ConfigEntity.selections.policy_sets. See that attribute to understand how policy value selections are stored.

    """
    schema = models.CharField(max_length=100, null=True)
    objects = GeoInheritanceManager()
    policies = models.ManyToManyField('Policy', default=lambda: [])
    # Pickle the set of values into a single string field
    # The allowed values of the policy. This should be anything that can be serialized and represented on the client
    values = PickledObjectField()

    def update_or_create_policy(self, policy_config):
        child_policy = Policy.objects.update_or_create(
            key=policy_config['key'],
            schema='%s__%s' % (self.schema, policy_config['key']) if self.schema else policy_config['key'],
            defaults=dict(
                name=policy_config['name'],
                description=policy_config.get('description', None),
                values=policy_config.   get('values', {})
            ))[0]
        if policy_config.get('policies', None) and len(policy_config['policies']) > 0:
            child_policy.policies.add(*map(lambda child_policy_config:
                                           child_policy.update_or_create_policy(child_policy_config), policy_config['policies']))
        return child_policy


    class Meta(object):
        app_label = 'main'

