import logging

from footprint.main.lib.functions import merge
from footprint.main.models.presentation.layer import Layer
from footprint.main.models.database.information_schema import InformationSchema
from footprint.main.models.presentation.layer_selection import get_or_create_dynamic_layer_selection_class_and_table
from footprint.main.publishing.import_processor import ImportProcessor
from footprint.main.models.geospatial.feature_class_creator import FeatureClassCreator
from footprint.main.publishing.data_import_publishing import DefaultImportProcessor


logger = logging.getLogger(__name__)

__author__ = 'calthorpe'

class OriginDbEntityProcessor(ImportProcessor):

    def importer(self, config_entity, db_entity):
        """
            Replaces the normal ImportProcessor importer with one to import a shapefile from disk
        """
        user = db_entity.creator

        if InformationSchema.objects.table_exists(db_entity.schema, db_entity.table):
            # The table already exists. Skip the import an log a warning
            logger.warn("The target table for the layer selection import already exists. Skipping table import.")
        else:
            feature_class_creator = FeatureClassCreator(config_entity, db_entity)
            origin_feature_class_configuration = db_entity.origin_instance.feature_class_configuration
            # Create the new DbEntity FeatureClassConfiguration from the origin's. Pass in what has already been
            # created for the new feature_class_configuration. This should have things like generated=True
            feature_class_configuration = feature_class_creator.complete_or_create_feature_class_configuration(
                origin_feature_class_configuration,
                **merge(db_entity.feature_class_configuration.__dict__, dict(generated=True)))
            # Update the DbEntity
            feature_class_creator.update_db_entity(feature_class_configuration)

            if feature_class_configuration.source_from_origin_layer_selection and \
               feature_class_configuration.origin_layer_id:
                # If desired, limit the layer clone to that of the source layer's current LayerSelection for the
                # User doing the update
                layer_selection_class = get_or_create_dynamic_layer_selection_class_and_table(
                    Layer.objects.get(id=feature_class_configuration.origin_layer_id), True)
                layer_selection = layer_selection_class.objects.get(user=user)
                features = layer_selection.selected_features
            else:
                # Leave blank to copy all features by default
                features = None

            DefaultImportProcessor().peer_importer(config_entity, db_entity, import_from_origin=True, source_queryset=features)


