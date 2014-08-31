from django.db import models
from footprint.main.lib.functions import remove_keys
from footprint.main.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.main.mixins.tags import Tags
from footprint.main.models.geospatial.db_entity import DbEntity
from footprint.main.models.geospatial.behavior import Behavior
from footprint.main.models.geospatial.intersection import Intersection
from footprint.main.models.tag import Tag

__author__ = 'calthorpe'

class FeatureBehavior(Tags):
    """
        Associated to a single DbEntity OneToOne and associates to a Behavior.
        Behavior defines the function of the DbEntity's features

        FeatureBehavior also has configuration properties that are populated from
        a the behavior.template_feature_behavior and then customized for the DbEntity

        self.db_entity can be used to access the DbEntity
    """

    # FeatureBehavior is a wrapper to Behavior that allows a DbEntity to associate
    # indirectly to a Behavior. The behavior defines a template which is used to create
    # an instance of the FeatureBehavior for use by the DbEntity
    # For behavior.teamplate_feature_behavior instances, the behavior is the owning behavior
    behavior = models.ForeignKey(Behavior, null=False)
    # The DbEntity of the FeatureBehavior. Only null temporarily when being hydrate by Tastypie during a DbEntity save
    db_entity = models.ForeignKey(DbEntity, null=True)

    # Set true for instances that are used as a template by Behavior (see Behavior.template_feature_behavior)
    is_template = models.BooleanField(default=False)
    # Indicates if the features are editable. Normally leave this alone
    # and let that of the Behavior take care of it
    readonly = models.BooleanField(default=False)

    # Adds intersection information specific to the DbEntity. The intersection type is normally specified
    # in the Behavior.intersection dict. So whatever is set here is merged with the dict of the Behavior
    intersection = models.ForeignKey(Intersection, null=True)

    def __init__(self, *args, **kwargs):
        super(FeatureBehavior, self).__init__(*args, **remove_keys(kwargs, ['tags']))
        self._tags = self._tags or []
        self._tags.extend(kwargs.get('tags', []))

    @property
    def computed_readonly(self):
        return self.readonly or self.behavior.readonly

    def set_defaults(self):
        """
            Sets defaults for FeatureBehavior instances created from a Behavior template or when updating
            after a configuration change.
            Override when subclassing FeatureBehavior to set default values
        """

        self.intersection = self.intersection or self.behavior.intersection
        self.readonly = self.readonly or self.behavior.readonly

    _tags = None

    def update_or_create_associations(self, feature_behavior):
        if feature_behavior._tags:
            self.tags.clear()
            self.tags.add(*map(lambda tag: Tag.objects.update_or_create(tag=tag.tag)[0], feature_behavior._tags))

    _no_post_save_publishing = False
    objects = GeoInheritanceManager()
    class Meta(object):
        abstract = False
        app_label = 'main'
