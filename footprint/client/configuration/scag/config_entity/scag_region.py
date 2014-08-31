
from footprint.main.models.geospatial.db_entity_configuration import update_or_create_db_entity
from footprint.client.configuration.fixture import RegionFixture
from footprint.main.models.geospatial.db_entity_keys import DbEntityKey

__author__ = 'calthorpe_associates'

class ScagDbEntityKey(DbEntityKey):
    EXISTING_LAND_USE_PARCEL_SOURCE = 'scag_existing_land_use_parcels'
    GENERAL_PLAN = 'general_plan_parcels'
    PRIMARY_SPZ_SOURCE = 'primary_spz'
    JURISDICTION_BOUNDARY = 'jurisdiction_boundary'
    SPHERE_OF_INFLUENCE = 'sphere_of_influence'
    FLOODPLAIN = 'floodplain'
    TIER1_TAZ = 'tier1_taz'
    TIER2_TAZ = 'tier2_taz'
    TRANSIT_AREAS = 'transit_areas'
    PARKS_OPEN_SPACE = 'parks_open_space'

class ScagRegionFixture(RegionFixture):

    def default_remote_db_entity_configurations(self):
        """
            Add the SACOG background. This function is called from default_db_entities so it doesn't
            need to call the parent_fixture's method
        """
        return []

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
            lambda remote_setup: update_or_create_db_entity(config_entity, **remote_setup),
            self.default_remote_db_entity_configurations())

        return default_db_entities + remote_db_entity_setups

