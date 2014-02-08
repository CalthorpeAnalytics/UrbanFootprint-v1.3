__author__ = 'calthorpe_associates'


class DbEntityKeys(object):

    #default urbanfootprint tables
    DB_ABSTRACT_BASE_FEATURE = 'base_feature'
    DB_ABSTRACT_BASE_PARCEL_FEATURE = 'base_parcel_feature'
    DB_ABSTRACT_BASE_DEMOGRAPHIC_FEATURE = 'base_demographic_feature'
    DB_ABSTRACT_DEVELOPABLE = 'developable'
    DB_ABSTRACT_INCREMENT_FEATURE = 'increments'
    DB_ABSTRACT_END_STATE_FEATURE = 'end_state'
    DB_ABSTRACT_END_STATE_DEMOGRAPHIC_FEATURE = 'end_state_demographic_feature'
    DB_ABSTRACT_FUTURE_SCENARIO_FEATURE = 'future_scenario_feature'
    DB_ABSTRACT_CPAD_HOLDINGS_FEATURE = 'cpad_holdings'
    DB_ABSTRACT_CENSUS_BLOCK = 'census_block'
    DB_ABSTRACT_CENSUS_BLOCKGROUP = 'census_blockgroup'
    DB_ABSTRACT_CENSUS_TRACT = 'census_tract'
    DB_ABSTRACT_FISCAL_FEATURE = 'fiscal'

    #VMT tables include both base and future versions
    DB_ABSTRACT_VMT_FEATURE = 'vmt_feature'
    DB_ABSTRACT_VMT_QUARTER_MILE_BUFFER_FEATURE = 'vmt_quarter_mile_buffer_feature'
    DB_ABSTRACT_VMT_ONE_MILE_BUFFER_FEATURE = 'vmt_one_mile_buffer_feature'
    DB_ABSTRACT_VMT_VARIABLE_BUFFER_FEATURE = 'vmt_variable_buffer_feature'

    DB_ABSTRACT_VMT_FUTURE_TRIP_LENGTHS_FEATURE = 'vmt_future_trip_lengths_feature'
    DB_ABSTRACT_VMT_BASE_TRIP_LENGTHS_FEATURE = 'vmt_base_trip_lengths_feature'

    #scag specific tables
    DB_ABSTRACT_SCAG_EXISTING_LAND_USE_PARCEL_SOURCE = 'scag_existing_land_use_parcels'
    DB_ABSTRACT_GENERAL_PLAN_FEATURE = 'general_plan_parcels'
    DB_ABSTRACT_PRIMARY_SPZ_SOURCE = 'primary_spz'
    DB_ABSTRACT_JURISDICTION_BOUNDARY = 'jurisdiction_boundary'
    DB_ABSTRACT_SPHERE_OF_INFLUENCE = 'sphere_of_influence'
    DB_ABSTRACT_FLOODPLAIN = 'floodplain'
    DB_ABSTRACT_TIER1_TAZ = 'tier1_taz'
    DB_ABSTRACT_TIER2_TAZ = 'tier2_taz'
    DB_ABSTRACT_TRANSIT_AREAS = 'transit_areas'
    DB_ABSTRACT_PARKS_OPEN_SPACE = 'parks_open_space'

    #sacog specfic tables
    DB_ABSTRACT_SACOG_EXISTING_LAND_USE_PARCEL_SOURCE = 'sacog_existing_land_use_parcels'
    DB_ABSTRACT_STREAM_FEATURE = 'streams'
    DB_ABSTRACT_VERNAL_POOL_FEATURE = 'vernal_pools'
    DB_ABSTRACT_WETLAND_FEATURE = 'wetlands'
    DB_ABSTRACT_HARDWOOD_FEATURE = 'hardwoods'
    DB_ABSTRACT_LIGHT_RAIL_FEATURE = 'light_rail'
    DB_ABSTRACT_LIGHT_RAIL_STOPS_FEATURE = 'light_rail_stops'
    DB_ABSTRACT_LIGHT_RAIL_STOPS_ONE_MILE_FEATURE = 'light_rail_stops_one_mile'
    DB_ABSTRACT_LIGHT_RAIL_STOPS_HALF_MILE_FEATURE = 'light_rail_stops_half_mile'
    DB_ABSTRACT_LIGHT_RAIL_STOPS_QUARTER_MILE_FEATURE = 'light_rail_stops_quarter_mile'

    #sandag specific tables
    DB_ABSTRACT_SANDAG_SCENARIO_B_BOUNDARY = 'scenario_b_boundary'
    DB_ABSTRACT_SANDAG_SCENARIO_C_BOUNDARY = 'scenario_c_boundary'
    DB_ABSTRACT_SANDAG_2050_RTP_TRANSIT_NETWORK = 'rtp_2050_transit_network'
    DB_ABSTRACT_SANDAG_2050_RTP_TRANSIT_STOPS = 'rtp_2050_transit_stops'

    DB_PLACETYPES = 'placetypes'


