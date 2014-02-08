from footprint.models.geospatial.feature import Feature

__author__ = 'calthorpe'


class PrimaryParcelFeature(Feature):
    # Every subclass must define a land_use_definition ForeignKey whose type is a subclass of ClientLandUseDefinition
    # land_use_definition = models.ForeignKey(ClientLandUseDefinition, null=True)

    # Dynamically created by dynamic subclasses
    # census_block = models.ForeignKey(CensusBlock, null=True)

    class Meta(object):
        abstract = True
        app_label = 'footprint'
