from tastypie.fields import ToManyField, ToOneField, ListField
from footprint.main.models import Behavior, FeatureBehavior
from footprint.main.models.geospatial.intersection import Intersection
from footprint.main.resources.footprint_resource import FootprintResource
from footprint.main.resources.tag_resource import TagResource

__author__ = 'calthorpe'


class IntersectionResource(FootprintResource):
    class Meta(FootprintResource.Meta):
        queryset = Intersection.objects.filter()

class BehaviorResource(FootprintResource):
    parents = ToManyField('self', attribute='parents', null=False)
    tags = ToManyField(TagResource, attribute='tags', full=True, null=True)
    computed_tags = ToManyField(TagResource, attribute='computed_tags', full=True, null=True)
    intersection = ToOneField(IntersectionResource, attribute='intersection', null=True)

    class Meta(FootprintResource.Meta):
        queryset = Behavior.objects.filter(deleted=False)

class FeatureBehaviorResource(FootprintResource):
    behavior = ToOneField(BehaviorResource, attribute='behavior', null=False)
    db_entity = ToOneField('footprint.main.resources.db_entity_resources.DbEntityResource', attribute='db_entity', null=True)
    tags = ToManyField(TagResource, attribute='tags', full=True, null=True)
    intersection = ToOneField(IntersectionResource, attribute='intersection', null=True)

    class Meta(FootprintResource.Meta):
        queryset = FeatureBehavior.objects.filter(is_template=False)
        resource_name= 'feature_behavior'

