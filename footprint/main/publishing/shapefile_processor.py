import logging
import stat
from footprint.main.database.import_data import ImportData
from footprint.main.models.database.information_schema import InformationSchema, sync_geometry_columns
from footprint.main.models.keys.content_type_key import ContentTypeKey
from footprint.main.publishing.import_processor import ImportProcessor
import zipfile
import os
from footprint.main.models.geospatial.feature_class_creator import FeatureClassCreator
from footprint.main.publishing.data_import_publishing import create_and_populate_relations, add_primary_key_if_needed
from django.conf import settings
from footprint.main.utils.utils import timestamp

logger = logging.getLogger(__name__)

__author__ = 'calthorpe'

class ShapefileProcessor(ImportProcessor):

    def __init__(self, **kwargs):
        self.srid = kwargs['db_entity'].srid # Required
        super(ShapefileProcessor, self).__init__()

    def importer(self, config_entity, db_entity):
        """
            Replaces the normal ImportProcessor importer with one to import a shapefile from disk
        """
        user = db_entity.creator

        if InformationSchema.objects.table_exists(db_entity.schema, db_entity.table):
            # The table already exists. Skip the import an log a warning
            logger.warn("The target table for the shapefile import already exists. Skipping table import.")
        else:
            zipfile = db_entity.url.replace('file://', '')
            shp, files_to_import = unpack_shapefile(zipfile, db_entity.key, user)
            import_shapefile_to_db(config_entity, db_entity, shp)

        # Add our normal primary key in the id column if needed
        add_primary_key_if_needed(db_entity)

        feature_class_creator = FeatureClassCreator(config_entity, db_entity)
        # Inspect the imported table to create the feature_class_configuration
        feature_class_configuration = feature_class_creator.feature_class_configuration_from_introspection()

        # Merge the created feature_class_configuration with the on already defined for the db_entity
        feature_class_creator.update_db_entity(feature_class_configuration)
        logger.debug("Finished shapefile import for DbEntity: %s, feature_class_configuration: %s" % (db_entity, db_entity.feature_class_configuration))

        # Create association classes and tables and populate them with data
        create_and_populate_relations(config_entity, feature_class_creator.db_entity)

def unpack_shapefile(zip_archive, name, user):
    archive = zipfile.ZipFile(zip_archive, 'r')
    archive_contents = archive.namelist()

    # verify that each file in the archive corresponds with a known shapefile type and is not
    # named with any strings that may compromise our servers
    for a in archive_contents:
        valid = False
        for shp_type in settings.SHAPEFILE_TYPES:
            if a.endswith(shp_type) and not a.startswith('/') and not ('..') in a:
                valid = True
        if not valid:
            raise Exception("Inspection of shapefile failed. Remove any extra files and make sure that filenames"
                            "do not use special characters")

    upload_media_path = os.path.join(settings.MEDIA_ROOT, 'uploads')
    # if the files seem okay, extract them to the media root
    archive.extractall(path=upload_media_path)

    files_to_import = []
    nice_name = "{username}_{geom_name}_{timestamp}".format(username=user.username,
                                                            geom_name=name,
                                                            timestamp=timestamp())

    for a in archive_contents:
        imported_name = os.path.join(upload_media_path, a)

        new_name = os.path.join(upload_media_path, nice_name + a[-4:])

        os.rename(imported_name, new_name)

        b = a.replace(a[:-4], name)
        if a.endswith('.shp'):
            shp = new_name

        files_to_import.append(b)

    return shp, files_to_import


def import_shapefile_to_db(config_entity, db_entity, shp):
    upload_media_path = os.path.join(settings.MEDIA_ROOT, 'uploads')
    shapefile_path = os.path.join(upload_media_path, shp),
    # Update the db_entity.url from the zip file url to the shapefile_path
    # This lets ImportData find it.
    db_entity.url = 'file://%s' % shapefile_path
    db_entity.feature_class_configuration.import_file_type = ContentTypeKey.SHAPEFILE
    db_entity.save()

    ImportData(config_entity=config_entity, db_entity_key=db_entity.key).run()
