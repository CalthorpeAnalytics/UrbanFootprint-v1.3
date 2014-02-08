import subprocess
import sys
import logging
from django.contrib.gis.gdal.datasource import DataSource
from django.contrib.gis.utils.layermapping import LayerMapping
from south.db import dbs
from django.db import connections, DatabaseError, connection
from south.utils.datetime_utils import datetime

from footprint.database.import_data import ImportData
from footprint.initialization.data_provider import DataProvider, SQLImportError
from footprint.initialization.fixture import InitFixture
from footprint.initialization.utils import resolve_fixture
from footprint.lib.functions import merge, any_true
from footprint.utils.dynamic_subclassing import create_table_for_dynamic_class
from footprint.utils.layermapping import MissingForeignKey
from footprint.utils.utils import parse_schema_and_table
import settings
from uf_tools import get_conn_string, dictfetchall
from footprint.models.geographies.geography import Geography
from footprint.models.database.information_schema import InformationSchema, register_geometry_columns

__author__ = 'calthorpe'

logger = logging.getLogger(__name__)


def on_config_entity_post_save_data_import(sender, **kwargs):
    """
        Sync a ConfigEntity's feature tables
    """
    config_entity = kwargs['instance']
    db_entity_keys = kwargs.get('db_entity_keys', None)

    # Get the list of DbEntity instances and their corresponding subclasses (the latter if it is configured)
    db_entities_and_classes = config_entity.default_db_entity_setups()

    for db_entity_dict in db_entities_and_classes:
        if db_entity_keys and not db_entity_dict['db_entity'].key in db_entity_keys:
            continue

        # Import the data into the subclass tables if an import strategy is specified. Otherwise the tables are left black
        db_entity = db_entity_dict['db_entity']

        # Only import if the config_entity is the owner of the db_entity. The ones that adopt it need not re-import
        if config_entity == config_entity.db_entity_owner(db_entity):
            feature_class = db_entity_dict.get('feature_class', None)
            source_db_entity_key = db_entity_dict.get('import_from_db_entity_key', None)

            # Recreate the destination table if was deleted
            if not InformationSchema.objects.table_exists(*parse_schema_and_table(feature_class._meta.db_table)):
                create_table_for_dynamic_class(feature_class)

            # If there is an origin_config_entity we override our importing and clone from the origin
            if config_entity.origin_config_entity:
                # The db_entity configured to import from another db_entity's class instance objects
                clone_table_import(config_entity, feature_class, source_db_entity_key)
            else:
                # Import from a source table
                if db_entity_dict.get('import_table', False):
                    # The table data needs to be imported from a seed table in the public schema
                    try:
                        seed_data_import(config_entity, db_entity, feature_class, db_entity_dict)
                    except SQLImportError, e:
                        # If the table doesn't import give a warning and continue
                        connection._rollback()
                        logger.warning(e.message)
                    except DatabaseError, e:
                        # If the table doesn't import give a warning and continue
                        connection._rollback()
                        logger.warning(e.message)
                # Copy data from a peer table
                elif source_db_entity_key:
                    # The db_entity configured to import from another db_entity's class instance objects
                    peer_table_import(config_entity, feature_class, source_db_entity_key,
                                      db_entity_dict.get('import_fields', ['geography_id', 'wkb_geometry']))
                    # Otherwise no import takes place.


def on_db_entity_save():
    """
    respond to whenever a db entity is added or updated
    :return:
    """


def on_config_entity_pre_delete_data_import(sender, **kwargs):
    """
        Sync geoserver to a ConfigEntity class after the latter is saved
    """
    pass


def sql_file_import_and_geography_sync(config_entity, db_entity, options):
    """
        Pulls seed data from a SQL file into the public schema, which then serves as a datasource to create
        ConfigEntity specfic tables. This process needs refining, or will be eliminated in favor of direct
        schema imports
    :param config_entity
    :param db_entity:
    :params options
    :return:
    """
    # If the db_entity is configured to import the table data, import from the public schema
    data_provider = DataProvider()
    table_name = data_provider.import_table_name(config_entity, db_entity)

    if not InformationSchema.objects.table_exists('public', table_name):
        import_features(config_entity, db_entity, options)


