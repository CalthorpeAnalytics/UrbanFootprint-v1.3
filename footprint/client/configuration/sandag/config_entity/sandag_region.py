
from footprint.main.models.geospatial.db_entity_configuration import update_or_create_db_entity
from footprint.client.configuration.fixture import RegionFixture
from footprint.main.models.geospatial.db_entity_keys import DbEntityKey

__author__ = 'calthorpe_associates'

class SandagDbEntityKey(DbEntityKey):
    SCENARIO_A_BOUNDARY = 'scenario_a_boundary'
    SCENARIO_B_BOUNDARY = 'scenario_b_boundary'
    SCENARIO_C_BOUNDARY = 'scenario_c_boundary'
    RTP_TRANSIT_NETWORK_2050 = 'rtp_2050_transit_network'
    RTP_TRANSIT_STOPS_2050 = 'rtp_2050_transit_stops'
    BASE_PARCEL = 'base_parcel_feature'

class SandagRegionFixture(RegionFixture):

    def default_remote_db_entity_configurations(self):
        return []

    def default_db_entities(self):
        """
            Region specific SANDAGE db_entities
        :return:
        """

        config_entity = self.config_entity
        parent_region_fixture = self.parent_fixture
        default_db_entities = parent_region_fixture.default_db_entities()

        remote_db_entity_setups = map(
            lambda remote_setup: update_or_create_db_entity(config_entity, **remote_setup),
            self.default_remote_db_entity_configurations())

        return default_db_entities + remote_db_entity_setups

