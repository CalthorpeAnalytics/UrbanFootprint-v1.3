sc_require('models/key_mixin');
sc_require('models/name_mixin');
sc_require('models/tags_mixin');
sc_require('models/medium_models');

Footprint.BuildingAttributeSet = Footprint.Record.extend({
    flat_building_densities: SC.Record.toOne("Footprint.FlatBuiltForm", {nested: YES}),
    building_uses: SC.Record.toMany('Footprint.BuildingUsePercent', {nested: YES}),
    parking_spaces: SC.Record.attr(Number),
    parking_structure_square_feet: SC.Record.attr(Number),
    floors: SC.Record.attr(Number),
    total_far: SC.Record.attr(Number),
    gross_population_density: SC.Record.attr(Number),
    household_density: SC.Record.attr(Number),
    impervious_roof_percent: SC.Record.attr(Number),
    impervious_hardscape_percent: SC.Record.attr(Number),
    pervious_hardscape_percent: SC.Record.attr(Number),
    softscape_and_landscape_percent: SC.Record.attr(Number),
    irrigated_percent: SC.Record.attr(Number),
    hardscape_percent: SC.Record.attr(Number),
    residential_irrigated_square_feet: SC.Record.attr(Number),
    commercial_irrigated_square_feet: SC.Record.attr(Number),
    residential_average_lot_size: SC.Record.attr(Number),
    gross_net_ratio: SC.Record.attr(Number),
    intersection_density: SC.Record.attr(Number),
    combined_pop_emp_density: SC.Record.attr(Number)
});

Footprint.BuildingUseDefinition = Footprint.Record.extend({
    name: SC.Record.attr(String)
});

Footprint.BuildingUsePercent = Footprint.Record.extend({
    building_use_definition: SC.Record.toOne("Footprint.BuildingUseDefinition", {nested: YES}),
    percent: SC.Record.attr(Number),
    vacancy_rate: SC.Record.attr(Number),
    household_size: SC.Record.attr(Number),
    efficiency: SC.Record.attr(Number),
    square_feet_per_unit: SC.Record.attr(Number),
    floor_area_ratio: SC.Record.attr(Number),
    unit_density: SC.Record.attr(Number),
    gross_built_up_area: SC.Record.attr(Number),
    net_built_up_area: SC.Record.attr(Number)
});


Footprint.BuiltForm = Footprint.Record.extend(
    Footprint.Name,
    Footprint.Tags, {

    medium: SC.Record.toOne("Footprint.Medium", {}),
    media: SC.Record.toMany("Footprint.Medium", {}),
    building_attribute_set: SC.Record.toOne("Footprint.BuildingAttributeSet", {isMaster: YES}),
    // The examples used by the visualizer
    examples: SC.Record.toMany("Footprint.BuiltFormExample"),

    // Save all of these records after the main record
    _saveBeforeProperties: function() {
        return ['medium', 'building_attribute_set'] //, 'examples', 'media']
    },

    _cloneProperties: function () {
        return ['medium', 'building_attribute_set'] //, 'examples', 'media'];
    },

    _copyProperties: function () {
        return ['tags']
    },

    _skipProperties: function() {
        return ['origin_instance'];
    },

    // Set the origin Built Form
    _cloneSetup: function(sourceRecord) {
        this.set('origin_instance', sourceRecord);
    },

    _mapAttributes: {
        key: function (record, key, random) {
            return record.get('origin_instance') ?
                'new_%@_%@'.fmt(key, random) :
                'new_%@'.fmt(random);
        },
        name: function (record, name, random) {
            return record.get('origin_instance') ?
                'New %@ %@'.fmt(name, random) :
                'New %@'.fmt(random);
        }
    },

});

Footprint.BuiltFormSet = Footprint.Record.extend(
    Footprint.Key,
    Footprint.Name, {

        built_forms: SC.Record.toMany("Footprint.BuiltForm", {
            nested: NO,
            inverse: "built_form_set",
            isMaster: YES
        }),

        _copyProperties: function () {
            return 'built_forms'.w();
        },
        _mapAttributes: {
            key: function (record, key, random) {
                return record.get('origin_instance') ?
                    key + 'New' :
                    'New %@'.fmt(random);
            },
            name: function (record, name) {
                return record.get('origin_instance') ?
                    name + 'New' :
                    'New %@'.fmt(random);
            }
        },

        treeItemIsExpanded: YES,
        treeItemChildren: function () {
            return this.get("built_forms");
        }.property()
    });

Footprint.FlatBuiltForm = Footprint.Record.extend({
    key: SC.Record.attr(Number),
    intersection_density: SC.Record.attr(Number),
    built_form_type: SC.Record.attr(String),
    gross_net_ratio: SC.Record.attr(Number),
    dwelling_unit_density: SC.Record.attr(Number),
    household_density: SC.Record.attr(Number),
    population_density: SC.Record.attr(Number),
    employment_density: SC.Record.attr(Number),
    single_family_large_lot_density: SC.Record.attr(Number),
    single_family_small_lot_density: SC.Record.attr(Number),
    attached_single_family_density: SC.Record.attr(Number),
    multifamily_2_to_4_density: SC.Record.attr(Number),
    multifamily_5_plus_density: SC.Record.attr(Number),
    armed_forces_density: SC.Record.attr(Number),
    office_density: SC.Record.attr(Number),
    retail_density: SC.Record.attr(Number),
    industrial_density: SC.Record.attr(Number),
    residential_density: SC.Record.attr(Number),
    agricultural_density: SC.Record.attr(Number)
});


Footprint.PrimaryComponent = Footprint.BuiltForm.extend({
    primary_component_percent_set: SC.Record.toMany('Footprint.PrimaryComponentPercent', {isMaster: NO}),
    _skipProperties: function () {
        return (sc_super() || []).concat(['primary_component_percent_set']);
    }
});

Footprint.PrimaryComponentPercent = Footprint.Record.extend({
    primary_component: SC.Record.toOne("Footprint.PrimaryComponent", {nested: NO, inverse:'primary_component_percent_set'}),
    percent: SC.Record.attr(Number)
});

Footprint.PlacetypeComponent = Footprint.BuiltForm.extend({
    primary_component_percents: SC.Record.toMany('Footprint.PrimaryComponentPercent', {nested: YES}),
    placetype_component_percent_set: SC.Record.toMany('Footprint.PlacetypeComponentPercent', {isMaster: NO}),
    _copyProperties: function () {
        return (sc_super() || []).concat(['primary_component_percents']);
    },
    _skipProperties: function () {
        return (sc_super() || []).concat(['placetype_component_percent_set']);
    }
});

Footprint.PlacetypeComponentPercent = Footprint.Record.extend({
    placetype_component: SC.Record.toOne("Footprint.PlacetypeComponent", {nested: NO, inverse:'placetype_component_percent_set'}),
    percent: SC.Record.attr(Number)
});


Footprint.Placetype = Footprint.BuiltForm.extend({
    placetype_component_percents: SC.Record.toMany('Footprint.PlacetypeComponentPercent', {nested: YES}),
    _copyProperties: function () {
        return (sc_super() || []).concat(['placetype_component_percents']);
    }
});

Footprint.BuiltFormExample = Footprint.Record.extend({
    url_aerial: SC.Record.attr(String),
    url_street: SC.Record.attr(String),
    content: SC.Record.attr(Object)
});
