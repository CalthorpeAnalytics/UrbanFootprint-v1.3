# coding=utf-8
__author__ = 'calthorpe_associates'

from django.db.models.signals import post_save
from django.db.models import Sum
from footprint.main.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.main.models.built_form.built_form import BuiltForm

class PrimaryComponent(BuiltForm):
    """
        Building represents a template building, such as a Rural Community College
    """
    objects = GeoInheritanceManager()

    class Meta(object):
    # This is not abstract so that django can form a many-to-many relationship with it in built_form_set
        app_label = 'main'

    def get_parent_field(self):
        return self.placetypecomponent_set


def on_instance_modify(sender, **kwargs):
    instance = kwargs['instance']
    for parent_object in instance.get_parent_field().all():
        if parent_object.primarycomponentpercent_set.all().aggregate(Sum('percent')) > .95:
            parent_object.aggregate_built_form_attributes()
        else:
            pass

post_save.connect(on_instance_modify, sender=PrimaryComponent)
