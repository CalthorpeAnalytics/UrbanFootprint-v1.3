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
from tastypie.fields import DictField, NOT_PROVIDED
from footprint.lib.functions import map_dict_to_dict, deep_copy_dict_structure

__author__ = 'calthorpe'

class ModelDictField(DictField):

    def resolve_resource_field(self, *keys):
        return self._resource.base_fields.get(keys[0], self.resolve_resource_field(*keys[1:]) if len(keys)>1 else None)

    def key_dehydrate_override(self):
        """
            Override this method to create mapping from a model class dict key to different dehydrated object key. This is used for instance to map 'db_entities' to 'db_entity_interests' because the ConfigEntity resource class wants to present selects as DbEntityInterests
        :return:
        """
        return {}

    def key_hydrate_override(self):
        """
            Override this method to create mapping from a model class dict key to different dehydrated object key. This is used for instance to map 'db_entities' to 'db_entity_interests' because the ConfigEntity resource class wants to present selects as DbEntityInterests
        :return:
        """
        return {}

    def instance_dehydrate_override(self):
        """
            Overrides instances of the model class dict. Specify functions by dict key that map the instance to a new value. The function receives the bundle.obj and the object of the key. For instance {'db_entities':lambda config_entity, db_entity: db_entity_interest_of_db_entity(db_entity) }
        :return:
        """
        return {}

    def instance_hydrate_override(self):
        """
            Overrides instances of the model class dict. Specify functions by dict key that map the instance to a new value. The function receives the bundle.obj and the object of the key. For instance {'db_entities':lambda config_entity, db_entity: db_entity_interest_of_db_entity(db_entity) }
        :return:
        """
        return {}

    def dehydrate(self, bundle):
        """
            Handles the selections dict. This could be generalized into a custom field that handles a dictionary of assorted model instances and converts each one to a resource URI
        :param bundle:
        :return:
        """

        # Deep copy the structure to create new dict instance so we don't mutilate the source
        value = deep_copy_dict_structure(super(ModelDictField, self).dehydrate(bundle))

        # TODO this should handle arbitrary depth, not just 2D
        for outer_key, dct in (value or {}).items():
            updated_outer_key = self.key_dehydrate_override().get(outer_key, outer_key)
            if (updated_outer_key != outer_key):
                del value[outer_key]
                value[updated_outer_key] = {}
            # Each inner key value is a model instance that is to be dehydrated to a resource_uri
            for key, model_instance in dct.items():
                updated_key = self.key_dehydrate_override().get(key, key)
                updated_model_instance = self.instance_dehydrate_override().get(updated_outer_key, lambda x,y: model_instance)(bundle.obj, model_instance)
                field = self.resolve_resource_field(updated_outer_key, updated_key)
                field_resource = field.to_class()
                if (updated_key != key):
                    del value[key]
                    value[updated_key] = {}
                value[updated_outer_key][updated_key] = field_resource.dehydrate_resource_uri(updated_model_instance)
        return value

    def hydrate(self, bundle):
        """
            Hydrates a dict of resource URI to the corresponding instances by resolving the URIs. Like dehydrate_selections, this could be generalized
        :param bundle:
        :return:
        """
        value = super(ModelDictField, self).hydrate(bundle)

        # Fill the dehydrated bundle for each outer key
        for outer_key, dct in (value or {}).items():
            updated_outer_key = self.key_hydrate_override().get(outer_key, outer_key)
            if (updated_outer_key != outer_key):
                del value[outer_key]
                value[updated_outer_key] = {}
            # Each inner key value is a resource uri that is to be hydrated to an instance
            for key, resource_uri in dct.items():
                updated_key = self.key_hydrate_override().get(key, key)
                field = self.resolve_resource_field(outer_key, key)
                field_resource = field.to_class()
                if (updated_key != key):
                    del value[key]
                    value[updated_key] = {}
                model_instance = field_resource.get_via_uri(resource_uri, bundle.request)
                updated_instance = self.instance_hydrate_override().get(updated_outer_key, lambda x,y: model_instance)(bundle.obj, model_instance)
                value[updated_outer_key][updated_key] = updated_instance
        return value
