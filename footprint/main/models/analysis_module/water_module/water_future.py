from footprint.main.models.analysis_module.water_module.water_keys import RESIDENTIAL_TYPES, COMMERCIAL_TYPES

__author__ = 'calthorpe'



def run_incremental_water_calculations(policy_config, water_dict, policy_assumptions):
    
    average_efficiency = 1 - ((policy_config['previous_efficiency_reduction'] +
        policy_config['efficiency_reduction']) / 2)
    
    if policy_config['use_key'] == 'residential':
        types = RESIDENTIAL_TYPES
    else:
        types = COMMERCIAL_TYPES
        
    if policy_config['policy_strata'] =='base':
        rate_type = 'redev'
    else:
        rate_type = 'new'

    if policy_config['water_type'] == 'outdoor':
        types = ['residential_irrigated_sqft', 'commercial_irrigated_sqft']

        for type in types:
            #residential new retrofit units for time increment
            if rate_type == 'new':

                #calculates the number of units for each policy type impacting new units for a given year and water type
                water_dict['{0}_{1}_increment_{2}_units_{3}'.format(type, policy_config['policy_name'], policy_config['water_type'], policy_config['year'])] = \
                    policy_config['year_increment'] * water_dict['{0}_{1}_rate'.format(type, rate_type)]\
                    - (water_dict['{0}_{1}_rate'.format(type, rate_type)] * policy_config['year_increment']\
                    * pow((1 - policy_config['turnover_rate']), policy_config['year_increment']))

                water_dict['{0}_{1}_increment_{2}_use_{3}'.format(type, policy_config['policy_name'], policy_config['water_type'], policy_config['year'])] = \
                    water_dict['{0}_{1}_increment_{2}_units_{3}'.format(type, policy_config['policy_name'], policy_config['water_type'], policy_config['year'])] * average_efficiency * water_dict['annual_evapotranspiration']

                #sums individual policy units and water use by year for all policy impacted units for all policies
                water_dict['{0}_{1}_policy_{2}_units_{3}'.format(type, policy_config['policy_strata'], policy_config['water_type'], policy_config['year'])] = \
                    water_dict['{0}_{1}_policy_{2}_units_{3}'.format(type, policy_config['policy_strata'], policy_config['water_type'], policy_config['year'])] + \
                    water_dict['{0}_{1}_increment_{2}_units_{3}'.format(type, policy_config['policy_name'],
                                                                         policy_config['water_type'], policy_config['year'])]

                #sums new individual policy units for all policy impacted new units for all policies for all years
                water_dict['{0}_new_policy_{1}_units'.format(type, policy_config['water_type'])] = \
                    water_dict['{0}_new_policy_{1}_units'.format(type, policy_config['water_type'])] + \
                    water_dict['{0}_{1}_increment_{2}_units_{3}'.format(type, policy_config['policy_name'],
                                                                         policy_config['water_type'], policy_config['year'])]

                #sums new individual policy use for all policy impacted new units for all policies for all years
                water_dict['{0}_new_policy_{1}_use'.format(type, policy_config['water_type'])] = \
                    water_dict['{0}_new_policy_{1}_use'.format(type, policy_config['water_type'])] + \
                    water_dict['{0}_{1}_increment_{2}_use_{3}'.format(type, policy_config['policy_name'],
                                                                         policy_config['water_type'], policy_config['year'])]

            else:
                #calculates the number of units for each policy type impacting base units for a given year and water type
                water_dict['{0}_{1}_increment_{2}_units_{3}'.format(type, policy_config['policy_name'], policy_config['water_type'], policy_config['year'])] = \
                    (water_dict['{0}_base'.format(type, rate_type)] - (policy_config['year_increment'] * \
                    water_dict['{0}_{1}_rate'.format(type, rate_type)])) - \
                    ((water_dict['{0}_base'.format(type, rate_type)] - (policy_config['year_increment'] * \
                    water_dict['{0}_{1}_rate'.format(type, rate_type)])) * \
                    pow((1 - policy_config['turnover_rate']), policy_config['year_increment']))

                water_dict['{0}_{1}_increment_{2}_use_{3}'.format(type, policy_config['policy_name'],
                    policy_config['water_type'], policy_config['year'])] = water_dict['{0}_{1}_increment_{2}_units_{3}'.\
                    format(type, policy_config['policy_name'], policy_config['water_type'], policy_config['year'])] * \
                    average_efficiency * water_dict['annual_evapotranspiration']

                water_dict['{0}_base_policy_{1}_units_{2}'.format(type, policy_config['water_type'], policy_config['year'])] = \
                    water_dict['{0}_base_policy_{1}_units_{2}'.format(type, policy_config['water_type'], policy_config['year'])] + \
                    water_dict['{0}_{1}_increment_{2}_units_{3}'.format(type, policy_config['policy_name'],
                                                                         policy_config['water_type'], policy_config['year'])]

                water_dict['{0}_base_policy_{1}_units'.format(type, policy_config['water_type'])] = \
                    water_dict['{0}_base_policy_{1}_units'.format(type, policy_config['water_type'])] + \
                    water_dict['{0}_{1}_increment_{2}_units_{3}'.format(type, policy_config['policy_name'],
                                                                         policy_config['water_type'], policy_config['year'])]

                water_dict['{0}_base_policy_{1}_use'.format(type, policy_config['water_type'])] = \
                    water_dict['{0}_base_policy_{1}_use'.format(type, policy_config['water_type'])] + \
                    water_dict['{0}_{1}_increment_{2}_use_{3}'.format(type, policy_config['policy_name'],
                                                                         policy_config['water_type'], policy_config['year'])]

    else:
        for type in types:
            #residential new retrofit units for time increment
            if rate_type == 'new':

                #calculates the number of units for each policy type impacting new units for a given year and water type
                water_dict['{0}_{1}_increment_{2}_units_{3}'.format(type, policy_config['policy_name'], policy_config['water_type'], policy_config['year'])] = \
                    policy_config['year_increment'] * water_dict['{0}_{1}_rate'.format(type, rate_type)]\
                    - (water_dict['{0}_{1}_rate'.format(type, rate_type)] * policy_config['year_increment']\
                    * pow((1 - policy_config['turnover_rate']), policy_config['year_increment']))

                water_dict['{0}_{1}_increment_{2}_use_{3}'.format(type, policy_config['policy_name'], policy_config['water_type'], policy_config['year'])] = \
                    water_dict['{0}_{1}_increment_{2}_units_{3}'.format(type, policy_config['policy_name'], policy_config['water_type'], policy_config['year'])] * average_efficiency * policy_assumptions['{0}_{1}'.format(type, policy_config['water_type'])]

                #sums individual policy units and water use by year for all policy impacted units for all policies
                water_dict['{0}_{1}_policy_{2}_units_{3}'.format(type, policy_config['policy_strata'], policy_config['water_type'], policy_config['year'])] = \
                    water_dict['{0}_{1}_policy_{2}_units_{3}'.format(type, policy_config['policy_strata'], policy_config['water_type'], policy_config['year'])] + \
                    water_dict['{0}_{1}_increment_{2}_units_{3}'.format(type, policy_config['policy_name'],
                                                                         policy_config['water_type'], policy_config['year'])]

                #sums new individual policy units for all policy impacted new units for all policies for all years
                water_dict['{0}_new_policy_{1}_units'.format(type, policy_config['water_type'])] = \
                    water_dict['{0}_new_policy_{1}_units'.format(type, policy_config['water_type'])] + \
                    water_dict['{0}_{1}_increment_{2}_units_{3}'.format(type, policy_config['policy_name'],
                                                                         policy_config['water_type'], policy_config['year'])]

                #sums new individual policy use for all policy impacted new units for all policies for all years
                water_dict['{0}_new_policy_{1}_use'.format(type, policy_config['water_type'])] = \
                    water_dict['{0}_new_policy_{1}_use'.format(type, policy_config['water_type'])] + \
                    water_dict['{0}_{1}_increment_{2}_use_{3}'.format(type, policy_config['policy_name'],
                                                                         policy_config['water_type'], policy_config['year'])]

            else:
                #calculates the number of units for each policy type impacting base units for a given year and water type
                water_dict['{0}_{1}_increment_{2}_units_{3}'.format(type, policy_config['policy_name'], policy_config['water_type'], policy_config['year'])] = \
                    (water_dict['{0}_base'.format(type, rate_type)] - (policy_config['year_increment'] * \
                    water_dict['{0}_{1}_rate'.format(type, rate_type)])) - \
                    ((water_dict['{0}_base'.format(type, rate_type)] - (policy_config['year_increment'] * \
                    water_dict['{0}_{1}_rate'.format(type, rate_type)])) * \
                    pow((1 - policy_config['turnover_rate']), policy_config['year_increment']))

                water_dict['{0}_{1}_increment_{2}_use_{3}'.format(type, policy_config['policy_name'],
                    policy_config['water_type'], policy_config['year'])] = water_dict['{0}_{1}_increment_{2}_units_{3}'.\
                    format(type, policy_config['policy_name'], policy_config['water_type'], policy_config['year'])] * \
                    average_efficiency * policy_assumptions['{0}_{1}'.format(type, policy_config['water_type'])]

                water_dict['{0}_base_policy_{1}_units_{2}'.format(type, policy_config['water_type'], policy_config['year'])] = \
                    water_dict['{0}_base_policy_{1}_units_{2}'.format(type, policy_config['water_type'], policy_config['year'])] + \
                    water_dict['{0}_{1}_increment_{2}_units_{3}'.format(type, policy_config['policy_name'],
                                                                         policy_config['water_type'], policy_config['year'])]

                water_dict['{0}_base_policy_{1}_units'.format(type, policy_config['water_type'])] = \
                    water_dict['{0}_base_policy_{1}_units'.format(type, policy_config['water_type'])] + \
                    water_dict['{0}_{1}_increment_{2}_units_{3}'.format(type, policy_config['policy_name'],
                                                                         policy_config['water_type'], policy_config['year'])]

                water_dict['{0}_base_policy_{1}_use'.format(type, policy_config['water_type'])] = \
                    water_dict['{0}_base_policy_{1}_use'.format(type, policy_config['water_type'])] + \
                    water_dict['{0}_{1}_increment_{2}_use_{3}'.format(type, policy_config['policy_name'],
                                                                         policy_config['water_type'], policy_config['year'])]
        
    return water_dict
        
        
