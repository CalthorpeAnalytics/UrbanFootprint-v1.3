import logging
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import Signal
from footprint.main.models.config.scenario import FutureScenario, BaseScenario
from footprint.main.models.geospatial.db_entity_configuration import create_db_entity_configuration, db_entity_configuration_keys
from footprint.main.models.geospatial.feature_class_creator import FeatureClassCreator
from footprint.main.publishing import data_import_publishing, layer_publishing, result_publishing, tilestache_publishing
from footprint.main.publishing.config_entity_publishing import post_save_publishing
from footprint.main.publishing.geo_json_processor import GeoJsonProcessor
from footprint.main.publishing.origin_db_entity_processor import OriginDbEntityProcessor
from footprint.main.publishing.shapefile_processor import ShapefileProcessor
from footprint.main.utils.subclasses import receiver_subclasses
from footprint.client.configuration.fixture import ConfigEntityFixture


from footprint.main.models.config.config_entity import ConfigEntity
from footprint.main.models.config.global_config import GlobalConfig
from footprint.main.models.config.project import Project
from footprint.main.models.config.region import Region
from footprint.main.models.geospatial.db_entity import DbEntity
from footprint.main.models.database.information_schema import PGNamespace
from footprint.main.lib.functions import filter_keys, merge, remove_keys
from footprint.main.models.config.db_entity_interest import DbEntityInterest
from footprint.main.models.config.interest import Interest
from footprint.main.models.keys.keys import Keys
from footprint.main.utils.utils import resolve_model, resolvable_module_attr_path, full_module_path, resolvable_model_name

__author__ = 'calthorpe_associates'

logger = logging.getLogger(__name__)

# All initial signals. They can run without dependencies
# All signals that can run after db_entities run
post_save_db_entity_initial = Signal(providing_args=[])
# All signals that can run after layer run
# This name is plural because one can in theory have multiple layers per db_entity
post_save_db_entity_layers = Signal(providing_args=[])
# All signals that can run after data imports run
post_save_db_entity_import = Signal(providing_args=[])

def dependent_signal_paths(signal_path):
    """
        Gives the hierarchy of publisher signal calling order based on the given signal
        Signals are given as strings instead of paths for serialization ease
        param: signal_path. The signal path for which the dependent signals are returned
        return: An array of signal_paths or an empty array
    """
    if signal_path == resolvable_module_attr_path(__name__, 'post_save_db_entity_initial'):
        # DataImport dependent publishers are run after DbEntity dependent publishers
        return [resolvable_module_attr_path(__name__, 'post_save_db_entity_import')]
    if signal_path == resolvable_module_attr_path(__name__, 'post_save_db_entity_import'):
        # To be safe, have Layer dependents import run after data import
        return [resolvable_module_attr_path(__name__, 'post_save_db_entity_layers')]
    return []

# All signals that can run after data imports run
# Very wild guess about config_entity saving proportional times to send to the client
# These represent the parsed signal names sent to the client after the dependencies of
# the signal finish running
signal_proportion_lookup = dict(
    # initial signal after save
    post_save_db_entity_initial=.34,
    # layers and dataImports run in parallel
    post_save_db_entity_layers=.33,
    post_save_db_entity_import=.33
)

def post_save_db_entity_initial_publishers(cls):
    """
        Data Import publishing, Layer publishing, and Result publishing can happen after DbEntity publishing
    """
    post_save_db_entity_initial.connect(data_import_publishing.on_db_entity_post_save_data_import, cls, True, "data_import_on_db_entity_post_save")


def post_save_db_entity_import_publishers(cls):
    """
        Layers and Result publishing can run after Data Import publishing
    """
    post_save_db_entity_import.connect(layer_publishing.on_db_entity_post_save_layers, cls, True, "layer_on_db_entity_post_save")
    post_save_db_entity_import.connect(result_publishing.on_db_entity_post_save_result, cls, True, "result_on_db_entity_post_save")

def post_save_db_entity_layers_publishers(cls):
    """
        Tilestache publishing can run after the Layer publisher
    """
    post_save_db_entity_layers.connect(tilestache_publishing.on_db_entity_post_save_tilestache, cls, True, "tilestache_on_db_entity_post_save")

# Register receivers for only the lineage classes of Scenario subclasses
for cls in [FutureScenario, BaseScenario, Project, Region, GlobalConfig]:
    post_save_db_entity_initial_publishers(cls)
    post_save_db_entity_import_publishers(cls)
    post_save_db_entity_layers_publishers(cls)

