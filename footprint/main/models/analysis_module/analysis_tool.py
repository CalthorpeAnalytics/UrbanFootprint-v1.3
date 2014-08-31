from django.db import models
from django.db.models.signals import post_save
from footprint.main.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.main.mixins.shared_key import SharedKey
from footprint.main.models import Behavior
from footprint.main.models.keys.keys import Keys
from footprint.main.utils.subclasses import receiver_subclasses

__author__ = 'calthorpe'


class AnalysisTool(SharedKey):
    """
        Base class for Analysis Tools. AnalysisModules have many AnalysisTools
    """

    objects = GeoInheritanceManager()
    config_entity = models.ForeignKey('ConfigEntity', null=False)
    # This behavior determines what DbEntities the tool responds to when the former are created or updated
    behavior = models.ForeignKey(Behavior, null=True)

    _no_post_save_publishing = False

    class Meta(object):
        app_label = 'main'
        abstract = False


    def initialize(self, created):
        """
            Optional initializer called after the tool instance is created
        """
        pass

    def update(self, **kwargs):
        """
            Overridden by the subclass to run the tool when a dependency changes
        """
        pass

    @classmethod
    def pre_save(cls, user_id, **kwargs):
        """
            Allows subclasses to perform presave operations during API saves
            of the AnalysisModule
        """
        pass

    @classmethod
    def post_save(cls, user_id, objects, **kwargs):
        """
            Allows subclasses to perform postsave operations during API saves
            of the AnalysisModule
        """
        pass

    @property
    def unique_id(self):
        """
            The client id of this instance, a combination of its id and the ConfigEntity id
        """
        return '%s_%s' % (self.config_entity.id, self.id)

@receiver_subclasses(post_save, AnalysisTool, "on_analysis_tool_post_save")
def on_analysis_tool_post_save(sender, **kwargs):
    analysis_tool = kwargs['instance']
    if not analysis_tool._no_post_save_publishing:
        analysis_tool.update()

class AnalysisToolKey(Keys):
    SCENARIO_UPDATER_TOOL='scenario_updater_tool'
    ENVIRONMENTAL_CONSTRAINT_UNION_TOOL='environmental_constraint_union_tool'
    ENVIRONMENTAL_CONSTRAINT_UPDATER_TOOL='environmental_constraint_updater_tool'
    ENERGY_UPDATER_TOOL='energy_updater_tool'
    WATER_UPDATER_TOOL='water_updater_tool'
    VMT_UPDATER_TOOL='vmt_updater_tool'
    FISCAL_UPDATER_TOOL='fiscal_updater_tool'
    AGRICULTURE_UPDATER_TOOL='agriculture_upater_tool'
