__author__ = 'calthorpe'


class BuiltFormKeys(object):
    """
    Keys for used by Built Forms
    """

    BUILDING_USE_RESIDENTIAL = 'Residential'
    BUILDING_USE_OFFICE = 'Office'
    BUILDING_USE_RETAIL = 'Retail'
    BUILDING_USE_INDUSTRIAL = 'Industrial'

    INFRASTRUCTURE_STREET = PLACETYPE_COMPONENT_STREET = 'Street'
    INFRASTRUCTURE_UTILITIES = PLACETYPE_COMPONENT_UTILITY = 'Utility'
    INFRASTRUCTURE_PARK = PLACETYPE_COMPONENT_PARK = 'Park'
    INFRASTRUCTURE_TYPES = [INFRASTRUCTURE_STREET, INFRASTRUCTURE_UTILITIES, INFRASTRUCTURE_PARK]

    BUILDINGTYPE_CIVIC = 'Civic'
    BUILDINGTYPE_RESIDENTIAL = 'Residential'
    BUILDINGTYPE_DETACHED_RESIDENTIAL = 'Detached Residential'
    BUILDINGTYPE_ATTACHED_AND_MULTIFAMILY = 'Attached and Multifamily Residential'
    BUILDINGTYPE_OFFICE_INDUSTRIAL = 'Office/Industrial'
    BUILDINGTYPE_COMMERCIAL_RETAIL = 'Commercial/Retail'
    BUILDINGTYPE_MIXED_USE = 'Mixed Use'
    BUILDINGTYPE_INSTITUTIONAL = 'Institutional'
    BUILDINGTYPE_BLANK = 'Blank'
    BUILDINGTYPE_AGRICULTURAL = 'Agricultural'

    RESIDENTIAL_BUILDINGTYPE_CATEGORIES = [
        BUILDINGTYPE_RESIDENTIAL, BUILDINGTYPE_DETACHED_RESIDENTIAL,
        BUILDINGTYPE_ATTACHED_AND_MULTIFAMILY
    ]

    EMPLOYMENT_BUILDINGTYPE_CATEGORIES = [
        BUILDINGTYPE_AGRICULTURAL,
        BUILDINGTYPE_OFFICE_INDUSTRIAL, BUILDINGTYPE_COMMERCIAL_RETAIL, BUILDINGTYPE_INSTITUTIONAL
    ]

    NET_COMPONENTS = [BUILDINGTYPE_RESIDENTIAL,
                      BUILDINGTYPE_DETACHED_RESIDENTIAL,
                      BUILDINGTYPE_ATTACHED_AND_MULTIFAMILY,
                      BUILDINGTYPE_OFFICE_INDUSTRIAL,
                      BUILDINGTYPE_COMMERCIAL_RETAIL,
                      BUILDINGTYPE_MIXED_USE,
                      BUILDINGTYPE_INSTITUTIONAL,
                      BUILDINGTYPE_BLANK,
                      BUILDINGTYPE_AGRICULTURAL]

    GROSS_COMPONENTS = INFRASTRUCTURE_TYPES + [BUILDINGTYPE_CIVIC]

    COMPONENT_CATEGORIES = NET_COMPONENTS + GROSS_COMPONENTS

    ATTACHED_RESIDENTIAL = 'Attached Single Family'
    MULTIFAMILY_2_TO_4 = 'Multifamily 2 To 4'
    MULTIFAMILY_5P = 'Multifamily 5 Plus'
    LARGE_LOT_SINGLE_FAMILY = 'Single Family Large Lot'
    SMALL_LOT_SINGLE_FAMILY = 'Single Family Small Lot'

    MULTIFAMILY_AND_ATTACHED = [ATTACHED_RESIDENTIAL, MULTIFAMILY_2_TO_4, MULTIFAMILY_5P]
    DETACHED_RESIDENTIAL = [LARGE_LOT_SINGLE_FAMILY, SMALL_LOT_SINGLE_FAMILY]

    RESIDENTIAL_CATEGORY = 'Residential'
    RETAIL_CATEGORY = 'Retail'
    OFFICE_CATEGORY = 'Office'
    INDUSTRIAL_CATEGORY = 'Industrial'
    AGRICULTURAL_CATEGORY = 'Agricultural'
    MILITARY_CATEGORY = 'Armed Forces'

    RESIDENTIAL_SUBCATEGORIES = MULTIFAMILY_AND_ATTACHED + DETACHED_RESIDENTIAL
    ALL_RESIDENTIAL_USES = MULTIFAMILY_AND_ATTACHED + DETACHED_RESIDENTIAL + [RESIDENTIAL_CATEGORY]

    TOP_LEVEL_EMPLOYMENT_CATEGORIES = [RETAIL_CATEGORY,
                                       OFFICE_CATEGORY,
                                       INDUSTRIAL_CATEGORY,
                                       AGRICULTURAL_CATEGORY,
                                       MILITARY_CATEGORY]

    RETAIL_SUBCATEGORIES = ['Retail Services', 'Restaurant', 'Accommodation', 'Arts Entertainment', 'Other Services']
    OFFICE_SUBCATEGORIES = ['Office Services', 'Public Admin', 'Education Services', 'Medical Services']
    INDUSTRIAL_SUBCATEGORIES = ['Manufacturing', 'Wholesale', 'Transport Warehouse', 'Construction Utilities']
    AGRICULTURAL_SUBCATEGORIES = ['Agriculture', 'Extraction']

    BUILDING_USE_DEFINITION_METACATEGORIES = [
        RESIDENTIAL_CATEGORY,
        OFFICE_CATEGORY,
        RETAIL_CATEGORY,
        INDUSTRIAL_CATEGORY,
        AGRICULTURAL_CATEGORY
    ]

    BUILDING_USE_DEFINITION_CATEGORIES = {
        'Retail Services': RETAIL_CATEGORY,
        'Restaurant': RETAIL_CATEGORY,
        'Accommodation': RETAIL_CATEGORY,
        'Arts Entertainment': RETAIL_CATEGORY,
        'Other Services': RETAIL_CATEGORY,

        'Office Services': OFFICE_CATEGORY,
        'Public Admin': OFFICE_CATEGORY,
        'Education Services': OFFICE_CATEGORY,
        'Medical Services': OFFICE_CATEGORY,

        'Manufacturing': INDUSTRIAL_CATEGORY,
        'Wholesale': INDUSTRIAL_CATEGORY,
        'Transport Warehouse': INDUSTRIAL_CATEGORY,
        'Construction Utilities': INDUSTRIAL_CATEGORY,

        'Agriculture': AGRICULTURAL_CATEGORY,
        'Extraction': AGRICULTURAL_CATEGORY,

        'Armed Forces': MILITARY_CATEGORY,

        LARGE_LOT_SINGLE_FAMILY: RESIDENTIAL_CATEGORY,
        SMALL_LOT_SINGLE_FAMILY: RESIDENTIAL_CATEGORY,
        ATTACHED_RESIDENTIAL: RESIDENTIAL_CATEGORY,
        MULTIFAMILY_2_TO_4: RESIDENTIAL_CATEGORY,
        MULTIFAMILY_5P: RESIDENTIAL_CATEGORY,
    }
    BUILDINGTYPE_SOURCE_ID_LOOKUP = {
        'by_name': {
            'Airport': {'fp_id': None, 'source_id': 62},
            'Campus/College High': {'fp_id': 395, 'source_id': 43},
            'Campus/College Low': {'fp_id': 346, 'source_id': 44},
            'Church': {'fp_id': 394, 'source_id': 59},
            'Connected Tourism': {'fp_id': None, 'source_id': 64},
            'Estate Lot': {'fp_id': 352, 'source_id': 21},
            'Garden Apartment': {'fp_id': 373, 'source_id': 16},
            'Health Office': {'fp_id': None, 'source_id': 66},
            'High-Rise Mixed Use': {'fp_id': 344, 'source_id': 2},
            'High-Rise Office': {'fp_id': 351, 'source_id': 25},
            'High-Rise Residential': {'fp_id': 380, 'source_id': 9},
            'Hospital/Civic/Other Institutional': {'fp_id': 400, 'source_id': 45},
            'Hotel High': {'fp_id': 358, 'source_id': 37},
            'Hotel Low': {'fp_id': 378, 'source_id': 38},
            'Industrial High': {'fp_id': 385, 'source_id': 33},
            'Industrial Low': {'fp_id': 347, 'source_id': 34},
            'Large Lot 7500': {'fp_id': 399, 'source_id': 20},
            'Low Density Commercial': {'fp_id': None, 'source_id': 61},
            'Low Intensity Strip Commercial (weighted avg)': {'fp_id': 342, 'source_id': 41},
            'Low-Rise Mixed Use': {'fp_id': 360, 'source_id': 4},
            'Low-Rise Office': {'fp_id': 361, 'source_id': 27},
            'Main Street Commercial (Retail + Office/Medical)': {'fp_id': 396, 'source_id': 28},
            'Main Street Commercial/MU High (3-5 Floors)': {'fp_id': 392, 'source_id': 6},
            'Main Street Commercial/MU Low (1-2 Floors)': {'fp_id': 343, 'source_id': 7},
            'Medium Intensity Strip Commercial (weighted avg)': {'fp_id': 365, 'source_id': 40},
            'Medium Lot 5500': {'fp_id': 353, 'source_id': 19},
            'Mid-Rise Mixed Use': {'fp_id': 357, 'source_id': 3},
            'Mid-Rise Office': {'fp_id': 363, 'source_id': 26},
            'Military General Catch-All': {'fp_id': None, 'source_id': 60},
            'Non-Urban Elementary School': {'fp_id': 387, 'source_id': 47},
            'Non-Urban High School': {'fp_id': 348, 'source_id': 51},
            'Non-Urban Middle School': {'fp_id': 345, 'source_id': 49},
            'Office Park High': {'fp_id': 390, 'source_id': 31},
            'Office Park Low': {'fp_id': 377, 'source_id': 32},
            'Open Space': {'fp_id': None, 'source_id': 65},
            'Park/Recreation': {'fp_id': None, 'source_id': 63},
            'Parking Structure': {'fp_id': 370, 'source_id': 30},
            'Parking Structure+Ground-Floor Retail': {'fp_id': 397, 'source_id': 29},
            'Parking Structure/Mixed Use': {'fp_id': 359, 'source_id': 5},
            'Public Infrastructure': {'fp_id': None, 'source_id': 68},
            'Regional Mall': {'fp_id': 391, 'source_id': 39},
            'Rural Employment': {'fp_id': 389, 'source_id': 42},
            'Rural Ranchette': {'fp_id': 369, 'source_id': 23},
            'Rural Residential': {'fp_id': 382, 'source_id': 22},
            'Skyscraper Mixed Use': {'fp_id': 384, 'source_id': 1},
            'Skyscraper Office': {'fp_id': 362, 'source_id': 24},
            'Skyscraper Residential': {'fp_id': 355, 'source_id': 8},
            'Small Lot 4000': {'fp_id': 354, 'source_id': 18},
            'Standard Podium Multi-Family': {'fp_id': 366, 'source_id': 12},
            'Standard Townhome': {'fp_id': 388, 'source_id': 15},
            'Suburban Civic Complex': {'fp_id': 368, 'source_id': 57},
            'Suburban Multifamily Apt/Condo': {'fp_id': 381, 'source_id': 13},
            'Town Civic Complex': {'fp_id': 372, 'source_id': 56},
            'Town/Branch Library': {'fp_id': 367, 'source_id': 58},
            'Transit/Rail Station': {'fp_id': None, 'source_id': 67},
            'Urban City Hall': {'fp_id': 386, 'source_id': 52},
            'Urban Convention Center': {'fp_id': 374, 'source_id': 55},
            'Urban Courthouse': {'fp_id': 393, 'source_id': 54},
            'Urban Elementary School': {'fp_id': 383, 'source_id': 46},
            'Urban High School': {'fp_id': 356, 'source_id': 50},
            'Urban Mid-Rise Residential': {'fp_id': 349, 'source_id': 10},
            'Urban Middle School': {'fp_id': 350, 'source_id': 48},
            'Urban Podium Multi-Family': {'fp_id': 371, 'source_id': 11},
            'Urban Public Library': {'fp_id': 375, 'source_id': 53},
            'Urban Townhome/Live-Work': {'fp_id': 379, 'source_id': 14},
            'Very Small Lot 3000': {'fp_id': 376, 'source_id': 17},
            'Warehouse High': {'fp_id': 364, 'source_id': 35},
            'Warehouse Low': {'fp_id': 398, 'source_id': 36}
        },

        'by_source_id': {
            1: 'Skyscraper Mixed Use',
            2: 'High-Rise Mixed Use',
            3: 'Mid-Rise Mixed Use',
            4: 'Low-Rise Mixed Use',
            5: 'Parking Structure/Mixed Use',
            6: 'Main Street Commercial/MU High (3-5 Floors)',
            7: 'Main Street Commercial/MU Low (1-2 Floors)',
            8: 'Skyscraper Residential',
            9: 'High-Rise Residential',
            10: 'Urban Mid-Rise Residential',
            11: 'Urban Podium Multi-Family',
            12: 'Standard Podium Multi-Family',
            13: 'Suburban Multifamily Apt/Condo',
            14: 'Urban Townhome/Live-Work',
            15: 'Standard Townhome',
            16: 'Garden Apartment',
            17: 'Very Small Lot 3000',
            18: 'Small Lot 4000',
            19: 'Medium Lot 5500',
            20: 'Large Lot 7500',
            21: 'Estate Lot',
            22: 'Rural Residential',
            23: 'Rural Ranchette',
            24: 'Skyscraper Office',
            25: 'High-Rise Office',
            26: 'Mid-Rise Office',
            27: 'Low-Rise Office',
            28: 'Main Street Commercial (Retail + Office/Medical)',
            29: 'Parking Structure+Ground-Floor Retail',
            30: 'Parking Structure',
            31: 'Office Park High',
            32: 'Office Park Low',
            33: 'Industrial High',
            34: 'Industrial Low',
            35: 'Warehouse High',
            36: 'Warehouse Low',
            37: 'Hotel High',
            38: 'Hotel Low',
            39: 'Regional Mall',
            40: 'Medium Intensity Strip Commercial (weighted avg)',
            41: 'Low Intensity Strip Commercial (weighted avg)',
            42: 'Rural Employment',
            43: 'Campus/College High',
            44: 'Campus/College Low',
            45: 'Hospital/Civic/Other Institutional',
            46: 'Urban Elementary School',
            47: 'Non-Urban Elementary School',
            48: 'Urban Middle School',
            49: 'Non-Urban Middle School',
            50: 'Urban High School',
            51: 'Non-Urban High School',
            52: 'Urban City Hall',
            53: 'Urban Public Library',
            54: 'Urban Courthouse',
            55: 'Urban Convention Center',
            56: 'Town Civic Complex',
            57: 'Suburban Civic Complex',
            58: 'Town/Branch Library',
            59: 'Church',
            60: 'Military General Catch-All',
            61: 'Low Density Commercial',
            62: 'Airport',
            63: 'Park/Recreation',
            64: 'Connected Tourism',
            65: 'Open Space',
            66: 'Health Office',
            67: 'Transit/Rail Station',
            68: 'Public Infrastructure'
        }
    }