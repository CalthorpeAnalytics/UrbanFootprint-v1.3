from footprint.main.models import DbEntity, Behavior, FeatureBehavior
from footprint.main.models.geospatial.behavior import BehaviorKey
from footprint.main.models.geospatial.db_entity_configuration import update_or_create_db_entity
from footprint.client.configuration.fixture import RegionFixture
from footprint.main.models.geospatial.db_entity_keys import DbEntityKey

__author__ = 'calthorpe_associates'

class SacogDbEntityKey(DbEntityKey):
    EXISTING_LAND_USE_PARCEL_SOURCE = 'sacog_existing_land_use_parcels'
    STREAM = 'streams'
    VERNAL_POOL = 'vernal_pools'
    WETLAND = 'wetlands'
    HARDWOOD = 'hardwoods'
    LIGHT_RAIL = 'light_rail'
    LIGHT_RAIL_STOPS = 'light_rail_stops'
    LIGHT_RAIL_STOPS_ONE_MILE = 'light_rail_stops_one_mile'
    LIGHT_RAIL_STOPS_HALF_MILE = 'light_rail_stops_half_mile'
    LIGHT_RAIL_STOPS_QUARTER_MILE = 'light_rail_stops_quarter_mile'

class SacogRegionFixture(RegionFixture):

    def default_remote_db_entity_configurations(self):
        """
            Add the SACOG background. This function is called from default_db_entities so it doesn't
            need to call the parent_fixture's method
        """
        # The Behavior keyspace
        behavior_key = BehaviorKey.Fab.ricate
        # Used to load Behaviors defined elsewhere
        get_behavior = lambda key: Behavior.objects.get(key=behavior_key(key))

        return [DbEntity(
            key='sacog_background',
            url="http://services.sacog.org/arcgis/rest/services/Imagery_DigitalGlobe_2012WGS/MapServer/tile/{Z}/{Y}/{X}",
            no_feature_class_configuration=True,
            feature_behavior=FeatureBehavior(
                behavior=get_behavior('remote_imagery')
            )
        )]

    def default_db_entities(self):
        """
            Region specific SACOG db_entity_setups
        :param default_dict:
        :return:
        """

        config_entity = self.config_entity
        parent_region_fixture = self.parent_fixture
        default_db_entities = parent_region_fixture.default_db_entities()

        remote_db_entity_setups = map(
            lambda db_entity: update_or_create_db_entity(config_entity, db_entity),
            self.default_remote_db_entity_configurations())

        return default_db_entities + remote_db_entity_setups

