# coding=utf-8
from footprint.managers.geo_inheritance_manager import GeoInheritanceManager

__author__ = 'calthorpe'

__author__ = 'calthorpe'

from footprint.mixins.name import Name

__author__ = 'calthorpe'

class BuildingtypeCategory(Name):
    """
        BuildingUseDefinition describes the possible general types of uses for a building
    """
    objects = GeoInheritanceManager()


    class Meta(object):
        app_label = 'footprint'
