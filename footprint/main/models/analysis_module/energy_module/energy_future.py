from footprint.main.models.analysis_module.energy_module.energy_keys import RESIDENTIAL_TYPES, COMMERCIAL_TYPES

__author__ = 'calthorpe'



def run_incremental_energy_calculations(policy_config, energy_dict):
    
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

    for type in types:
        #residential new retrofit units for time increment
        if rate_type == 'new':

            #calculates the number of units for each policy type impacting new units for a given year and energy type
            energy_dict['{0}_{1}_increment_{2}_units_{3}'.format(type, policy_config['policy_name'], policy_config['energy_type'], policy_config['year'])] = \
                policy_config['year_increment'] * energy_dict['{0}_{1}_rate'.format(type, rate_type)]\
                - (energy_dict['{0}_{1}_rate'.format(type, rate_type)] * policy_config['year_increment']\
                * pow((1 - policy_config['turnover_rate']), policy_config['year_increment']))

            energy_dict['{0}_{1}_increment_{2}_use_{3}'.format(type, policy_config['policy_name'], policy_config['energy_type'], policy_config['year'])] = \
                energy_dict['{0}_{1}_increment_{2}_units_{3}'.format(type, policy_config['policy_name'], policy_config['energy_type'], policy_config['year'])] * average_efficiency * energy_dict['{0}_{1}'.format(type, policy_config['energy_type'])]

            #sums individual policy units and energy use by year for all policy impacted units for all policies
            energy_dict['{0}_{1}_policy_{2}_units_{3}'.format(type, policy_config['policy_strata'], policy_config['energy_type'], policy_config['year'])] = \
                energy_dict['{0}_{1}_policy_{2}_units_{3}'.format(type, policy_config['policy_strata'], policy_config['energy_type'], policy_config['year'])] + \
                energy_dict['{0}_{1}_increment_{2}_units_{3}'.format(type, policy_config['policy_name'],
                                                                     policy_config['energy_type'], policy_config['year'])]

            #sums new individual policy units for all policy impacted new units for all policies for all years
            energy_dict['{0}_new_policy_{1}_units'.format(type, policy_config['energy_type'])] = \
                energy_dict['{0}_new_policy_{1}_units'.format(type, policy_config['energy_type'])] + \
                energy_dict['{0}_{1}_increment_{2}_units_{3}'.format(type, policy_config['policy_name'], 
                                                                     policy_config['energy_type'], policy_config['year'])]

            #sums new individual policy use for all policy impacted new units for all policies for all years
            energy_dict['{0}_new_policy_{1}_use'.format(type, policy_config['energy_type'])] = \
                energy_dict['{0}_new_policy_{1}_use'.format(type, policy_config['energy_type'])] + \
                energy_dict['{0}_{1}_increment_{2}_use_{3}'.format(type, policy_config['policy_name'], 
                                                                     policy_config['energy_type'], policy_config['year'])]
            
        else:
            #calculates the number of units for each policy type impacting base units for a given year and energy type
            energy_dict['{0}_{1}_increment_{2}_units_{3}'.format(type, policy_config['policy_name'], policy_config['energy_type'], policy_config['year'])] = \
                (energy_dict['{0}_base'.format(type, rate_type)] - (policy_config['year_increment'] * \
                energy_dict['{0}_{1}_rate'.format(type, rate_type)])) - \
                ((energy_dict['{0}_base'.format(type, rate_type)] - (policy_config['year_increment'] * \
                energy_dict['{0}_{1}_rate'.format(type, rate_type)])) * \
                pow((1 - policy_config['turnover_rate']), policy_config['year_increment']))

            energy_dict['{0}_{1}_increment_{2}_use_{3}'.format(type, policy_config['policy_name'],
                policy_config['energy_type'], policy_config['year'])] = energy_dict['{0}_{1}_increment_{2}_units_{3}'.\
                format(type, policy_config['policy_name'], policy_config['energy_type'], policy_config['year'])] * \
                average_efficiency * energy_dict['{0}_{1}'.format(type, policy_config['energy_type'])]

            energy_dict['{0}_base_policy_{1}_units_{2}'.format(type, policy_config['energy_type'], policy_config['year'])] = \
                energy_dict['{0}_base_policy_{1}_units_{2}'.format(type, policy_config['energy_type'], policy_config['year'])] + \
                energy_dict['{0}_{1}_increment_{2}_units_{3}'.format(type, policy_config['policy_name'],
                                                                     policy_config['energy_type'], policy_config['year'])]
            
            energy_dict['{0}_base_policy_{1}_units'.format(type, policy_config['energy_type'])] = \
                energy_dict['{0}_base_policy_{1}_units'.format(type, policy_config['energy_type'])] + \
                energy_dict['{0}_{1}_increment_{2}_units_{3}'.format(type, policy_config['policy_name'], 
                                                                     policy_config['energy_type'], policy_config['year'])]
            
            energy_dict['{0}_base_policy_{1}_use'.format(type, policy_config['energy_type'])] = \
                energy_dict['{0}_base_policy_{1}_use'.format(type, policy_config['energy_type'])] + \
                energy_dict['{0}_{1}_increment_{2}_use_{3}'.format(type, policy_config['policy_name'], 
                                                                     policy_config['energy_type'], policy_config['year'])]
        
    return energy_dict
        
        
