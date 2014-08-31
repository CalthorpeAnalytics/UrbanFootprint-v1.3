from tastypie.constants import ALL
from tastypie.fields import CharField
from footprint.main.models import EnvironmentalConstraintUpdaterTool
from footprint.main.models.analysis_module.environmental_constraint_module.environmental_constraint_percent import \
    EnvironmentalConstraintPercent
from footprint.main.resources.analysis_module_resource import AnalysisToolResource
from footprint.main.resources.config_entity_resources import ConfigEntityResource
from footprint.main.resources.db_entity_resources import DbEntityResource
from footprint.main.resources.footprint_resource import FootprintResource
from tastypie import fields
from footprint.main.resources.mixins.mixins import ToManyCustomAddField

__author__ = 'calthorpe'


class EnvironmentalConstraintUpdaterToolResource(AnalysisToolResource):

    def add_environmental_constraint_percents(bundle, *environmental_constraint_percents):
        for environmental_constraint_percent in environmental_constraint_percents:
            environmental_constraint_percent.save()

    def remove_environmental_constraint_percents(bundle, *environmental_constraint_percents):
        for environmental_constraint_percent in environmental_constraint_percents:
            environmental_constraint_percent.delete()

    environmental_constraint_percent_query = lambda bundle: bundle.obj.environmentalconstraintpercent_set.all()
    environmental_constraint_percents = ToManyCustomAddField(
        'footprint.main.resources.environmental_constraint_resources.EnvironmentalConstraintPercentResource',
        attribute=environmental_constraint_percent_query,
        add=add_environmental_constraint_percents,
        remove=add_environmental_constraint_percents,
        full=True,
        null=True)

    class Meta(AnalysisToolResource.Meta):
        queryset = EnvironmentalConstraintUpdaterTool.objects.all()
        resource_name = 'environmental_constraint_updater_tool'


class EnvironmentalConstraintPercentResource(FootprintResource):

    db_entity = fields.ToOneField(DbEntityResource, 'db_entity', full=True, null=False)
    analysis_tool = fields.ToOneField(
        EnvironmentalConstraintUpdaterToolResource,
        'analysis_tool', full=False, null=False)

    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = EnvironmentalConstraintPercent.objects.all()
        resource_name = 'environmental_constraint_percent'