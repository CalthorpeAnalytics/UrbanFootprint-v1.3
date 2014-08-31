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
from tastypie.constants import ALL_WITH_RELATIONS, ALL
from tastypie.fields import CharField
from footprint.main.models import Project, Region, GlobalConfig, Scenario, ConfigEntity
from footprint.main.models.config.scenario import BaseScenario, FutureScenario
from footprint.main.resources.medium_resources import MediumResource
from footprint.main.resources.model_dict_field import ModelDictField
from footprint.main.resources.mixins.mixins import PolicySetsResourceMixin, BuiltFormSetsResourceMixin, DbEntityResourceMixin, PresentationResourceMixin, CategoryResourceMixin, \
    CloneableResourceMixin
from footprint.main.resources.footprint_resource import FootprintResource
from tastypie import fields

__author__ = 'calthorpe_associates'


class CustomModelDictField(ModelDictField):
    def key_dehydrate_override(self):
        return {'db_entities': 'db_entity_interests'}

    def instance_dehydrate_override(self):
        return {'db_entity_interests':
                lambda config_entity, db_entity: config_entity.dbentityinterest_set.filter(db_entity=db_entity)[0]
        }

    def key_hydrate_override(self):
        return {'db_entity_interests': 'db_entities'}

    def instance_hydrate_override(self):
        return {'db_entities': lambda config_entity, db_entity_interest: db_entity_interest.db_entity}


class ConfigEntityResource(FootprintResource, PolicySetsResourceMixin, BuiltFormSetsResourceMixin,
                           DbEntityResourceMixin, PresentationResourceMixin, CategoryResourceMixin, CloneableResourceMixin):

    media = fields.ToManyField(MediumResource, 'media', full=False, null=True)
    # Selections needs to be revisited, so it is readonly for now
    selections = CustomModelDictField(attribute='selections', null=False, blank=False, readonly=False)
    # These should never be written, they are calculated automatically
    schema = CharField(attribute='schema', readonly=True)
    scope = CharField(attribute='scope', readonly=True)

    def hydrate(self, bundle):
        """
            Set the user who created the ConfigEntity
        :param bundle:
        :return:
        """
        if not bundle.obj.id:
            bundle.obj.creator = self.resolve_user(bundle.request.GET)
        bundle.obj.updater = self.resolve_user(bundle.request.GET)
        return super(ConfigEntityResource, self).hydrate(bundle)


    class Meta(FootprintResource.Meta):
        abstract = True
        always_return_data = True
        queryset = ConfigEntity.objects.filter(deleted=False)
        resource_name = 'config_entity'
        filtering = {
            # Accept the parent_config_entity to limit the ConfigEntity instances to a certain id
            # (i.e. parent_config_entity__id=n)
            "parent_config_entity": ALL_WITH_RELATIONS,
            "id": ALL
        }


class GlobalConfigResource(ConfigEntityResource):
    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = GlobalConfig.objects.filter(deleted=False)
        resource_name = 'global_config'


class RegionResource(ConfigEntityResource):
    parent_config_entity = fields.ToOneField(ConfigEntityResource, 'parent_config_entity', full=False)

    class Meta(ConfigEntityResource.Meta):
        always_return_data = True
        queryset = Region.objects.filter(deleted=False)
        resource_name = 'region'


class ProjectResource(ConfigEntityResource):
    parent_config_entity = fields.ToOneField(RegionResource, 'parent_config_entity', full=False)

    class Meta(ConfigEntityResource.Meta):
        always_return_data = True
        queryset = Project.objects.filter(deleted=False)
        resource_name = 'project'


class ScenarioResource(ConfigEntityResource):
    parent_config_entity = fields.ToOneField(ProjectResource, 'parent_config_entity', full=False)

    class Meta(ConfigEntityResource.Meta):
        abstract = False
        always_return_data = True
        queryset = Scenario.objects.filter(deleted=False)
        resource_name = 'scenario'


class BaseScenarioResource(ScenarioResource):
    parent_config_entity = fields.ToOneField(ProjectResource, 'parent_config_entity', full=False)

    class Meta(ConfigEntityResource.Meta):
        always_return_data = True
        queryset = BaseScenario.objects.filter(deleted=False)
        resource_name = 'base_scenario'


class FutureScenarioResource(ScenarioResource):
    parent_config_entity = fields.ToOneField(ProjectResource, 'parent_config_entity', full=False)

    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = FutureScenario.objects.filter(deleted=False)
        resource_name = 'future_scenario'
