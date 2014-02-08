import logging
from footprint.main.lib.functions import merge, remove_keys
from footprint.main.models import Layer
from footprint.main.models.database.information_schema import InformationSchema, sync_geometry_columns
from footprint.main.models.presentation.layer_selection import get_or_create_dynamic_layer_selection_class_and_table
from footprint.main.publishing.import_processor import ImportProcessor
from footprint.main.models.geospatial.feature_class_creator import FeatureClassCreator
from footprint.main.publishing.data_import_publishing import create_and_population_associations, add_primary_key_if_needed, DefaultImportProcessor

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
            feature_class_configuration = merge(
                origin_feature_class_configuration,
                # override the origin configuration except for stuff that should mimic it
                remove_keys(feature_class_creator.create_feature_class_configuration(), ['fields', 'intersection', 'abstract_class', 'source_from_origin_layer_selection']),
                # Erase import configuration properties
                dict(import_fields=[], import_ids_only=False))

            feature_class_creator.merge_feature_class_configuration_into_db_entity(feature_class_configuration)
            layer = Layer.objects.get(presentation__config_entity=config_entity, db_entity_key=db_entity.origin_instance.key)
            if db_entity.feature_class_configuration.get('source_from_origin_layer_selection'):
                layer_selection_class = get_or_create_dynamic_layer_selection_class_and_table(layer, True)
                layer_selection = layer_selection_class.objects.get(user=user)
                features = layer_selection.selected_features
            else:
                features = None

            DefaultImportProcessor().peer_importer(config_entity, db_entity, import_from_origin=True, source_queryset=features)