def import_features(config_entity, db_entity, options):
    """
        Imports the feature data from a sql dump file or remote database into the public schema. The import table is used to import Feature class instances and the related Geography instances
    :return:
    """

    data_provider = DataProvider()
    table_name = data_provider.import_table_name(config_entity, db_entity)

    db_name = connections.databases['default']['NAME']
    conn_string = get_conn_string('default')

    init_fixture = resolve_fixture(None, "init", InitFixture, settings.CLIENT)
    import_database = init_fixture.import_database()
    if settings.EXTERNALLY_IMPORT_FEATURES and import_database:
        # Attempt to fetch the feature tables from the import database
        ImportData(**merge(import_database, dict(config_entity=config_entity, db_entity_key=db_entity.key))).run()
    else:
        # Attempt to load the sql by searching for dump files in the STATIC_ROOT/sql folder
        sql_source = settings.STATIC_ROOT + "/sql/{0}.sql".format(table_name)

        load_parcel_command = "psql {0} -f {1}".format(db_name, sql_source)
        result = subprocess.call(load_parcel_command, shell=True)
        if result != 0:
            raise SQLImportError("Sql file could not be imported: {0}".format(load_parcel_command))

    register_geometry_columns(conn_string)
    sync_geographies(config_entity, db_entity, options)


def seed_data_import(config_entity, db_entity, feature_class, options):
    """
        Imports seed feature table data from a sql dump file
    :param config_entity:
    :param db_entity:
    :param feature_class:
    :param options
    :return:
    """

    # Import from a sql dump and create Geography instances for each feature in anticipation of importing the feature
    sql_file_import_and_geography_sync(config_entity, db_entity, options)

    if feature_class.objects.count() > 0:
        return
        # If the no features have been imported proceed with the import
    db = get_conn_string(config_entity.db)
    ds = DataSource("PG:" + db)
    data_provider = DataProvider()
    tablename = data_provider.import_table_name(config_entity, db_entity)
    layer = ds[tablename]
    mapping = {'wkb_geometry': 'UNKNOWN', }
    for f in layer.fields:
        mapping[f] = f

    # Map the Geography instance association. The Geography instance was already created with the uf_geometry_id set to
    # the Feature class's attribute specified by the unique id prepended with the configentity scope plus the db entity key and the options['source_id_column']
    mapping['geography'] = {'source_id': 'uf_geometry_id'}

    if options.get('import_mapping', None):
        # If the Feature class configuration defines import_mapping, pass the mapping to it so it can customize its mapping
        options['import_mapping'](mapping)

    logger.info('Import for class %s' % feature_class)
    try:
        # import_fields = []
        # mapping_fields, mapping_queries = _get_mapping_fields_and_queries(feature_class, mapping=mapping)
        # default_fields, field_defaults = _get_default_fields_and_values(feature_class, import_fields=import_fields)
        #
        # insert_sql = "insert into {table_name}({mapping_fields},{input_fields},{default_fields) " \
        #              "select {mapping_queries},{input_fields},{default_fields} from {source_table}".format
        #
        # import_query = insert_sql(
        #     table_name='',
        #     mapping_fields=mapping_fields,
        #     input_fields=import_fields,
        #     default_fields=default_fields,
        #     mapping_queries=mapping_queries,
        #     source_table=''
        # )

        base_import = LayerMapping(feature_class, ds, mapping, layer=tablename)

    except Exception, e:
        trace = sys.exc_info()[2]
        raise Exception(
            "Error mapping feature class %s of db_entity %s of config_entity %s with mapping %s. Original Exception: %s" %
            (feature_class.__name__, db_entity.key, config_entity.key, mapping, e.message)), None, trace
    try:
        base_import.save(progress=True, strict=True)
    except MissingForeignKey, e:
        trace = sys.exc_info()[2]
        raise Exception(
            "Missing Foreign key instance for feature class %s of db_entity %s of config_entity %s with mapping %s. "
            "Original Exception: %s" %
            (feature_class.__name__, db_entity.key, config_entity.key, mapping, e.message)), None, trace


def sync_geographies(config_entity, db_entity, options={}):
    """
        Write geometry column data into the geography table for a feature table that was just imported.
    :param config_entity
    :param db_entity
    :param options:
    """
    register_geometry_columns(None, options.get('schema', None))
    data_provider = DataProvider()
    table_name = data_provider.import_table_name(config_entity, db_entity)
    logger.info("syncing {source_table} to footprint geography".format(source_table=table_name))

    conn_string = get_conn_string('default')
    datasource = DataSource("PG:{0}".format(conn_string))
    mapping = geography_mapping(table_name, options)


    cursor = connections['default'].cursor()
    # Generate a source_id column on the import table which uniquely identifies each geometry row
    source_id_prefix = '{0}__{1}__'.format(config_entity.schema(), db_entity.key)

    if not 'uf_geometry_id' in map(lambda s: s.column_name, InformationSchema.objects.columns_of_table('public', table_name)):
        alter_source_id_sql = '''alter table {source_table} add column uf_geometry_id varchar;''' \
            .format(source_table=table_name)
        cursor.execute(alter_source_id_sql)
        connections['default'].commit()
        update_source_id_sql = '''update {source_table} set uf_geometry_id = cast('{source_id_prefix}' || cast({source_id_column} as varchar) as varchar);'''.format(source_table=table_name, source_id_prefix=source_id_prefix, source_id_column=mapping['source_id'])
        cursor.execute(update_source_id_sql)
        connections['default'].commit()

    cursor.execute('select uf_geometry_id from {table}'.format(
        table=table_name)
    )
    rows = dictfetchall(cursor)
    test_source_id = rows[0]['uf_geometry_id']
    # If the Geography table already has our source_ids assume that we already did the import
    if len(Geography.objects.filter(source_id=test_source_id)) == 1:
        print "Geography table already contains a source_id matching the feature table's first source_id"
        return

    cursor.execute(update_source_id_sql)
    connections['default'].commit()

    geography_column_insert_sql = "insert into footprint_geography(geometry, source_id) \
    select st_SetSRID(st_transform(wkb_geometry, 4326),4326), uf_geometry_id from {source_table}".format(
        source_id=mapping['source_id'], source_table=table_name)
    result = cursor.execute(geography_column_insert_sql)
    if result:
        raise result
        #
        # layer_map = LayerMapping(Geography, datasource, mapping, layer=table_name)
        # layer_map.save()


