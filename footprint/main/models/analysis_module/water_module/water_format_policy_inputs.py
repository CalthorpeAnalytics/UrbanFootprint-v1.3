__author__ = 'calthorpe'



def FormatPolicyInputs(config_entity):

    policy_assumptions = {}
    
    policy_assumptions['du_detsf_ll_indoor'] = \
        config_entity.selected_policy_set().policy_by_key('water.residential_indoor_water_factors.du_detsf_ll') * 365
    
    policy_assumptions['du_detsf_sl_indoor'] = \
        config_entity.selected_policy_set().policy_by_key('water.residential_indoor_water_factors.du_detsf_sl') * 365
    
    policy_assumptions['du_attsf_indoor'] = \
        config_entity.selected_policy_set().policy_by_key('water.residential_indoor_water_factors.du_attsf') * 365
    
    policy_assumptions['du_mf_indoor'] = \
        config_entity.selected_policy_set().policy_by_key('water.residential_indoor_water_factors.du_mf') * 365
    

    policy_assumptions['retail_services_indoor'] = \
        config_entity.selected_policy_set().policy_by_key('water.commercial_indoor_water_factors.retail_services') * 365
    
    policy_assumptions['restaurant_indoor'] = \
        config_entity.selected_policy_set().policy_by_key('water.commercial_indoor_water_factors.restaurant') * 365
    
    policy_assumptions['accommodation_indoor'] = \
        config_entity.selected_policy_set().policy_by_key('water.commercial_indoor_water_factors.accommodation') * 365
    
    policy_assumptions['other_services_indoor'] = \
        config_entity.selected_policy_set().policy_by_key('water.commercial_indoor_water_factors.other_services') * 365
    
    policy_assumptions['office_services_indoor'] = \
        config_entity.selected_policy_set().policy_by_key('water.commercial_indoor_water_factors.office_services') * 365
    
    policy_assumptions['education_indoor'] = \
        config_entity.selected_policy_set().policy_by_key('water.commercial_indoor_water_factors.education') * 365
    
    policy_assumptions['public_admin_indoor'] = \
        config_entity.selected_policy_set().policy_by_key('water.commercial_indoor_water_factors.public_admin') * 365
    
    policy_assumptions['medical_services_indoor'] = \
        config_entity.selected_policy_set().policy_by_key('water.commercial_indoor_water_factors.medical_services') * 365
    
    policy_assumptions['wholesale_indoor'] = \
        config_entity.selected_policy_set().policy_by_key('water.commercial_indoor_water_factors.wholesale') * 365
    
    policy_assumptions['transport_warehousing_indoor'] = \
        config_entity.selected_policy_set().policy_by_key('water.commercial_indoor_water_factors.transport_warehousing') * 365
    
    policy_assumptions['construction_indoor'] = \
        config_entity.selected_policy_set().policy_by_key('water.commercial_indoor_water_factors.construction_utilities') * 365

    policy_assumptions['utilities_indoor'] = \
        config_entity.selected_policy_set().policy_by_key('water.commercial_indoor_water_factors.construction_utilities') * 365
    
    policy_assumptions['manufacturing_indoor'] = \
        config_entity.selected_policy_set().policy_by_key('water.commercial_indoor_water_factors.manufacturing') * 365
    
    policy_assumptions['extraction_indoor'] = \
        config_entity.selected_policy_set().policy_by_key('water.commercial_indoor_water_factors.extraction') * 365
    
    policy_assumptions['military_indoor'] = \
        config_entity.selected_policy_set().policy_by_key('water.commercial_indoor_water_factors.military') * 365
    
    policy_assumptions['agriculture_indoor'] = \
        config_entity.selected_policy_set().policy_by_key('water.commercial_indoor_water_factors.agriculture') * 365

    #Residential Indoor Water Use efficiency Assumptions
    policy_assumptions['residential_new_efficiency_indoor'] = \
        config_entity.selected_policy_set().policy_by_key('water.residential_new_construction_efficiency_indoor')
    
    policy_assumptions['residential_new_retrofit_efficiency_indoor'] = \
        config_entity.selected_policy_set().policy_by_key('water.residential_new_building_retrofit_efficiency_indoor')
    
    policy_assumptions['residential_base_retrofit_efficiency_indoor'] = \
        config_entity.selected_policy_set().policy_by_key('water.residential_persisting_building_retrofit_efficiency_indoor')
    
    #residential rates for building turnover    
    policy_assumptions['residential_new_retrofit_indoor_rate'] = \
        float(config_entity.selected_policy_set().policy_by_key('water.residential_rates_indoor.annual_new_building_retrofit_rate'))
    
    policy_assumptions['residential_base_retrofit_indoor_rate'] = \
        float(config_entity.selected_policy_set().policy_by_key('water.residential_rates_indoor.annual_base_building_retrofit_rate'))
    
    policy_assumptions['residential_base_replacement_indoor_rate'] = \
        float(config_entity.selected_policy_set().policy_by_key('water.residential_rates_indoor.annual_base_building_renovation_rate'))



    #Commercial Indoor Water  Use efficiency Assumptions
    policy_assumptions['commercial_new_efficiency_indoor'] = \
        config_entity.selected_policy_set().policy_by_key('water.commercial_new_construction_efficiency_indoor')
    
    policy_assumptions['commercial_new_retrofit_efficiency_indoor'] = \
        config_entity.selected_policy_set().policy_by_key('water.commercial_new_building_retrofit_efficiency_indoor')
    
    policy_assumptions['commercial_base_retrofit_efficiency_indoor'] = \
        config_entity.selected_policy_set().policy_by_key('water.commercial_persisting_building_retrofit_efficiency_indoor')
    
    #commercial rates for building turnover    
    policy_assumptions['commercial_new_retrofit_indoor_rate'] = \
        float(config_entity.selected_policy_set().policy_by_key('water.commercial_rates_indoor.annual_new_building_retrofit_rate'))
    
    policy_assumptions['commercial_base_retrofit_indoor_rate'] = \
        float(config_entity.selected_policy_set().policy_by_key('water.commercial_rates_indoor.annual_base_building_retrofit_rate'))
    
    policy_assumptions['commercial_base_replacement_indoor_rate'] = \
        float(config_entity.selected_policy_set().policy_by_key('water.commercial_rates_indoor.annual_base_building_renovation_rate'))



    #Residential outdoor WATER Use efficiency Assumptions
    policy_assumptions['residential_new_efficiency_outdoor'] = \
        config_entity.selected_policy_set().policy_by_key('water.residential_new_construction_efficiency_outdoor')
    
    policy_assumptions['residential_new_retrofit_efficiency_outdoor'] = \
        config_entity.selected_policy_set().policy_by_key('water.residential_new_building_retrofit_efficiency_outdoor')
    
    policy_assumptions['residential_base_retrofit_efficiency_outdoor'] = \
        config_entity.selected_policy_set().policy_by_key('water.residential_persisting_building_retrofit_efficiency_outdoor')
    
    #residential rates for building turnover    
    policy_assumptions['residential_new_retrofit_outdoor_rate'] = \
        float(config_entity.selected_policy_set().policy_by_key('water.residential_rates_outdoor.annual_new_building_retrofit_rate'))
    
    policy_assumptions['residential_base_retrofit_outdoor_rate'] = \
        float(config_entity.selected_policy_set().policy_by_key('water.residential_rates_outdoor.annual_base_building_retrofit_rate'))
    
    policy_assumptions['residential_base_replacement_outdoor_rate'] = \
        float(config_entity.selected_policy_set().policy_by_key('water.residential_rates_outdoor.annual_base_building_renovation_rate'))


    #Commercial outdoor WATER Use efficiency Assumptions
    policy_assumptions['commercial_new_efficiency_outdoor'] = \
        config_entity.selected_policy_set().policy_by_key('water.commercial_new_construction_efficiency_outdoor')
    
    policy_assumptions['commercial_new_retrofit_efficiency_outdoor'] = \
        config_entity.selected_policy_set().policy_by_key('water.commercial_new_building_retrofit_efficiency_outdoor')
    
    policy_assumptions['commercial_base_retrofit_efficiency_outdoor'] = \
        config_entity.selected_policy_set().policy_by_key('water.commercial_persisting_building_retrofit_efficiency_outdoor')
    
    #commercial rates for building turnover    
    policy_assumptions['commercial_new_retrofit_outdoor_rate'] = \
        float(config_entity.selected_policy_set().policy_by_key('water.commercial_rates_outdoor.annual_new_building_retrofit_rate'))
    
    policy_assumptions['commercial_base_retrofit_outdoor_rate'] = \
        float(config_entity.selected_policy_set().policy_by_key('water.commercial_rates_outdoor.annual_base_building_retrofit_rate'))
    
    policy_assumptions['commercial_base_replacement_outdoor_rate'] = \
        float(config_entity.selected_policy_set().policy_by_key('water.commercial_rates_outdoor.annual_base_building_renovation_rate'))


    return policy_assumptions