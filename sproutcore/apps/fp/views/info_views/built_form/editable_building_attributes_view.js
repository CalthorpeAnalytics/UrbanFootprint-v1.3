/**
 * Created with PyCharm.
 * User: calthorpe
 * Date: 11/26/13
 * Time: 3:07 PM
 * To change this template use File | Settings | File Templates.
 */
sc_require('views/info_views/built_form/editable_input_field_view');
sc_require('views/info_views/built_form/editable_building_use_type_view');

Footprint.EditableBuildingAttributesView = SC.View.extend({
    classNames: ['footprint-building-input-view'],
    childViews:'buildingStoriesView totalFarView parkingSpacesView parkingSqFtView hardscapePercentView irrigatedPercentView imperviousPercentView vacancyRateView householdSizeView residentialLotSqFtView editableBuildingUseTypeView'.w(),

    content: null,

    layout: {left: 330, bottom:40, top: 340, width: 650},

    buildingStoriesView: Footprint.editableInputFieldView.extend({
        layout: {top: 10, left: 30, width: 260, height:20},
        contentBinding: SC.Binding.oneWay('.parentView*content.building_attribute_set.floors'),
        value: 'Building Stories'
    }),
    totalFarView: Footprint.editableInputFieldView.extend({
        layout: {top: 40, left: 30, width: 260, height:20},
        contentBinding: SC.Binding.oneWay('.parentView*content.building_attribute_set.total_far'),
        value: 'Total FAR'
    }),
    parkingSpacesView: Footprint.editableInputFieldView.extend({
        layout: {top: 70, left: 30, width: 260, height:20},
        contentBinding: SC.Binding.oneWay('.parentView*content.building_attribute_set.parking_spaces'),
        value: 'Parking Spaces'
    }),
    parkingSqFtView: Footprint.editableInputFieldView.extend({
        layout: {top: 100, left: 30, width: 260, height:20},
        contentBinding: SC.Binding.oneWay('.parentView*content.building_attribute_set.parking_structure_square_feet'),
        value: 'Parking Structure SqFt'
    }),
    hardscapePercentView: Footprint.editableInputFieldView.extend({
        layout: {top: 130, left: 30, width: 260, height:20},
        contentBinding: SC.Binding.oneWay('.parentView*content.building_attribute_set.hardscape_percent'),
        value: 'Hardscape Percent'
    }),
    irrigatedPercentView: Footprint.editableInputFieldView.extend({
        layout: {top: 160, left: 30, width: 260, height:20},
        contentBinding: SC.Binding.oneWay('.parentView*content.building_attribute_set.irrigated_percent'),
        value: 'Irrigated Percent'
    }),
    imperviousPercentView: Footprint.editableInputFieldView.extend({
        layout: {top: 190, left: 30, width: 260, height:20},
        contentBinding: SC.Binding.oneWay('.parentView*content.building_attribute_set.impervious_roof_percent'),
        value: 'Impervious Use Percent'
    }),
    vacancyRateView: Footprint.editableInputFieldView.extend({
        layout: {top: 145, left: 320, width: 260, height:20},
        contentBinding: SC.Binding.oneWay('.parentView*content.building_attribute_set').buildingUseFilter('vacancy_rate', 'Residential'),
        value: 'Vacancy Rate'
    }),

    householdSizeView: Footprint.editableInputFieldView.extend({
        layout: {top: 170, left: 320, width: 260, height:20},
        contentBinding: SC.Binding.oneWay('.parentView*content.building_attribute_set').buildingUseFilter('household_size', 'Residential'),
        value: 'Household Size'
    }),

    residentialLotSqFtView: Footprint.editableInputFieldView.extend({
        layout: {top: 195, left: 320, width: 260, height:20},
        contentBinding: SC.Binding.oneWay('.parentView*content.building_attribute_set.residential_average_lot_size'),
        value: 'SF Lot Square Feet'
    }),

    editableBuildingUseTypeView: Footprint.editableBuildingUseTypeView.extend({
        layout: {left: 320, width: 320, height: 125, top:10},
        contentBinding: SC.Binding.oneWay('.parentView*content.building_attribute_set')
    })
})