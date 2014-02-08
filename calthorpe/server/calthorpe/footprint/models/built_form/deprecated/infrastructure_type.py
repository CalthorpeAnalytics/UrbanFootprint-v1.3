# coding=utf-8
from footprint.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.models.built_form.placetype_component import PlacetypeComponent
from footprint.models.built_form.infrastructure_attributes import InfrastructureAttributeSet
from footprint.models.built_form.infrastructure import Infrastructure
from django.db import models
__author__ = 'calthorpe'

class InfrastructureType(PlacetypeComponent, InfrastructureAttributeSet):
    """
        Infrastructure is the container for streets, parks, detention/utilities
    """
    objects = GeoInheritanceManager()

    infrastructures = models.ManyToManyField(Infrastructure, through='InfrastructurePercent')

    def get_component_field(self):
        return self.infrastructures

    class Meta(object):
        app_label = 'footprint'

    # Returns the string representation of the model.
    def __unicode__(self):
        return self.name
