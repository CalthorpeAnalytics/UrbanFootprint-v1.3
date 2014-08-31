from footprint.main.models.analysis_module.energy_module.energy_future import run_incremental_energy_calculations, sum_incremental_energy_use, run_final_energy_calcs
from footprint.main.models.analysis_module.energy_module.energy_keys import ENERGY_TYPES, NEW_EFFICIENCY, COMMERCIAL_TYPES, RESIDENTIAL_TYPES, POLICY_STRATA, BASE_EFFICIENCY
from footprint.main.models.config import config_entity

__author__ = 'calthorpe'


def calculate_future_energy(energy_dict, policy_assumptions, global_energy_config):
    
    #residential annual redevelopment rate by dwelling unit type
    energy_dict['du_detsf_sl_redev_rate'] = energy_dict['du_detsf_sl_redev'] / global_energy_config['time_increment']
    energy_dict['du_detsf_ll_redev_rate'] = energy_dict['du_detsf_ll_redev'] / global_energy_config['time_increment']
    energy_dict['du_attsf_redev_rate'] = energy_dict['du_attsf_redev'] / global_energy_config['time_increment']
    energy_dict['du_mf_redev_rate'] = energy_dict['du_mf_redev'] / global_energy_config['time_increment']
    
    #commercial annual redevelopment rate by commercial square foot type
    energy_dict['retail_services_redev_rate'] = energy_dict['retail_services_redev'] / global_energy_config['time_increment']
    energy_dict['restaurant_redev_rate'] = energy_dict['restaurant_redev'] / global_energy_config['time_increment']
    energy_dict['accommodation_redev_rate'] = energy_dict['accommodation_redev'] / global_energy_config['time_increment']
    energy_dict['arts_entertainment_redev_rate'] = energy_dict['arts_entertainment_redev'] / global_energy_config['time_increment']
    energy_dict['other_services_redev_rate'] = energy_dict['other_services_redev'] / global_energy_config['time_increment']
    energy_dict['office_services_redev_rate'] = energy_dict['office_services_redev'] / global_energy_config['time_increment']
    energy_dict['education_redev_rate'] = energy_dict['education_redev'] / global_energy_config['time_increment']
    energy_dict['public_admin_redev_rate'] = energy_dict['public_admin_redev'] / global_energy_config['time_increment']
    energy_dict['medical_services_redev_rate'] = energy_dict['medical_services_redev'] / global_energy_config['time_increment']
    energy_dict['wholesale_redev_rate'] = energy_dict['wholesale_redev'] / global_energy_config['time_increment']
    energy_dict['transport_warehousing_redev_rate'] = energy_dict['transport_warehousing_redev'] / global_energy_config['time_increment']
    
    #residential annual dwelling unit rate by dwelling unit type
    energy_dict['du_detsf_sl_new_rate'] = energy_dict['du_detsf_sl_new'] / global_energy_config['time_increment']
    energy_dict['du_detsf_ll_new_rate'] = energy_dict['du_detsf_ll_new'] / global_energy_config['time_increment']
    energy_dict['du_attsf_new_rate'] = energy_dict['du_attsf_new'] / global_energy_config['time_increment']
    energy_dict['du_mf_new_rate'] = energy_dict['du_mf_new'] / global_energy_config['time_increment']
    
    #commercial annual new building square feet rate by commercial square foot type
    energy_dict['retail_services_new_rate'] = energy_dict['retail_services_new'] / global_energy_config['time_increment']
    energy_dict['restaurant_new_rate'] = energy_dict['restaurant_new'] / global_energy_config['time_increment']
    energy_dict['accommodation_new_rate'] = energy_dict['accommodation_new'] / global_energy_config['time_increment']
    energy_dict['arts_entertainment_new_rate'] = energy_dict['arts_entertainment_new'] / global_energy_config['time_increment']
    energy_dict['other_services_new_rate'] = energy_dict['other_services_new'] / global_energy_config['time_increment']
    energy_dict['office_services_new_rate'] = energy_dict['office_services_new'] / global_energy_config['time_increment']
    energy_dict['education_new_rate'] = energy_dict['education_new'] / global_energy_config['time_increment']
    energy_dict['public_admin_new_rate'] = energy_dict['public_admin_new'] / global_energy_config['time_increment']
    energy_dict['medical_services_new_rate'] = energy_dict['medical_services_new'] / global_energy_config['time_increment']
    energy_dict['wholesale_new_rate'] = energy_dict['wholesale_new'] / global_energy_config['time_increment']
    energy_dict['transport_warehousing_new_rate'] = energy_dict['transport_warehousing_new'] / global_energy_config['time_increment']
    

    #calculate the year by year energy use for new buildings integrating user defined policy increments
    for energy_type in ENERGY_TYPES:

        types = RESIDENTIAL_TYPES + COMMERCIAL_TYPES

        for use in POLICY_STRATA.keys():
            for year in POLICY_STRATA[use]:
                for type in types:
                    energy_dict['{0}_{1}_policy_{2}_units_{3}'.format(type, use, energy_type, year)] = float(0)

        for type in types:
            energy_dict['{0}_new_policy_{1}_units'.format(type, energy_type)] = float(0)
            energy_dict['{0}_base_policy_{1}_units'.format(type, energy_type)] = float(0)
            energy_dict['{0}_new_policy_{1}_use'.format(type, energy_type)] = float(0)
            energy_dict['{0}_base_policy_{1}_use'.format(type, energy_type)] = float(0)
            energy_dict['{0}_new_no_policy_{1}_units'.format(type, energy_type)] = float(0)
            energy_dict['{0}_new_no_policy_{1}_use'.format(type, energy_type)] = float(0)
            energy_dict['{0}_base_no_policy_{1}_use'.format(type, energy_type)] = float(0)

        for strata in POLICY_STRATA.keys():
            if strata == 'new':
                efficiency_dict = NEW_EFFICIENCY
            else:
                efficiency_dict = BASE_EFFICIENCY

            for use in efficiency_dict.keys():
                use_key = use

                for efficiency in efficiency_dict[use]:

                    if 'replacement' in efficiency:
                        if use_key == 'residential':
                            efficiency_class = \
                                policy_assumptions['residential_new_efficiency_{0}'.format(
                                    energy_type)]
                        else:
                            efficiency_class = \
                                policy_assumptions['commercial_new_efficiency_{0}'.format(
                                    energy_type)]
                    else:
                        efficiency_class = policy_assumptions['{0}_efficiency_{1}'.format(efficiency, energy_type)]

                    years = map(float, efficiency_class.values.keys())
                    previous_calibration_year = global_energy_config['base_year']

                    for year in sorted(years, key=int):

                        for type in types:
                            energy_dict['{0}_new_policy_{1}_units_{2}'.format(type, energy_type, year)] = 0

                        if global_energy_config['future_year'] > year and previous_calibration_year < year:
                        #residential replacement units in the persisting building stock by dwelling unit type
                            year_increment = year - previous_calibration_year
                        elif global_energy_config['future_year'] <= year and previous_calibration_year < year:
                            year_increment = global_energy_config['future_year'] - previous_calibration_year
                        else:
                            year_increment = 0

                        if 'replacement' in efficiency:
                            if use_key == 'residential':
                                efficiency_reduction = \
                                    policy_assumptions['residential_new_efficiency_{0}'.format(
                                        energy_type)].values.get(str(int(year))),

                                efficiency_reduction=efficiency_reduction[0]

                                if previous_calibration_year == global_energy_config['base_year']:
                                    previous_efficiency_reduction = 0
                                else:
                                    previous_efficiency_reduction = \
                                    policy_assumptions['residential_new_efficiency_{0}'.format(
                                        energy_type)].values.get(str(int(previous_calibration_year)))

                            else:
                                efficiency_reduction = \
                                    policy_assumptions['commercial_new_efficiency_{0}'.format(energy_type)].values.get(str(int(year))),
                                efficiency_reduction=efficiency_reduction[0]

                                if previous_calibration_year == global_energy_config['base_year']:
                                    previous_efficiency_reduction = 0
                                else:
                                    previous_efficiency_reduction = \
                                    policy_assumptions['commercial_new_efficiency_{0}'.format(energy_type)]\
                                        .values.get(str(int(year))),
                                    previous_efficiency_reduction= previous_efficiency_reduction[0]

                        else:
                            efficiency_reduction=policy_assumptions['{0}_efficiency_{1}'.format(efficiency,
                                energy_type)].values.get(str(int(year))),

                            efficiency_reduction=efficiency_reduction[0]

                            if previous_calibration_year == global_energy_config['base_year']:
                                previous_efficiency_reduction = 0
                            else:
                                previous_efficiency_reduction = policy_assumptions['{0}_efficiency_{1}'.format(efficiency,
                                energy_type)].values.get(str(int(previous_calibration_year))),
                                previous_efficiency_reduction= previous_efficiency_reduction[0]

                        policy_config = dict(
                            year=str(int(year)),
                            previous_calibration_year=str(int(previous_calibration_year)),
                            year_increment=year_increment,
                            years=years,
                            use_key=use_key,
                            use_types=types,
                            res_types=RESIDENTIAL_TYPES,
                            com_types=COMMERCIAL_TYPES,
                            policy_strata=strata,
                            policy_name=efficiency,
                            efficiency_reduction=float(efficiency_reduction),
                            previous_efficiency_reduction=float(previous_efficiency_reduction),
                            turnover_rate=policy_assumptions['{0}_{1}_rate'.format(efficiency, energy_type)],
                            energy_type=energy_type,
                            efficiency_list=efficiency_dict.keys(),
                            base_year=str(int(global_energy_config['base_year'])),
                            future_year=str(int(global_energy_config['future_year'])),
                            scenario_increment=global_energy_config['time_increment'],
                            efficiency_dict=efficiency_dict
                        )

                        incremental_energy_efficiency_dict = \
                            run_incremental_energy_calculations(policy_config, energy_dict)

                        previous_calibration_year = year

        new_energy_use = sum_incremental_energy_use(policy_config, incremental_energy_efficiency_dict, policy_assumptions)
        total_energy_use = run_final_energy_calcs(policy_config, new_energy_use)


    return total_energy_use