def sum_incremental_energy_use(policy_config, energy_dict, policy_assumptions):



    for use in policy_config['efficiency_dict'].keys():

        previous_calibration_year = policy_config['base_year']

        for year in sorted(policy_config['years'], key=int):

            increment_ratio = (year - float(previous_calibration_year)) / policy_config['scenario_increment']

            new_efficiency_reduction = policy_assumptions['{0}_new_efficiency_{1}'.format(use,
                                            policy_config['energy_type'])].values.get(str(int(year)))

            if previous_calibration_year == policy_config['base_year']:
                previous_new_efficiency_reduction = float(0)
            else:
                previous_new_efficiency_reduction = policy_assumptions['{0}_new_efficiency_{1}'.format(use,
                                                policy_config['energy_type'])].values.get(str(int(previous_calibration_year)))

            year_increment = float(year) - float(previous_calibration_year)

            average_efficiency = 1 - ((previous_new_efficiency_reduction + new_efficiency_reduction) / 2)

            if use =='residential':
                use_types = policy_config['res_types']
            else:
                use_types = policy_config['com_types']

            for type in use_types:

                energy_dict['{0}_new_no_policy_{1}_units'.format(type, policy_config['energy_type'])] = \
                    energy_dict['{0}_new_no_policy_{1}_units'.format(type, policy_config['energy_type'])] + \
                    ((energy_dict['{0}_new_rate'.format(type)] * year_increment) - \
                    float(energy_dict['{0}_new_policy_{1}_units_{2}'.format(type, policy_config['energy_type'], str(int(year)))]))

                energy_dict['{0}_new_no_policy_{1}_use'.format(type, policy_config['energy_type'])] = \
                    energy_dict['{0}_new_no_policy_{1}_use'.format(type, policy_config['energy_type'])] + \
                    ((energy_dict['{0}_new_rate'.format(type)] * year_increment) - \
                    float(energy_dict['{0}_new_policy_{1}_units_{2}'.format(type, policy_config['energy_type'], str(int(year)))])) * \
                    energy_dict['{0}_{1}'.format(type, policy_config['energy_type'])] * average_efficiency

                energy_dict['{0}_base_no_policy_{1}_use'.format(type, policy_config['energy_type'])] = \
                    energy_dict['{0}_base_no_policy_{1}_use'.format(type, policy_config['energy_type'])] + \
                    ((energy_dict['{0}_base'.format(type)] - (energy_dict['{0}_redev_rate'.format(type)] * year_increment) - \
                    float(energy_dict['{0}_base_policy_{1}_units_{2}'.format(type, policy_config['energy_type'], str(int(year)))])) * \
                    energy_dict['{0}_{1}'.format(type, policy_config['energy_type'])]) * increment_ratio


            previous_calibration_year = year

    return energy_dict



def run_final_energy_calcs(policy_config, energy_dict):
    
    energy_dict['residential_{0}_use'.format(policy_config['energy_type'])] = float(0)
    energy_dict['commercial_{0}_use'.format(policy_config['energy_type'])] = float(0)
    
    for type in policy_config['use_types']:
        energy_dict['{0}_new_{1}_use'.format(type, policy_config['energy_type'])] = \
            energy_dict['{0}_new_no_policy_{1}_use'.format(type, policy_config['energy_type'])] + \
            energy_dict['{0}_new_policy_{1}_use'.format(type, policy_config['energy_type'])]
        
        energy_dict['{0}_base_{1}_use'.format(type, policy_config['energy_type'])] = \
            energy_dict['{0}_base_no_policy_{1}_use'.format(type, policy_config['energy_type'])] + \
            energy_dict['{0}_base_policy_{1}_use'.format(type, policy_config['energy_type'])]
        
        energy_dict['{0}_{1}_use'.format(type, policy_config['energy_type'])] = \
            energy_dict['{0}_new_{1}_use'.format(type, policy_config['energy_type'])] + \
            energy_dict['{0}_base_{1}_use'.format(type, policy_config['energy_type'])]
        
    for type in policy_config['res_types']:
        energy_dict['residential_{0}_use'.format(policy_config['energy_type'])] = energy_dict['residential_{0}_use'.format(policy_config['energy_type'])] + \
             energy_dict['{0}_{1}_use'.format(type, policy_config['energy_type'])]
        
    for type in policy_config['com_types']:
        energy_dict['commercial_{0}_use'.format(policy_config['energy_type'])] = energy_dict['commercial_{0}_use'.format(policy_config['energy_type'])] + \
             energy_dict['{0}_{1}_use'.format(type, policy_config['energy_type'])]

    energy_dict['total_{0}_use'.format(policy_config['energy_type'])] = energy_dict['residential_{0}_use'.format(policy_config['energy_type'])] + \
        energy_dict['commercial_{0}_use'.format(policy_config['energy_type'])]

    return energy_dict