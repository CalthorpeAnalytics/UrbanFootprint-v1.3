from footprint.main.models.analysis_module.water_module.water_keys import WATER_TYPES, RESIDENTIAL_TYPES, COMMERCIAL_TYPES

__author__ = 'calthorpe'


def calculate_base_water(water_dict, policy_assumptions):
    
    types = RESIDENTIAL_TYPES + COMMERCIAL_TYPES

    water_dict['residential_water_use'] = float(0)
    water_dict['commercial_water_use'] = float(0)

    for water_type in WATER_TYPES:

        water_dict['residential_{0}_water_use'.format(water_type)] = float(0)
        water_dict['commercial_{0}_water_use'.format(water_type)] = float(0)

        if 'outdoor' in water_type:
            water_dict['residential_{0}_water_use'.format(water_type)] = water_dict['residential_irrigated_sqft'] * \
               water_dict['annual_evapotranspiration']
            water_dict['commercial_{0}_water_use'.format(water_type)] = water_dict['commercial_irrigated_sqft'] * \
               water_dict['annual_evapotranspiration']
        else:
            for type in types:
                water_dict['{0}_{1}_water_use'.format(type, water_type)] = \
                    water_dict['{0}'.format(type)] * \
                    policy_assumptions['{0}_{1}'.format(type, water_type)]
            
            for type in RESIDENTIAL_TYPES:
                water_dict['residential_{0}_water_use'.format(water_type)] = \
                    water_dict['residential_{0}_water_use'.format(water_type)] + \
                    water_dict['{0}_{1}_water_use'.format(type, water_type)]
        
            for type in COMMERCIAL_TYPES:
                water_dict['commercial_{0}_water_use'.format(water_type)] = \
                    water_dict['commercial_{0}_water_use'.format(water_type)] +  \
                    water_dict['{0}_{1}_water_use'.format(type, water_type)]
                
            water_dict['residential_water_use'] = water_dict['residential_water_use'] + \
                 water_dict['residential_{0}_water_use'.format(water_type)]
            
            water_dict['commercial_water_use'] = water_dict['commercial_water_use'] + \
                 water_dict['commercial_{0}_water_use'.format(water_type)]

            water_dict['total_{0}_water_use'.format(water_type)] = \
                water_dict['residential_{0}_water_use'.format(water_type)] + \
                water_dict['commercial_{0}_water_use'.format(water_type)]

    water_dict['residential_water_use'] = water_dict['residential_water_use'] + \
         water_dict['residential_outdoor_water_use']

    water_dict['commercial_water_use'] = water_dict['commercial_water_use'] + \
         water_dict['commercial_outdoor_water_use']

    water_dict['total_outdoor_water_use'] = \
        water_dict['residential_outdoor_water_use'] + \
        water_dict['commercial_outdoor_water_use']

    water_dict['total_water_use'] = \
        water_dict['residential_water_use'] + \
        water_dict['commercial_water_use']

    return water_dict