#@profile
def on_config_entity_post_save_db_entity(sender, **kwargs):
    """
        Sync a ConfigEntity's DbEntities
    """
    config_entity = kwargs['instance']
    logger.debug("\t\tHandler: on_config_entity_post_save_db_entity. ConfigEntity: %s" % config_entity.name)
    if ConfigEntity._heapy:
        ConfigEntity.dump_heapy()
    update_or_create_db_entities(config_entity)

@receiver_subclasses(post_save, DbEntityInterest, "db_entity_interest_post_save")
def on_db_entity_interest_post_save(sender, **kwargs):
    """
        Called after a DbEntityInterest saves, but not when a config_entity is running post_save publishers
        In other words, this is only called after a direct DbEntityInterest save/update.
        This does the same as post_save_config_entity, but starts with the 'post_save_config_entity_db_entities'
        signal to do only DbEntity dependent publishing.
    """
    db_entity_interest = kwargs['instance']
    if kwargs.get('created', None):
        db_entity = db_entity_interest.db_entity
        # TODO
        # While we test upload, just delete the previous DbEntitys with the same key name
        # in the ConfigEntity.
        db_entity_interest.config_entity.db_entities.filter(key=db_entity.key).exclude(id=db_entity.id).delete()

        # Make sure the db_entity's schema matches the config_entity's if not set
        # TODO we assume that the schema should match the config_entity, rather than
        # an ancestor or the config_entity (like the project or a scenario). There
        # are many cases where the schema should not be that of the config_entity, so
        # we might want to remove this default and force the saver to set it
        if not db_entity.schema or not db_entity.table:
            db_entity.schema = db_entity.schema or db_entity_interest.config_entity.schema()
            # Always base the table name on the key
            db_entity.table = db_entity.key
            # Update changes with the publishers turned off
            publishers_off = db_entity_interest.config_entity._no_post_save_db_entity_interest_publishing
            db_entity_interest.config_entity._no_post_save_db_entity_interest_publishing = True
            db_entity_interest.db_entity.save()
            db_entity_interest.config_entity._no_post_save_db_entity_interest_publishing = publishers_off

    if db_entity_interest.config_entity.deleted:
        # Do nothing for deleted config_entities
        return

    # Commence the post-save publishing chain for DbEntityInterests, such as the DataImport and Layer publishers
    # but only if _no_post_save_db_entity_interest_publishing wasn't set outside this call

    config_entity = ConfigEntity._subclassed_config_entity(db_entity_interest.config_entity)
    # TODO The default user should be the admin
    user = config_entity.creator if config_entity.creator else User.objects.all()[0]
    db_entity = db_entity_interest.db_entity

    if db_entity.deleted:
        # Do nothing for deleted db_entities
        return

    # Check to see if the DbEntity has a complete feature_class_configuration
    feature_class_creator = FeatureClassCreator(config_entity, db_entity)
    if not feature_class_creator.feature_class_is_ready:
        # Create or further refine the feature_class_configuration
        # Merge what exists with generated=True to mark the configuration as generated rather than preconfigured
        db_entity.feature_class_configuration = feature_class_configuration = merge(db_entity.feature_class_configuration or {}, dict(generated=True))
        # Choose the correct importer, if any, to set up the feature_class_configuration and features
        if db_entity.origin_instance:
            # Import from the origin_instance. This could be a full copy or from the current layer selection features
            feature_class_configuration['data_importer'] = full_module_path(OriginDbEntityProcessor)
        elif '.json' in db_entity.url:
            # Import it using the geojson importer
            feature_class_configuration['data_importer'] = full_module_path(GeoJsonProcessor)
        elif '.zip' in db_entity.url:
            feature_class_configuration['data_importer'] = full_module_path(ShapefileProcessor)
        else:
            # Assume a remote url for background imagery, and thus no nothing
            return
        db_entity_interest.config_entity._no_post_save_db_entity_interest_publishing = True
        db_entity.save()
        db_entity_interest.config_entity._no_post_save_db_entity_interest_publishing = False

    # Quit if the publishers were turned off outside this method
    if db_entity_interest.config_entity._no_post_save_db_entity_interest_publishing:
        return

    starting_signal_path = resolvable_module_attr_path(__name__, 'post_save_db_entity_initial')

    logger.debug("Handler: post_save_db_entity_interest for config_entity {config_entity}, db_entity {db_entity}, and user {username}".format(
        config_entity=config_entity,
        db_entity=db_entity_interest.db_entity,
        username=user.username))
    if ConfigEntity._heapy:
        ConfigEntity.dump_heapy()


    return post_save_publishing(
        starting_signal_path,
        config_entity,
        user,
        instance=db_entity_interest,
        instance_key=db_entity_interest.db_entity.key,
        signal_proportion_lookup=signal_proportion_lookup,
        dependent_signal_paths=dependent_signal_paths,
        signal_prefix='post_save_db_entity'
    )

