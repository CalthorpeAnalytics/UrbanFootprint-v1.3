# coding=utf-8


__author__ = 'calthorpe_associates'

from footprint.main.models.built_form.built_form import BuiltForm
from footprint.main.models.built_form.infrastructure_attributes import InfrastructureAttributeSet
class Infrastructure(InfrastructureAttributeSet, BuiltForm):
    """
        Infrastructure is the container for streets, parks, detention/utilities
    """

    class Meta(object):
        app_label = 'main'

    # Returns the string representation of the model.
    def __unicode__(self):
        return self.name
