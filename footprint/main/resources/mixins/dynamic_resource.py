# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2013 Calthorpe Associates
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com

# Mixin that marks a resource class as needing dynamic subclassing because the model class it models needs dynamic subclassing

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from footprint.main.lib.functions import remove_keys, merge
from footprint.main.models import ConfigEntity, Layer
from footprint.main.models.config.scenario import FutureScenario, BaseScenario
from footprint.main.resources.footprint_resource import FootprintResource

class DynamicResource(FootprintResource):

    class Meta(FootprintResource.Meta):
        pass

    def create_subclass(self, params, **kwargs):
        """
            Returns a subclass of self based on the given parameters. For example a BaseFeatureResource will subclass
            itself based on the value of the 'config_entity_id' in params
        :param params:
        :return:
        """
        raise Exception("Must implement create_subclass in mixer")

    def resolve_config_entity(self, params):
        """
            Resolves the config_entity based on the layer id indicated in the param
        :param params:
        :return:
        """

        # TODO hack to handle lack of multi-level subclass relation resolution
        scenarios = FutureScenario.objects.filter(id=int(params['config_entity__id']))
        if len(list(scenarios)) > 0:
            # Scenario subclass instance
            return scenarios[0]
        else:
            scenarios = BaseScenario.objects.filter(id=int(params['config_entity__id']))
            if len(list(scenarios)) > 0:
                return scenarios[0]
            else:
                return ConfigEntity.objects.filter(id=int(params['config_entity__id'])).all().select_subclasses()[0]

    def resolve_layer(self, params):
        """
            The Layer id is used to resolve the type of Feature (via its DbEntity)
        :param params:
        :return:
        """
        return Layer.objects.get(id=params['layer__id'])

    def subclass_resource_if_needed(self, view, request):
        """
            Overrides the FootprintResource method to perform subclassing of the resource based on the request params
        :param view:
        :param request:
        :return:
        """
        params = request.GET
        # TODO cache dynamic class creation results
        # Create the dynamic resource class
        dynamic_resource_class = self.create_subclass(params, method=request.method)
        config_entity = self.resolve_config_entity(params)
        # This might not be need anymore, but it indicates what other dynamic classes were created so that
        # permissions can be added for them
        additional_classes_used = []
        # We add permissions to the current user so they can access these dynamic classes if it's the first access by the user
        # TODO permissions would ideally be done ahead of time, of if we could automatically give the user full access to all. This might be fixed in the latest Django version
        # subclasses of a certain type, but I don't see how to do that in the Django docs
        user = self.resolve_user(params)
        self.add_permissions_to_user(user, self.get_or_create_permissions_for_class(dynamic_resource_class, additional_classes_used, config_entity))

        # Extract and add GET parameters
        request._config_entity = config_entity
        request._filters = remove_keys(
            merge(request.GET, self.search_params(params)),
            self.remove_params(params))

        return dynamic_resource_class().wrap_view(view)

    def search_params(self, params):
        """
        :param params
        :return: return the modified params_copy
        """
        return {}

    def remove_params(self, params):
        """
        :return: a string list of parameters to remove
        """
        return []

    def get_or_create_permissions_for_class(self, DynamicResourceClass, additional_classes_used, config_entity):
        model_class = DynamicResourceClass.Meta.object_class
        for clazz in [model_class] + additional_classes_used:
            return map(lambda action: Permission.objects.get_or_create(
                codename='{0}_{1}'.format(action, clazz.__name__.lower()),
                # Since our dynamic model doesn't have a ContentType, borrow that of the ConfigEntity
                content_type_id=ContentType.objects.get(app_label="main", model=config_entity.__class__.__name__.lower()).id,
                name='Can {0} {1}'.format(action, clazz.__name__))[0],
                       ['add', 'change', 'delete'])

    def add_permissions_to_user(self, user , permissions):
        existing = user.user_permissions.all()
        new_permissions = filter(lambda permission: permission not in existing, permissions)
        user.user_permissions.add(*new_permissions)