def update_or_create_db_entities(config_entity):
    """
        Creates or updates the db_entities of the ConfigEntity
    :param config_entity
    :return:
    """

    # If not present, create the database schema for this ConfigEntity's feature table data
    PGNamespace.objects.create_schema(config_entity.schema())

    client_fixture = ConfigEntityFixture.resolve_config_entity_fixture(config_entity)

    # Process the DbEntities from the origin_config_entity or the db_entity_configuration from the fixtures.
    # We only get those scoped (owned) by the class of our config_entity. The scoped above will be adopted automatically
    # and need not be created. This means a Scenario creates DbEntities scoped to Scenario and adopts those scoped
    # to Project or Region. It does not clone the latter.

    if config_entity.origin_config_entity:
        origin_config_entity = config_entity.origin_config_entity
        # Clone the DbEntities from the origin ConfigEntity.
        # The given kwargs are the only overrides needed to correctly set up the target DbEntity
        db_entities_or_configurations = map(
            lambda db_entity: clone_or_update_db_entity_and_interest(
                config_entity,
                db_entity,
                schema=config_entity.schema(),
                scope=config_entity.id,
                geography_scope=FeatureClassCreator(config_entity).resolve_geography_scope(),
                class_attrs={'config_entity__id': config_entity.id, 'override_db': config_entity.db, 'db_entity_key': db_entity.key}).db_entity,
            origin_config_entity.owned_db_entities())
    else:
        # Get the default DbEntity configurations from the fixture
        default_db_entity_configurations = client_fixture.default_db_entity_configurations()
        # Find additional owned (not adopted) db_entities that aren't defaults, namely those that were created by the user
        additional_db_entities = client_fixture.non_default_owned_db_entities()
        # Combine the defaults with the additions
        db_entities_or_configurations = default_db_entity_configurations+list(additional_db_entities)

    update_or_create_db_entity_interests(config_entity, *db_entities_or_configurations)
    # Disable the post_post_save signal while saving to prevent an infinite loop
    config_entity._no_post_save_publishing = True
    # Save post_create changes. This is just to store selected DbEntities
    config_entity.save()
    config_entity._no_post_save_publishing = False

def update_or_create_db_entity_interests(config_entity, *db_entity_configurations_or_db_entities):
    """
        Configures saved DbEntities by creating their subclass tables if needed and their DbEntityInterest. This
        is an extension of sync_default_db_entities but is also used by publishers to configure the DbEntities
        that they need that aren't part of the default sets.
        already in a post_config_entity save handler
        :param db_entity_configurations_or_db_entities: A list of db_entity configurations or db_entities (the latter
        is used if creating a new DbEntity from another)
    :return:
    """

    # Getting ready to create or update DbEntityInterests. Tell the DbEntityInterest post_save handler
    # to NOT start the DbEntity publishing chain. We don't want to run the DbEntity dependent publishers
    # such as Layers and DataImport. The ConfigEntityPublisher will run these itself
    config_entity._no_post_save_db_entity_interest_publishing = True

    # Do a forced adoption of DbEntityInterests from the parent ConfigEntity. This makes sure that ConfigEntity has
    # the parent's DbEntityInterests before adding any of its own. Otherwise the parent's are never adopted and
    # are created from the db_entity_configurations instead, which is minimally less efficient
    # See _adopt_from_donor docs for an explanation.
    config_entity._adopt_from_donor('db_entities', True)

    db_entity_interests_and_created = map(
        lambda db_entity_configuration_or_db_entity: update_or_create_db_entity_and_interest(config_entity, db_entity_configuration_or_db_entity),
        db_entity_configurations_or_db_entities)

    # Now add the db_entity_interests that were created.
    # They are already associated with the ConfigEntity on creation so this doesn't really do much
    created_db_entity_interests = map(lambda tup: tup[0], filter(lambda db_entity_interests_and_created: db_entity_interests_and_created[1], db_entity_interests_and_created))
    config_entity.add_db_entity_interests(*created_db_entity_interests)

    # Remove temporary flag
    config_entity._no_post_save_db_entity_interest_publishing = False