def sum_incremental_water_use(policy_config, water_dict, policy_assumptions):



    for use in policy_config['efficiency_dict'].keys():

        previous_calibration_year = policy_config['base_year']

        for year in sorted(policy_config['years'], key=int):

            increment_ratio = (year - float(previous_calibration_year)) / policy_config['scenario_increment']

            new_efficiency_reduction = policy_assumptions['{0}_new_efficiency_{1}'.format(use,
                                            policy_config['water_type'])].values.get(str(int(year)))

            if previous_calibration_year == policy_config['base_year']:
                previous_new_efficiency_reduction = float(0)
            else:
                previous_new_efficiency_reduction = policy_assumptions['{0}_new_efficiency_{1}'.format(use,
                                                policy_config['water_type'])].values.get(str(int(previous_calibration_year)))

            year_increment = float(year) - float(previous_calibration_year)

            average_efficiency = 1 - ((previous_new_efficiency_reduction + new_efficiency_reduction) / 2)


            if policy_config['water_type'] == 'outdoor':
                types = ['residential_irrigated_sqft', 'commercial_irrigated_sqft']

                for type in types:

                    water_dict['{0}_new_no_policy_{1}_units'.format(type, policy_config['water_type'])] = \
                        water_dict['{0}_new_no_policy_{1}_units'.format(type, policy_config['water_type'])] + \
                        ((water_dict['{0}_new_rate'.format(type)] * year_increment) - \
                        float(water_dict['{0}_new_policy_{1}_units_{2}'.format(type, policy_config['water_type'], str(int(year)))]))

                    water_dict['{0}_new_no_policy_{1}_use'.format(type, policy_config['water_type'])] = \
                        water_dict['{0}_new_no_policy_{1}_use'.format(type, policy_config['water_type'])] + \
                        ((water_dict['{0}_new_rate'.format(type)] * year_increment) - \
                        float(water_dict['{0}_new_policy_{1}_units_{2}'.format(type, policy_config['water_type'], str(int(year)))])) * \
                        water_dict['annual_evapotranspiration'] * average_efficiency


                    water_dict['{0}_base_no_policy_{1}_use'.format(type, policy_config['water_type'])] = \
                        water_dict['{0}_base_no_policy_{1}_use'.format(type, policy_config['water_type'])] + \
                        ((water_dict['{0}_base'.format(type)] - (water_dict['{0}_redev_rate'.format(type)] * year_increment) - \
                        float(water_dict['{0}_base_policy_{1}_units_{2}'.format(type, policy_config['water_type'], str(int(year)))])) * \
                        water_dict['annual_evapotranspiration']) * increment_ratio

            else:

                if use =='residential':
                    use_types = policy_config['res_types']
                else:
                    use_types = policy_config['com_types']

                for type in use_types:

                    water_dict['{0}_new_no_policy_{1}_units'.format(type, policy_config['water_type'])] = \
                        water_dict['{0}_new_no_policy_{1}_units'.format(type, policy_config['water_type'])] + \
                        ((water_dict['{0}_new_rate'.format(type)] * year_increment) - \
                        float(water_dict['{0}_new_policy_{1}_units_{2}'.format(type, policy_config['water_type'], str(int(year)))]))

                    water_dict['{0}_new_no_policy_{1}_use'.format(type, policy_config['water_type'])] = \
                        water_dict['{0}_new_no_policy_{1}_use'.format(type, policy_config['water_type'])] + \
                        ((water_dict['{0}_new_rate'.format(type)] * year_increment) - \
                        float(water_dict['{0}_new_policy_{1}_units_{2}'.format(type, policy_config['water_type'], str(int(year)))])) * \
                        policy_assumptions['{0}_{1}'.format(type, policy_config['water_type'])] * average_efficiency


                    water_dict['{0}_base_no_policy_{1}_use'.format(type, policy_config['water_type'])] = \
                        water_dict['{0}_base_no_policy_{1}_use'.format(type, policy_config['water_type'])] + \
                        ((water_dict['{0}_base'.format(type)] - (water_dict['{0}_redev_rate'.format(type)] * year_increment) - \
                        float(water_dict['{0}_base_policy_{1}_units_{2}'.format(type, policy_config['water_type'], str(int(year)))])) * \
                        policy_assumptions['{0}_{1}'.format(type, policy_config['water_type'])]) * increment_ratio


            previous_calibration_year = year

    return water_dict



