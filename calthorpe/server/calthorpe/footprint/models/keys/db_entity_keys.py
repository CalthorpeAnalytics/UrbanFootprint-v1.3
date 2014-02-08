__author__ = 'calthorpe'


class DbEntityKeys(object):

    #default urbanfootprint tables
    DB_ABSTRACT_BASE_FEATURE = 'base_feature'
    DB_ABSTRACT_BASE_PARCEL_FEATURE = 'base_parcel_feature'
    DB_ABSTRACT_DEVELOPABLE = 'developable'
    DB_ABSTRACT_INCREMENT_FEATURE = 'increments'
    DB_ABSTRACT_END_STATE_FEATURE = 'end_state'
    DB_ABSTRACT_FUTURE_SCENARIO_FEATURE = 'future_scenario_feature'
    DB_ABSTRACT_CPAD_HOLDINGS_FEATURE = 'cpad_holdings'
    DB_ABSTRACT_CENSUS_BLOCK = 'census_block'
    DB_ABSTRACT_CENSUS_BLOCKGROUP = 'census_blockgroup'
    DB_ABSTRACT_CENSUS_TRACT = 'census_tract'

    #scag specific tables
    DB_ABSTRACT_SCAG_EXISTING_LAND_USE_PARCEL_SOURCE = 'existing_land_use_parcels'
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
    DB_ABSTRACT_SACOG_EXISTING_LAND_USE_PARCEL_SOURCE = 'existing_land_use_parcels'
    DB_ABSTRACT_STREAM_FEATURE = 'streams'
    DB_ABSTRACT_VERNAL_POOL_FEATURE = 'vernal_pools'
    DB_ABSTRACT_WETLAND_FEATURE = 'wetlands'

    #sandag specific tables
    DB_ABSTRACT_SANDAG_SCENARIO_B_BOUNDARY = 'scenario_b_boundary'
    DB_ABSTRACT_SANDAG_SCENARIO_C_BOUNDARY = 'scenario_c_boundary'
    DB_ABSTRACT_SANDAG_2050_RTP_TRANSIT_NETWORK = 'rtp_2050_transit_network'
    DB_ABSTRACT_SANDAG_2050_RTP_TRANSIT_STOPS = 'rtp_2050_transit_stops'

    DB_PLACETYPES = 'placetypes'


