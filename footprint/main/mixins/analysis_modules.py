
__author__ = 'calthorpe'

class AnalysisModules(object):
    """
        Convenience methods to access AnalysisModules from a ConfigEntity. ConfigEntity's don't store references to
        these, they are dynamic classes modeled by tables created in the ConfigEntity's schema
    """

    @property
    def analysis_modules(self):
        from footprint.main.models import AnalysisModule
        return AnalysisModule.objects.filter(config_entity=self)
