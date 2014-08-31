from footprint.main.models.analysis_module.water_module.water_future import run_incremental_water_calculations, sum_incremental_water_use, run_final_water_calcs
from footprint.main.models.analysis_module.water_module.water_keys import WATER_TYPES, RESIDENTIAL_TYPES, COMMERCIAL_TYPES, POLICY_STRATA, NEW_EFFICIENCY, BASE_EFFICIENCY


def calculate_future_water(water_dict, policy_assumptions, global_water_config):

    types = RESIDENTIAL_TYPES + COMMERCIAL_TYPES + ['residential_irrigated_sqft', 'commercial_irrigated_sqft']

    water_dict['residential_indoor_water_use'] = float(0)
    water_dict['commercial_indoor_water_use'] = float(0)
    water_dict['residential_outdoor_water_use'] = float(0)
    water_dict['commercial_outdoor_water_use'] = float(0)

    for type in types:

    #residential annual redevelopment rate by dwelling unit type
        water_dict['{0}_redev_rate'.format(type)] = water_dict['{0}_redev'.format(type)]/ global_water_config['time_increment']
        water_dict['{0}_new_rate'.format(type)] = water_dict['{0}_new'.format(type)]/ global_water_config['time_increment']

    #calculate the year by year water use for new buildings integrating user defined policy increments
    for water_type in WATER_TYPES:

        for use in POLICY_STRATA.keys():
            for year in POLICY_STRATA[use]:
                for type in types:
                    water_dict['{0}_{1}_policy_{2}_units_{3}'.format(type, use, water_type, year)] = float(0)

        for type in types:
            water_dict['{0}_new_policy_{1}_units'.format(type, water_type)] = float(0)
            water_dict['{0}_base_policy_{1}_units'.format(type, water_type)] = float(0)
            water_dict['{0}_new_policy_{1}_use'.format(type, water_type)] = float(0)
            water_dict['{0}_base_policy_{1}_use'.format(type, water_type)] = float(0)
            water_dict['{0}_new_no_policy_{1}_units'.format(type, water_type)] = float(0)
            water_dict['{0}_new_no_policy_{1}_use'.format(type, water_type)] = float(0)
            water_dict['{0}_base_no_policy_{1}_use'.format(type, water_type)] = float(0)

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
                                    water_type)]
                        else:
                            efficiency_class = \
                                policy_assumptions['commercial_new_efficiency_{0}'.format(
                                    water_type)]
                    else:
                        efficiency_class = policy_assumptions['{0}_efficiency_{1}'.format(efficiency, water_type)]

                    years = map(float, efficiency_class.values.keys())
                    previous_calibration_year = global_water_config['base_year']

                    for year in sorted(years, key=int):

                        for type in types:
                            water_dict['{0}_new_policy_{1}_units_{2}'.format(type, water_type, year)] = 0

                        if global_water_config['future_year'] > year and previous_calibration_year < year:
                        #residential replacement units in the persisting building stock by dwelling unit type
                            year_increment = year - previous_calibration_year
                        elif global_water_config['future_year'] <= year and previous_calibration_year < year:
                            year_increment = global_water_config['future_year'] - previous_calibration_year
                        else:
                            year_increment = 0

                        if 'replacement' in efficiency:
                            if use_key == 'residential':
                                efficiency_reduction = \
                                    policy_assumptions['residential_new_efficiency_{0}'.format(
                                        water_type)].values.get(str(int(year))),

                                efficiency_reduction=efficiency_reduction[0]

                                if previous_calibration_year == global_water_config['base_year']:
                                    previous_efficiency_reduction = 0
                                else:
                                    previous_efficiency_reduction = \
                                    policy_assumptions['residential_new_efficiency_{0}'.format(
                                        water_type)].values.get(str(int(previous_calibration_year)))

                            else:
                                efficiency_reduction = \
                                    policy_assumptions['commercial_new_efficiency_{0}'.format(water_type)].values.get(str(int(year))),
                                efficiency_reduction=efficiency_reduction[0]

                                if previous_calibration_year == global_water_config['base_year']:
                                    previous_efficiency_reduction = 0
                                else:
                                    previous_efficiency_reduction = \
                                    policy_assumptions['commercial_new_efficiency_{0}'.format(water_type)]\
                                        .values.get(str(int(year))),
                                    previous_efficiency_reduction= previous_efficiency_reduction[0]

                        else:
                            efficiency_reduction=policy_assumptions['{0}_efficiency_{1}'.format(efficiency,
                                water_type)].values.get(str(int(year))),

                            efficiency_reduction=efficiency_reduction[0]

                            if previous_calibration_year == global_water_config['base_year']:
                                previous_efficiency_reduction = 0
                            else:
                                previous_efficiency_reduction = policy_assumptions['{0}_efficiency_{1}'.format(efficiency,
                                water_type)].values.get(str(int(previous_calibration_year))),
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
                            turnover_rate=policy_assumptions['{0}_{1}_rate'.format(efficiency, water_type)],
                            water_type=water_type,
                            efficiency_list=efficiency_dict.keys(),
                            base_year=str(int(global_water_config['base_year'])),
                            future_year=str(int(global_water_config['future_year'])),
                            scenario_increment=global_water_config['time_increment'],
                            efficiency_dict=efficiency_dict
                        )

                        incremental_water_efficiency_dict = \
                            run_incremental_water_calculations(policy_config, water_dict, policy_assumptions)

                        previous_calibration_year = year

        new_water_use = sum_incremental_water_use(policy_config, incremental_water_efficiency_dict, policy_assumptions)
        total_water_use = run_final_water_calcs(policy_config, new_water_use)


    return total_water_use