def update_or_create_db_entity_and_interest(config_entity, db_entity_configuration_or_db_entity):
    """
        Sync a single db_entity_configuration or db_entity and its db_entity_interest
        :return A tuple of the DbEntityInterest and the created flag
    """
    if not isinstance(db_entity_configuration_or_db_entity, DbEntity):
        # If a subclass of DbEntity is needed, find it here
        db_entity_clazz = resolve_model(db_entity_configuration_or_db_entity['db_entity_class_name'])

        # Get or create the feature_class if configured
        db_entity = db_entity_clazz.objects.update_or_create(**merge(
            # key and schema uniquely identify the DbEntity
            filter_keys(db_entity_configuration_or_db_entity, ['key', 'schema']),
            dict(defaults=remove_keys(db_entity_configuration_or_db_entity,
                                      ['db_entity_class_name', 'key', 'schema']))))[0]
    else:
        db_entity = db_entity_configuration_or_db_entity

    logger.debug("\t\t\tConfigEntity/DbEntity Publishing. DbEntity: %s" % db_entity.full_name)

    # Create the DbEntityInterest through class instance which associates the ConfigEntity instance
    # to the DbEntity instance. For now the interest attribute is hard-coded to OWNER. This might
    # be used in the future to indicate other levels of interest
    interest = Interest.objects.get(key=Keys.INTEREST_OWNER)
    db_entity_interest, created, updated = DbEntityInterest.objects.update_or_create(
        config_entity=config_entity,
        db_entity=db_entity,
        interest=interest)

    return db_entity_interest, created


def full_name_of_db_entity_table(self, table):
    """
    :param table: the table name of the table that the DbEntity represents
    :return: The combined schema and table name of the given db_entity. This is used to name the dynamic class that is created to represent the table
    """
    return '"{0}"."{1}"'.format(self.schema(), table)

def clone_or_update_db_entity_and_interest(config_entity, source_db_entity, **kwargs):
    """
        Clones or updates the source_db_entity modified with the given kwargs (including possibly the key) into this ConfigEntity.
        This is used for a duplicate clone from one ConfigEntity (same DbEntity key) to another and also for
        creating a modified DbEntity for a Result from a non-Result DbEntity (different DbEntity key). A third case for this
        method is cloning a DbEntity within a ConfigEntity, which is not yet implemented.

        If the kwargs['override_on_update'] is True, the kwargs should override the target DbEntity attribute values on update.
        This is useful for the Result clone case where we want to pick up updates to the source DbEntity. But in the straight
        clone case we want to make the target DbEntity independent of the source once it is created.
        Returns the DbEntityInterest

        :param: config_entity. The config_entity of the DbEntities
        :param: source_db_entity. The source of the clone
        :param: kwargs. Attributes matching the DbEntity that need to override those of the source_db_entity. This might be the
        key, schema, etc. override_on_update is optional and is described above
    """

    # key is always resolved by the kwargs or else the source DbEntity key
    key = kwargs.get('key', source_db_entity.key)
    db_entity_exists = config_entity.db_entities.filter(key=key).count() == 1
    create_or_update_on_override =  not db_entity_exists or kwargs.get('override_on_update', False)

    # Prefer the kwargs values over those of the db_entity
    db_entity_configuration = merge(
        # Extract the db_entity_configuration_keys from the source DbEntity
        filter_keys(source_db_entity.__dict__, db_entity_configuration_keys()),
        # Override keys with the passed in kwargs only on create or on update if override_on_update==True
        remove_keys(kwargs,
                    list(set(['override_on_update', 'key']+FeatureClassCreator.FEATURE_CLASS_CONFIGURATION_KEYS)-set(['table', 'schema']))) \
            if create_or_update_on_override else dict(),
        # Always use this key
        dict(key=key),
        # Set the clone source key if different than the target key
        dict(class_key=source_db_entity.key) if source_db_entity.key != key else dict(),
        dict(
             # Override feature_class_configuration keys if specified in the kwargs and create_or_update_on_ovrride is True
             feature_class_configuration=merge(
                source_db_entity.feature_class_configuration,
                filter_keys(kwargs, FeatureClassCreator.feature_class_configuration_keys()) if create_or_update_on_override else dict(),
                dict(db_entity_key=key))),
        dict(
             # db_entity_class_name is not stored by the source db_entity, since it knows what class it is
             db_entity_class_name=resolvable_model_name(source_db_entity.__class__))
    )

    # Getting ready to create or update DbEntityInterest. Tell the DbEntityInterest post_save handler
    # to NOT start the DbEntity publishing chain. We don't want to run the DbEntity dependent publishers
    # such as Layers and DataImport for Result DbEntity.
    config_entity._no_post_save_db_entity_interest_publishing = True

    db_entity_interest = update_or_create_db_entity_and_interest(config_entity, db_entity_configuration)[0]

    # Remove temporary flag
    config_entity._no_post_save_db_entity_interest_publishing = False

    return db_entity_interest
