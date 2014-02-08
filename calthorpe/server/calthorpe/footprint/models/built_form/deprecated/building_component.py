# coding=utf-8
__author__ = 'calthorpe'

from django.db import models


class BuildingComponent(models.Model):

    class Meta(object):
        abstract = True
        app_label = 'footprint'

    def on_instance_modify(sender, **kwargs):
        instance = kwargs['instance']
        for parent_object in instance.get_parent_field().all():
            if parent_object.primarycomponentpercent_set.all().aggregate(Sum('percent')) > .95:
                parent_object.aggregate_built_form_attributes()
            else:
                pass
