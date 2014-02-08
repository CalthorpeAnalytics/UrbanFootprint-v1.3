
from inflection import titleize
from footprint.main.lib.functions import merge, remove_keys
from footprint.main.models.geospatial.db_entity import DbEntity
from footprint.main.models.geospatial.feature_class_creator import FeatureClassCreator
from footprint.main.utils.utils import resolvable_model_name, full_module_path
from footprint.client.configuration import resolve_fixture, InitFixture


__author__ = 'calthorpe_associates'

def create_db_entity_configuration(config_entity, **kwargs):
    """
        Returns a dictionary containing a DbEntity instance and a dynamic feature subclass based on the the class
        referenced by kwargs['base_class'] and optionally extra fields referenced by kwargs['fields'].
        The dynamic subclass instances represent features of the layer represented by the DbEntity instance.
    :param config_entity: Scopes the configuration. If null this will return an "abstract" configuration
    :param kwargs:
     'key':Used for the DBEntity key and table name, and also used to name the dynamic subclass of
        kwargs['base_class'] TODO: It might be better to use a separate name so that the feature class table
        can have the word 'feature' in it instead of 'layer;
     'name':Optional name for the DBEntity. By default the key value is used
     'db_entity_class' is optional and indicates the subclass to construct rather than DbEntity
     'base_class': the class to subclass whose instances represent features of the DbEntity.
     'fields': array of additional model fields for the subclass
    :return: a dict with a 'db_entity' key pointing to the DbEntity instance and a 'feature_class' key pointing to
        the dynamic feature subclass that was created based on the base_class and config_entity
    """

    if not config_entity:
        return abstract_db_entity_configuration(**kwargs)
    name = '{0}'.format(
        # The name is passed in named or the titlized version of key
        kwargs.get('name', None) or titleize(kwargs['key']))
    db_entity_class = kwargs.get('db_entity_class', DbEntity)
    db_entity_class_name = resolvable_model_name(db_entity_class)

    schema = config_entity.schema()
    init_fixture = resolve_fixture(None, "init", InitFixture, schema)
    connection = init_fixture.import_database()
    # Unless overridden, create the url according to this postgres url scheme
    url = kwargs.get('url',
                     'postgres://{user}:{password}/{host}:{port}/{database}'.format(
                         **merge(dict(port=5432),
                                 connection)) if connection else None)

    # We distinguish the DbEntity by key, name, and schema. Multiple DbEntities with the same key is a schema
    # may exist, but they must have different names to distinguish them
    feature_class_creator = FeatureClassCreator(config_entity)
    return dict(
        # This is used to determine what DbEntity subclass to create, if any
        db_entity_class_name=db_entity_class_name,
        key=kwargs['key'],
        schema=schema,
        name=name,
        url=url,
        table=kwargs.get('table', kwargs['key'] if not kwargs.get('query', None) else None),
        query=kwargs.get('query', None),
        group_by=kwargs.get('group_by', None),
        class_key=kwargs.get('class_key', None),
        hosts=kwargs.get('hosts', None), # TODO used?
        extent_authority=kwargs.get('extent_authority', False),
        creator=kwargs.get('creator', None),
        srid=kwargs.get('srid', None),
        feature_class_configuration=
            # If a feature_class_configuration is specified explicitly, that means we are cloning the db_entity from another config_entity
            # So just copy it and update for this config_entity
            feature_class_creator.feature_class_configuration_for_config_entity(kwargs['feature_class_configuration']) if \
                kwargs.get('feature_class_configuration') else \
                # Formulate the feature_class_configuration from the db_entity_configuratoin
                feature_class_creator.get_feature_class_configuration(
                    **remove_keys(kwargs, ['query', 'group_by', 'class_key', 'hosts', 'extent_authority', 'creator', 'srid'])
                ) if not 'no_feature_class_configuration' in kwargs else None
    )

def abstract_db_entity_configuration(**kwargs):
    """
        Returns a minimized db_entity_configuration when no config_entity is in scope. This is primarily to lookup the abstract
        Feature class by db_entity_key
    :param kwargs:
    :return:
    """
    return dict(
        key=kwargs['key'],
        feature_class_configuration=dict(
            abstract_class=full_module_path(kwargs['base_class'])
        )
    )

def db_entity_configuration_keys():
    # The keys of the DbEntity and DbEntity configuration, used for cloning
    return [
        'db_entity_class_name',
        'key',
        'schema',
        'name',
        'url',
        'table',
        'query',
        'group_by',
        'class_key',
        'url',
        'hosts',
        'extent_authority',
        'feature_class_configuration',
    ]
