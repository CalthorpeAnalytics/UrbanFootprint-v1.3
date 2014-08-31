__author__ = 'calthorpe'



def FormatPolicyInputs(config_entity):

    policy_assumptions = {}

    #Residential Gas Use efficiency Assumptions
    policy_assumptions['residential_new_efficiency_gas'] = \
        config_entity.selected_policy_set().policy_by_key('energy.residential_new_construction_efficiency_gas')
    
    policy_assumptions['residential_new_retrofit_efficiency_gas'] = \
        config_entity.selected_policy_set().policy_by_key('energy.residential_new_building_retrofit_efficiency_gas')
    
    policy_assumptions['residential_base_retrofit_efficiency_gas'] = \
        config_entity.selected_policy_set().policy_by_key('energy.residential_persisting_building_retrofit_efficiency_gas')
    
    #residential rates for building turnover    
    policy_assumptions['residential_new_retrofit_gas_rate'] = \
        float(config_entity.selected_policy_set().policy_by_key('energy.residential_rates_gas.annual_new_building_retrofit_rate'))
    
    policy_assumptions['residential_base_retrofit_gas_rate'] = \
        float(config_entity.selected_policy_set().policy_by_key('energy.residential_rates_gas.annual_base_building_retrofit_rate'))
    
    policy_assumptions['residential_base_replacement_gas_rate'] = \
        float(config_entity.selected_policy_set().policy_by_key('energy.residential_rates_gas.annual_base_building_renovation_rate'))



    #Commercial Gas Use efficiency Assumptions
    policy_assumptions['commercial_new_efficiency_gas'] = \
        config_entity.selected_policy_set().policy_by_key('energy.commercial_new_construction_efficiency_gas')
    
    policy_assumptions['commercial_new_retrofit_efficiency_gas'] = \
        config_entity.selected_policy_set().policy_by_key('energy.commercial_new_building_retrofit_efficiency_gas')
    
    policy_assumptions['commercial_base_retrofit_efficiency_gas'] = \
        config_entity.selected_policy_set().policy_by_key('energy.commercial_persisting_building_retrofit_efficiency_gas')
    
    #commercial rates for building turnover    
    policy_assumptions['commercial_new_retrofit_gas_rate'] = \
        float(config_entity.selected_policy_set().policy_by_key('energy.commercial_rates_gas.annual_new_building_retrofit_rate'))
    
    policy_assumptions['commercial_base_retrofit_gas_rate'] = \
        float(config_entity.selected_policy_set().policy_by_key('energy.commercial_rates_gas.annual_base_building_retrofit_rate'))
    
    policy_assumptions['commercial_base_replacement_gas_rate'] = \
        float(config_entity.selected_policy_set().policy_by_key('energy.commercial_rates_gas.annual_base_building_renovation_rate'))



    #Residential electricity Use efficiency Assumptions
    policy_assumptions['residential_new_efficiency_electricity'] = \
        config_entity.selected_policy_set().policy_by_key('energy.residential_new_construction_efficiency_electricity')
    
    policy_assumptions['residential_new_retrofit_efficiency_electricity'] = \
        config_entity.selected_policy_set().policy_by_key('energy.residential_new_building_retrofit_efficiency_electricity')
    
    policy_assumptions['residential_base_retrofit_efficiency_electricity'] = \
        config_entity.selected_policy_set().policy_by_key('energy.residential_persisting_building_retrofit_efficiency_electricity')
    
    #residential rates for building turnover    
    policy_assumptions['residential_new_retrofit_electricity_rate'] = \
        float(config_entity.selected_policy_set().policy_by_key('energy.residential_rates_electricity.annual_new_building_retrofit_rate'))
    
    policy_assumptions['residential_base_retrofit_electricity_rate'] = \
        float(config_entity.selected_policy_set().policy_by_key('energy.residential_rates_electricity.annual_base_building_retrofit_rate'))
    
    policy_assumptions['residential_base_replacement_electricity_rate'] = \
        float(config_entity.selected_policy_set().policy_by_key('energy.residential_rates_electricity.annual_base_building_renovation_rate'))



    #Commercial electricity Use efficiency Assumptions
    policy_assumptions['commercial_new_efficiency_electricity'] = \
        config_entity.selected_policy_set().policy_by_key('energy.commercial_new_construction_efficiency_electricity')
    
    policy_assumptions['commercial_new_retrofit_efficiency_electricity'] = \
        config_entity.selected_policy_set().policy_by_key('energy.commercial_new_building_retrofit_efficiency_electricity')
    
    policy_assumptions['commercial_base_retrofit_efficiency_electricity'] = \
        config_entity.selected_policy_set().policy_by_key('energy.commercial_persisting_building_retrofit_efficiency_electricity')
    
    #commercial rates for building turnover    
    policy_assumptions['commercial_new_retrofit_electricity_rate'] = \
        float(config_entity.selected_policy_set().policy_by_key('energy.commercial_rates_electricity.annual_new_building_retrofit_rate'))
    
    policy_assumptions['commercial_base_retrofit_electricity_rate'] = \
        float(config_entity.selected_policy_set().policy_by_key('energy.commercial_rates_electricity.annual_base_building_retrofit_rate'))
    
    policy_assumptions['commercial_base_replacement_electricity_rate'] = \
        float(config_entity.selected_policy_set().policy_by_key('energy.commercial_rates_electricity.annual_base_building_renovation_rate'))


    return policy_assumptions