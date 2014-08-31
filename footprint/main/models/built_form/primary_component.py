# coding=utf-8
__author__ = 'calthorpe_associates'

from django.db.models.signals import post_save
from django.db.models import Sum
from django.db import models
from footprint.main.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.main.models.built_form.built_form import BuiltForm
import logging
logger = logging.getLogger(__name__)


class PrimaryComponent(BuiltForm):
    """
        primary component represents a template primary input to built form, such as a Rural Community College or a
        tomato crop
    """
    objects = GeoInheritanceManager()

    class Meta(object):
    # This is not abstract so that django can form a many-to-many relationship with it in built_form_set
        app_label = 'main'

    def get_aggregates_field(self):
        return self.placetypecomponent_set

    def get_aggregate_built_forms(self):
        return self.placetypecomponent_set.all()
