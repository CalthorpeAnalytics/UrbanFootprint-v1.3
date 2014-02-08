# coding=utf-8
from footprint.main.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.main.mixins.name import Name

__author__ = 'calthorpe_associates'

class BuildingtypeCategory(Name):
    """
        BuildingUseDefinition describes the possible general types of uses for a building
    """
    objects = GeoInheritanceManager()


    class Meta(object):
        app_label = 'main'
