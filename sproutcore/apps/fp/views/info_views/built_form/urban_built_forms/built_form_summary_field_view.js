/**
 * Created by calthorpe on 2/19/14.
 */

Footprint.BuiltFormSummaryFieldView = SC.View.extend({
    classNames: ['footprint-summary-field-view'],
    childViews:'nameTitleView contentView'.w(),
    content: null,
    status: null,
    layout: null,
    allContent: null,
    flatBuiltFormStatus: null,
    titleTextAlignment: null,
    computedValue: null,
    componentType: null,
    componentSummaryObserver: null,
    editController: null,

    nameTitleView: SC.LabelView.extend({
        textAlignBinding: SC.Binding.oneWay('.parentView.titleTextAlignment'),
        valueBinding: SC.Binding.oneWay('.parentView.value'),
        layout: {width:.65},
        backgroundColor: '#99CCFF'
    }),
    contentView: SC.LabelView.extend({
        classNames: ['footprint-noneditable-bottom-labelled-content-view'],
        classNameBindings: ['positiveNegative:is-negative'],
        positiveNegative: function() {
            return this.get('value') < 0
        }.property('value').cacheable(),
        textAlign: SC.ALIGN_CENTER,
        valueBinding: SC.Binding.oneWay('.parentView.computedValue'),
        layout: {left:.65}
    })

});


