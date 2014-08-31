# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2014 Calthorpe Associates
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
from footprint.client.configuration.utils import resolve_fixture_class
from footprint.main.models import ConfigEntity
from footprint.main.models.built_form.client_land_use_definition import ClientLandUseDefinition
from footprint.main.resources.mixins.dynamic_resource import DynamicResource
from footprint.main.utils.dynamic_subclassing import get_dynamic_resource_class
from footprint import settings


class ClientLandUseDefinitionResource(DynamicResource):
    """
        This is an abstract resource class. A client specific resource subclass is created by dynamic_resource_class
    """

    class Meta(DynamicResource.Meta):
        abstract = True,
        always_return_data = False
        resource_name = 'client_land_use_definition'
        queryset = ClientLandUseDefinition.objects.all()

    def create_subclass(self, params, **kwargs):
        land_use_definition_fixture_class = resolve_fixture_class(
            "built_form",
            "land_use_definition",
            ClientLandUseDefinition,
            settings.CLIENT)

        return get_dynamic_resource_class(
            self.__class__,
            land_use_definition_fixture_class)

    def resolve_config_entity(self, params):
        """
        :param params.config_entity: The id of the config_entity
        :return: The subclassed ConfigEntity instanced based on the param value
        """
        return ConfigEntity.objects.filter(id=int(params['config_entity__id'])).all().select_subclasses()[0]
