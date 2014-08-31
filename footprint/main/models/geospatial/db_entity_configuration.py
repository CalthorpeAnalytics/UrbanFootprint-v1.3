from django.contrib.auth.models import User
from inflection import titleize
from footprint.client.configuration.fixture import InitFixture
from footprint.main.lib.functions import merge
from footprint.main.models import FeatureBehavior
from footprint.main.models.geospatial.db_entity import DbEntity
from footprint.main.models.geospatial.feature_class_creator import FeatureClassCreator
from footprint.client.configuration.utils import resolve_fixture

__author__ = 'calthorpe_associates'


def db_entity_defaults(db_entity, config_entity=None):

    # Instantiate a FeatureClassCreator to make the FeatureClassConfiguration
    feature_class_creator = FeatureClassCreator(config_entity, db_entity, no_ensure=True)
    if config_entity:
        # Find the database of the configured client
        connection = resolve_fixture(None, "init", InitFixture, config_entity.schema()).import_database()
    else:
        # No config_entity abstract DbEntity case
        connection = None

    return dict(
        # The name is passed in or the titleized version of key
        name=db_entity.name or titleize(db_entity.key),
        # Postgres URL for local sources, or possibly a remote url (e.g. for background layer sources)
        # Unless overridden, create the url according to this postgres url scheme
        url=db_entity.url or \
            ('postgres://{user}:{password}/{host}:{port}/{database}'.format(
                **merge(dict(port=5432), connection)) if connection else None),
        # Normally Equals the key, except for views of the table, like a Result DbEntity
        # Views leave this null and rely on query
        table=db_entity.table or (db_entity.key if not db_entity.query else None),
        # Query to create a "view" of the underlying data. Used by Result DbEntity instances
        query=db_entity.query,
        # How to group the features or query results. Not yet well hashed out
        group_by=db_entity.group_by,
        # The source DbEntity key if this DbEntity resulted from cloning a peer DbEntity
        source_db_entity_key=db_entity.source_db_entity_key,
        # Array used by remote data sources whose URLs have different host names
        # If so then the url will have a string variable for the host
        hosts=db_entity.hosts,
        # Indicates that this DbEntity's geography extent is an authority extent used to
        # calculate the ConfigEntity's extent
        extent_authority=db_entity.extent_authority or False,
        # The User who created the DbEntity. TODO. Default should be an admin
        creator=db_entity.creator if hasattr(db_entity, 'creator') else User.objects.filter()[0],
        # The User who updated the DbEntity. TODO. Default should be an admin
        updater=db_entity.creator if hasattr(db_entity, 'creator') else User.objects.filter()[0],

        # The SRID of the Feature table
        srid=db_entity.srid,
        # This is a non-model object. So it is saved as a PickledObjectField
        # Whether the same instance is returned or not does not matter
        # If db_entity.feature_class_configuration is None, it will return None
        feature_class_configuration=feature_class_creator.complete_or_create_feature_class_configuration(
            db_entity.feature_class_configuration
        ),
        no_feature_class_configuration=db_entity.no_feature_class_configuration,
        # feature_behavior is handled internally by DbEntity
    )


def update_or_create_db_entity(config_entity, db_entity):
    """
        Returns an updated version of the DbEntity or a clone. The DbEntity may come from the following sources:
            1. Client Configuration. Whether preconfigured on the server or received from the API,
            this is an unsaved DbEntity used to create a complete DbEntity associated with the ConfigEntity.
            1.5. Same as 1 but no config_entity is given. Return a minimum version of the DbEntity, unsaved.
            This happens upon system initialization when we just need basic attributes of the preconfigured DbEntities.
            2. ConfigEntity Clone. Clone the DbEntity, changing nothing but ConfigEntity specifics
            3. Update existing DbEntity. For case 1, if the DbEntity matching the Key and ConfigEntity already
            exists, call update or create passing the dict of this db_entity to that function.
            4. If we receive a saved db_entity (has an id) then apply defaults and save it. This would be a
            post_save process invoked by the API or the system saving the DbEntity
    """

    if not config_entity:
        # Just give back the unsaved, incomplete version
        db_entity.__dict__.update(db_entity_defaults(db_entity))
        return db_entity

    try:
        # feature_behavior is saved after DbEntity. It references DbEntity
        feature_behavior = db_entity.feature_behavior
    except:
        feature_behavior = None

    # Return a persisted DbEntity, either updated or created
    updated_db_entity = DbEntity.objects.update_or_create(
        # Uniqueness is based on key and schema
        key=db_entity.key,
        # The schema of the owning config_entity, used for uniqueness
        # This is always the same as db_entity.configentity_set[0].schema()
        schema=config_entity.schema(),
        defaults=db_entity_defaults(db_entity, config_entity)
    )[0]

    # Now persist the feature_behavior
    FeatureBehavior._no_post_save_publishing = True
    updated_db_entity.update_or_create_feature_behavior(feature_behavior)
    FeatureBehavior._no_post_save_publishing = False

    return updated_db_entity



