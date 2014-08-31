__author__ = 'calthorpe'


RESIDENTIAL_TYPES = ['du_detsf_ll', 'du_detsf_sl', 'du_attsf', 'du_mf']

COMMERCIAL_TYPES = ['retail_services', 'restaurant', 'accommodation', 'other_services', 'office_services', 'education',
                    'public_admin', 'medical_services', 'wholesale', 'transport_warehousing']

ENERGY_TYPES = ['gas', 'electricity']

POLICY_STRATA = dict(
    base=['2020', '2035', '2050'],
    new=['2020', '2035', '2050'])

NEW_EFFICIENCY = dict(
    residential=['residential_new_retrofit'],
    commercial=['commercial_new_retrofit'])

BASE_EFFICIENCY = dict(
    residential=['residential_base_retrofit', 'residential_base_replacement'],
    commercial=['commercial_base_retrofit', 'commercial_base_replacement'])

ENERGY_OUTPUT_FIELDS = ['id', 'title24_zone', 'fcz_zone', 'total_commercial_sqft', 'emp', 'hh', 'total_gas_use',
                        'total_electricity_use', 'residential_gas_use', 'commercial_gas_use',
                        'residential_electricity_use', 'commercial_electricity_use', 'du_detsf_ll_gas_use', 
                        'du_detsf_sl_gas_use', 'du_attsf_gas_use', 'du_mf_gas_use',  'retail_services_gas_use', 
                        'restaurant_gas_use', 'accommodation_gas_use', 'other_services_gas_use',
                        'office_services_gas_use', 'education_gas_use','public_admin_gas_use',
                        'medical_services_gas_use', 'wholesale_gas_use', 'transport_warehousing_gas_use',
                        'du_detsf_ll_electricity_use', 'du_detsf_sl_electricity_use', 'du_attsf_electricity_use',
                        'du_mf_electricity_use', 'retail_services_electricity_use', 'restaurant_electricity_use',
                        'accommodation_electricity_use', 'other_services_electricity_use',
                        'office_services_electricity_use', 'education_electricity_use','public_admin_electricity_use',
                        'medical_services_electricity_use', 'wholesale_electricity_use',
                        'transport_warehousing_electricity_use']


