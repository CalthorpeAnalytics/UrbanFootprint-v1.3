__author__ = 'calthorpe'


RESIDENTIAL_TYPES = ['du_detsf_ll', 'du_detsf_sl', 'du_attsf', 'du_mf']

COMMERCIAL_TYPES = ['retail_services', 'restaurant', 'accommodation', 'other_services', 'office_services', 'education',
                    'public_admin', 'medical_services', 'wholesale', 'transport_warehousing', 'construction', 'utilities',
                    'manufacturing', 'extraction', 'military', 'agriculture']

WATER_TYPES = ['indoor', 'outdoor']

POLICY_STRATA = dict(
    base=['2020', '2035', '2050'],
    new=['2020', '2035', '2050'])

NEW_EFFICIENCY = dict(
    residential=['residential_new_retrofit'],
    commercial=['commercial_new_retrofit'])

BASE_EFFICIENCY = dict(
    residential=['residential_base_retrofit', 'residential_base_replacement'],
    commercial=['commercial_base_retrofit', 'commercial_base_replacement'])

WATER_OUTPUT_FIELDS = ['id', 'evapotranspiration_zone', 'pop', 'hh', 'emp', 'total_water_use', 'residential_water_use',
                       'commercial_water_use', 'residential_indoor_water_use', 'commercial_indoor_water_use',
                       'residential_outdoor_water_use', 'commercial_outdoor_water_use']