updateFlatBuildings = function(content) {

    var lot_sqft = parseFloat(content.getPath('building_attribute_set.lot_size_square_feet'));
    var total_far = parseFloat(content.getPath('building_attribute_set.total_far'));
    var building_uses = content.getPath('building_attribute_set.building_use_percents');
    var flat_density = content.get('flat_building_densities');

    if (building_uses) {
        building_uses.forEach(function(use) {
            var building_use_percent = use.get('percent');
            var efficiency = use.get('efficiency');
            var sqft_unit = use.get('square_feet_per_unit');

            if (use.getPath('building_use_definition.name') =='Single Family Large Lot') {
                var density = parseFloat((43560.0 / (building_use_percent * lot_sqft)).toFixed(1));
                if (density < 0 || density > 0 || density == 0) {
                    flat_density.setIfChanged('single_family_large_lot_density', density);
                }
            }

            if (use.getPath('building_use_definition.name') =='Single Family Small Lot') {
                var density = parseFloat((43560.0 / (building_use_percent * lot_sqft)).toFixed(1));
                if (density < 0 || density > 0 || density == 0) {
                    flat_density.setIfChanged('single_family_small_lot_density', density);
                }
            }

            if (use.getPath('building_use_definition.name') =='Attached Single Family') {
                var density = parseFloat(((building_use_percent * total_far * efficiency * lot_sqft) / sqft_unit) * (43560.0 / lot_sqft).toFixed(1));
                if (density < 0 || density > 0 || density == 0) {
                    flat_density.setIfChanged('attached_single_family_density', density);
                }
            }

            if (use.getPath('building_use_definition.name') =='Multifamily 2 To 4') {
                var density = parseFloat(((building_use_percent * total_far * efficiency * lot_sqft) / sqft_unit) * (43560.0 / lot_sqft).toFixed(1));
                if (density < 0 || density > 0 || density == 0) {
                    flat_density.setIfChanged('multifamily_2_to_4_density', density);
                }
            }

            if (use.getPath('building_use_definition.name') =='Multifamily 5 Plus') {
                var density = parseFloat(((building_use_percent * total_far * efficiency * lot_sqft) / sqft_unit) * (43560.0 / lot_sqft).toFixed(1));
                if (density < 0 || density > 0 || density == 0) {
                    flat_density.setIfChanged('multifamily_5_plus_density', density);
                }
            }


            if (use.getPath('building_use_definition.name') =='Retail Services') {
                var density = parseFloat(((building_use_percent * total_far * efficiency * lot_sqft) / sqft_unit) * (43560.0 / lot_sqft).toFixed(1));
                if (density < 0 || density > 0 || density == 0) {
                    flat_density.setIfChanged('retail_services_density', density);
                }
            }

            if (use.getPath('building_use_definition.name') =='Restaurant') {
                var density = parseFloat(((building_use_percent * total_far * efficiency * lot_sqft) / sqft_unit) * (43560.0 / lot_sqft).toFixed(1));
                if (density < 0 || density > 0 || density == 0) {
                    flat_density.setIfChanged('restaurant_density', density);
                }
            }

            if (use.getPath('building_use_definition.name') =='Arts Entertainment') {
                var density = parseFloat(((building_use_percent * total_far * efficiency * lot_sqft) / sqft_unit) * (43560.0 / lot_sqft).toFixed(1));
                if (density < 0 || density > 0 || density == 0) {
                    flat_density.setIfChanged('arts_entertainment_density', density);
                }
            }

            if (use.getPath('building_use_definition.name') =='Accommodation') {
                var density = parseFloat(((building_use_percent * total_far * efficiency * lot_sqft) / sqft_unit) * (43560.0 / lot_sqft).toFixed(1));
                if (density < 0 || density > 0 || density == 0) {
                    flat_density.setIfChanged('accommodation_density', density);
                }
            }

            if (use.getPath('building_use_definition.name') =='Other Services') {
                var density = parseFloat(((building_use_percent * total_far * efficiency * lot_sqft) / sqft_unit) * (43560.0 / lot_sqft).toFixed(1));
                if (density < 0 || density > 0 || density == 0) {
                    flat_density.setIfChanged('other_services_density', density);
                }
            }

            if (use.getPath('building_use_definition.name') =='Office Services') {
                var density = parseFloat(((building_use_percent * total_far * efficiency * lot_sqft) / sqft_unit) * (43560.0 / lot_sqft).toFixed(1));
                if (density < 0 || density > 0 || density == 0) {
                    flat_density.setIfChanged('office_services_density', density);
                }
            }

            if (use.getPath('building_use_definition.name') =='Public Admin') {
                var density = parseFloat(((building_use_percent * total_far * efficiency * lot_sqft) / sqft_unit) * (43560.0 / lot_sqft).toFixed(1));
                if (density < 0 || density > 0 || density == 0) {
                    flat_density.setIfChanged('public_admin_density', density);
                }
            }

            if (use.getPath('building_use_definition.name') =='Education Services') {
                var density = parseFloat(((building_use_percent * total_far * efficiency * lot_sqft) / sqft_unit) * (43560.0 / lot_sqft).toFixed(1));
                if (density < 0 || density > 0 || density == 0) {
                    flat_density.setIfChanged('education_services_density', density);
                }
            }

            if (use.getPath('building_use_definition.name') =='Medical Services') {
                var density = parseFloat(((building_use_percent * total_far * efficiency * lot_sqft) / sqft_unit) * (43560.0 / lot_sqft).toFixed(1));
                if (density < 0 || density > 0 || density == 0) {
                    flat_density.setIfChanged('medical_services_density', density);
                }
            }

            if (use.getPath('building_use_definition.name') =='Manufacturing') {
                var density = parseFloat(((building_use_percent * total_far * efficiency * lot_sqft) / sqft_unit) * (43560.0 / lot_sqft).toFixed(1));
                if (density < 0 || density > 0 || density == 0) {
                    flat_density.setIfChanged('manufacturing_density', density);
                }
            }

            if (use.getPath('building_use_definition.name') =='Wholesale') {
                var density = parseFloat(((building_use_percent * total_far * efficiency * lot_sqft) / sqft_unit) * (43560.0 / lot_sqft).toFixed(1));
                if (density < 0 || density > 0 || density == 0) {
                    flat_density.setIfChanged('wholesale_density', density);
                }
            }

            if (use.getPath('building_use_definition.name') =='Transport Warehouse') {
                var density = parseFloat(((building_use_percent * total_far * efficiency * lot_sqft) / sqft_unit) * (43560.0 / lot_sqft).toFixed(1));
                if (density < 0 || density > 0 || density == 0) {
                    flat_density.setIfChanged('transport_warehouse_density', density);
                }
            }

            if (use.getPath('building_use_definition.name') =='Construction Utilities') {
                var density = parseFloat(((building_use_percent * total_far * efficiency * lot_sqft) / sqft_unit) * (43560.0 / lot_sqft).toFixed(1));
                if (density < 0 || density > 0 || density == 0) {
                    flat_density.setIfChanged('construction_utilities_density', density);
                }
            }

            if (use.getPath('building_use_definition.name') =='Agriculture') {
                var density = parseFloat(((building_use_percent * total_far * efficiency * lot_sqft) / sqft_unit) * (43560.0 / lot_sqft).toFixed(1));
                if (density < 0 || density > 0 || density == 0) {
                    flat_density.setIfChanged('agriculture_density', density);
                }
            }
            if (use.getPath('building_use_definition.name') =='Extraction') {
                var density = parseFloat(((building_use_percent * total_far * efficiency * lot_sqft) / sqft_unit) * (43560.0 / lot_sqft).toFixed(1));
                if (density < 0 || density > 0 || density == 0) {
                    flat_density.setIfChanged('extraction_density', density);
                }
            }

            if (use.getPath('building_use_definition.name') =='Armed Forces') {
                var density = parseFloat(((building_use_percent * total_far * efficiency * lot_sqft) / sqft_unit) * (43560.0 / lot_sqft).toFixed(1));
                if (density < 0 || density > 0 || density == 0) {
                    flat_density.setIfChanged('armed_forces_density', density);
                }
            }
        })
    }
};

updateFlatBuiltForm = function(content, field, compontent_type) {

    var weighted_density = 0.0;
    var component_percents = content.get('component_percents');
    var flat_content = content.get('flat_building_densities')

    if (component_percents) {
        component_percents.forEach(function(component_percent) {
            if (component_percent.get('percent'))
                var percent = component_percent.get('percent');
            else
                var percent = 0;

            var component = component_percent.get('subclassedComponent');
            if (!component) {
                logWarning("component_percent has no component. This is due to a transition between Built Form controllers, but needs fixing");
            }
            else {
                var flat_building_densities = component.get('flat_building_densities');
                if (flat_building_densities && flat_building_densities.get(field))
                    var density = flat_building_densities.get(field);
                else
                    var density = 0;
                var percent_density = percent * density;
                weighted_density = weighted_density + percent_density;
            }
        });

        if (weighted_density < 0 || weighted_density > 0 || weighted_density == 0) {
            if (flat_content){
                flat_content.setIfChanged(field, weighted_density);

            }
        }
    }
};