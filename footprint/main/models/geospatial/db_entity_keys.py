from footprint.main.models.keys.keys import Keys

__author__ = 'calthorpe'


class DbEntityKey(Keys):
    """
        A Key class to key DbEntity instances
    """
    class Fab(Keys.Fab):
        @classmethod
        def prefix(cls):
            # No prefix since these are so fundamental and are used to create table names,
            # so we don't want them any longer than needed to clearly describe the db_entity
            return ''
    # Preconfigured keys
    # Some of these have the word feature in order to match the generated data tables
    # They should all be normalized to remove 'feature'
    BASE = 'base_feature'
    DEFAULT_DEVELOPABLE = 'default_developable'
    CPAD_HOLDINGS = 'cpad_holdings'
    CENSUS_TRACT = 'census_tract'
    CENSUS_BLOCKGROUP = 'census_blockgroup'
    CENSUS_BLOCK = 'census_block'
    BASE_DEMOGRAPHIC = 'base_demographic_feature'
    BASE_AGRICULTURE = 'base_agriculture_feature'
    CLIMATE_ZONE = 'climate_zones'
    FUTURE_SCENARIO = 'future_scenario_feature'
    INCREMENT = 'increments'
    END_STATE = 'end_state'
    FUTURE_AGRICULTURE = 'future_agriculture_feature'
    DEVELOPABLE = 'developable'
    END_STATE_DEMOGRAPHIC = 'end_state_demographic_feature'
    FISCAL = 'fiscal'
    VMT = 'vmt_feature'
    VMT_FUTURE_TRIP_LENGTHS = 'vmt_future_trip_lengths_feature'
    VMT_BASE_TRIP_LENGTHS = 'vmt_base_trip_lengths_feature'
    VMT_QUARTER_MILE_BUFFER = 'vmt_quarter_mile_buffer_feature'
    VMT_ONE_MILE_BUFFER = 'vmt_one_mile_buffer_feature'
    VMT_VARIABLE_BUFFER = 'vmt_variable_buffer_feature'
    ENERGY = 'energy'
    WATER = 'water'
    LAND_CONSUMPTION = 'land_consumption'