def geography_mapping(table, options={}):
    return merge({'source_id': options['source_id_column']} if options.get('source_id_column', None) else {},
                 {'geometry': 'UNKNOWN', })


def clone_table_import(config_entity, db_entity_key, import_fields=None):
    """
        Clones data from the config_entity's origin_config_entity
    :param config_entity:
    :param db_entity_key:
    :param import_fields. Optional limited fields to import. If None it imports all fields.
    :return:
    """

    destination_feature_class = config_entity.origin_config_entity.feature_class_of_db_entity(db_entity_key)
    source_feature_class = config_entity.origin_config_entity.feature_class_of_db_entity(db_entity_key)

    return _table_import(destination_feature_class, source_feature_class, import_fields)


def peer_table_import(config_entity, feature_class, source_db_entity_key, import_fields):
    """
        Creates the ConfigEntity specific FeatureClass table by importing from a peer table, the former is
        indicated by the feature_class and the latter by the source_feature_class.
    :param config_entity: The config_entity import target
    :param feature_class: The feature_class that models the destination table
    :param source_db_entity_key: The feature_class that models the source table
    :param import_fields: Array of field names limiting the fields to be imported. Those imported must be modeled in
    the feature_class. By default all fields modeled by the feature_class are imported
    :return:
    """
    source_feature_class = config_entity.feature_class_of_db_entity(source_db_entity_key)
    return _table_import(feature_class, source_feature_class, import_fields)


def _get_mapping_fields_and_queries(feature_class, mapping):
    mapping_query = "(select a.id from {related_table} a, {source_table} b where b.{source_id_column} = a.{related_id})"
    # related_fields = (field, map for field in mapping.items() if isinstance(field, dict))
    mapping_fields = ''
    mapping_queries = ''


def _get_default_fields_and_values(feature_class, import_fields=[]):
    default_django_fields = [field for field in feature_class._meta.fields if field.column not in import_fields]
    default_fields = ''
    field_defaults = ''
    for field in default_django_fields:
        if field.null:
            continue
        default_fields += field.column + ", "
        if getattr(field, "auto_now", False) or getattr(field, "auto_now_add", False):
            field_defaults += "'" + str(datetime.now()) + "', "
        else:
            field_defaults += "'" + str(field.default) + "', "

    default_fields = default_fields[:-2]
    field_defaults = field_defaults[:-2]
    return default_fields, field_defaults


def _table_import(destination_feature_class, source_feature_class, import_fields=None):
    """
        Handles the details of clone_table_import and peer_table_import
    :param destination_feature_class:
    :param source_feature_class:
    :param import_fields:
    :return:
    """
    import_manager = source_feature_class.objects
    import_table = import_manager.model._meta.db_table

    if destination_feature_class.objects.count() == 0:

        insert_statement = """
        truncate table {feature_class_table} cascade;
        insert into {feature_class_table}({source_fields}{default_fields})
        select {source_fields}{field_defaults} from {source_table};
        """.format

        source_fields = ""

        if not import_fields:
            import_fields = map(lambda field: field.column, destination_feature_class._meta.fields)
        else:
            import_fields.append('id')

        for field in import_fields:
            source_fields += "{field}, ".format(field=field)

        default_fields, field_defaults = _get_default_fields_and_values(destination_feature_class, import_fields)

        dbs['default'].execute(insert_statement(
            feature_class_table=destination_feature_class._meta.db_table,
            source_fields=source_fields,
            source_table=import_table,
            default_fields=default_fields,
            field_defaults=field_defaults)
        )