def run_final_water_calcs(policy_config, water_dict):
    
    water_dict['residential_water_use'.format(policy_config['water_type'])] = float(0)
    water_dict['commercial_water_use'.format(policy_config['water_type'])] = float(0)

    if 'outdoor' in policy_config['water_type']:
        outdoor_types = ['residential_irrigated_sqft', 'commercial_irrigated_sqft']
        
        for type in outdoor_types:
            water_dict['{0}_new_{1}_use'.format(type, policy_config['water_type'])] = \
                water_dict['{0}_new_no_policy_{1}_use'.format(type, policy_config['water_type'])] + \
                water_dict['{0}_new_policy_{1}_use'.format(type, policy_config['water_type'])]
            
            water_dict['{0}_base_{1}_use'.format(type, policy_config['water_type'])] = \
                water_dict['{0}_base_no_policy_{1}_use'.format(type, policy_config['water_type'])] + \
                water_dict['{0}_base_policy_{1}_use'.format(type, policy_config['water_type'])]

            if 'residential' in type:
                water_dict['residential_outdoor_water_use'] = \
                    water_dict['{0}_new_{1}_use'.format(type, policy_config['water_type'])] + \
                    water_dict['{0}_base_{1}_use'.format(type, policy_config['water_type'])]
            else:
                water_dict['commercial_outdoor_water_use'] = \
                    water_dict['{0}_new_{1}_use'.format(type, policy_config['water_type'])] + \
                    water_dict['{0}_base_{1}_use'.format(type, policy_config['water_type'])]
        
    else:
        for type in policy_config['use_types']:
            water_dict['{0}_new_{1}_use'.format(type, policy_config['water_type'])] = \
                water_dict['{0}_new_no_policy_{1}_use'.format(type, policy_config['water_type'])] + \
                water_dict['{0}_new_policy_{1}_use'.format(type, policy_config['water_type'])]
            
            water_dict['{0}_base_{1}_use'.format(type, policy_config['water_type'])] = \
                water_dict['{0}_base_no_policy_{1}_use'.format(type, policy_config['water_type'])] + \
                water_dict['{0}_base_policy_{1}_use'.format(type, policy_config['water_type'])]
            
            water_dict['{0}_{1}_use'.format(type, policy_config['water_type'])] = \
                water_dict['{0}_new_{1}_use'.format(type, policy_config['water_type'])] + \
                water_dict['{0}_base_{1}_use'.format(type, policy_config['water_type'])]
        
        for type in policy_config['res_types']:
            water_dict['residential_{0}_water_use'.format(policy_config['water_type'])] = \
                water_dict['residential_{0}_water_use'.format(policy_config['water_type'])] + \
                water_dict['{0}_{1}_use'.format(type, policy_config['water_type'])]
            
        for type in policy_config['com_types']:
            water_dict['commercial_{0}_water_use'.format(policy_config['water_type'])] = water_dict['commercial_{0}_water_use'.format(policy_config['water_type'])] + \
                 water_dict['{0}_{1}_use'.format(type, policy_config['water_type'])]


    
    water_dict['residential_water_use'.format(policy_config['water_type'])] = water_dict['residential_indoor_water_use'] + \
        water_dict['residential_outdoor_water_use']
            
    water_dict['commercial_water_use'.format(policy_config['water_type'])] = water_dict['commercial_indoor_water_use'] + \
        water_dict['commercial_outdoor_water_use']

    water_dict['total_water_use'.format(policy_config['water_type'])] = \
        water_dict['residential_water_use'.format(policy_config['water_type'])] + \
        water_dict['commercial_water_use'.format(policy_config['water_type'])]

    return water_dict