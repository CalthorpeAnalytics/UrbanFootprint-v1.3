/**
 * Created with PyCharm.
 * User: calthorpe
 * Date: 11/26/13
 * Time: 3:07 PM
 * To change this template use File | Settings | File Templates.
 */
sc_require('views/info_views/built_form/editable_input_field_view');
sc_require('views/info_views/built_form/urban_built_forms/editable_building_use_type_view');
sc_require('views/info_views/built_form/urban_built_forms/building_donut_chart_view');

Footprint.EditableBuildingAttributeSetView = SC.View.extend({

    classNames: ['footprint-building-input-view'],
    childViews:['nameTitleView', 'websiteView', 'buildingDonutChartView', 'buildingTitleView', 'parcelCompTitleView', 'parkingTitleView',
        'parcelCharacteristicsTitleView', 'lotSizeView', 'buildingStoriesView', 'totalFarView',
        'surfaceParkingSpacesView', 'aboveStructuredParkingView', 'belowStructuredParkingView', 'residentialVacancyView',
        'householdSizeView', 'averageParkingSqftView', 'buildingFootprintView', 'parkingSqFtView',
        'otherHardscapeSqFtView', 'irrigatedSqFtView', 'nonIrrigatedSqFtView',
        'irrigatedPercentView', 'residentialCharacteristicsTitleView'],

    content: null,
    selectedItem: null,

    nameTitleView: SC.LabelView.extend({
       classNames: ['footprint-bold-title-view'],
       value: 'Building Website',
       fontWeight: 700,
       layout: {left: 25, width: 120, height:20, top: 10}
    }),

    websiteView: Footprint.EditableModelStringView.extend({
       classNames: ['footprint-editable-content-view'],
       valueBinding: SC.Binding.oneWay('.parentView*content.website'),
       layout: {left: 30, width: 280, height:20, top: 30}
    }),

    buildingDonutChartView: Footprint.buildingParcelAreaChartView.extend({
        layout: {left: 420, height:200, width: 200},
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        selectedItemBinding: SC.Binding.oneWay('.parentView.selectedItem')
    }),

    buildingTitleView: SC.LabelView.extend({
        classNames: ['footprint-bold-title-view'],
        value: 'Parcel/Building',
        layout: {height: 20, width: 100, left:25, top:60}
    }),

    parcelCompTitleView: SC.LabelView.extend({
        classNames: ['footprint-bold-title-view'],
        value: 'Parcel \n Composition',
        layout: {height: 40, width: 90, left:360, top:10}
    }),

    parkingTitleView: SC.LabelView.extend({
        classNames: ['footprint-bold-title-view'],
        value: 'Parking',
        layout: {height: 20, width: 100, left:155, top: 60}
    }),

    residentialCharacteristicsTitleView: SC.LabelView.extend({
        classNames: ['footprint-bold-title-view'],
        value: 'Residential',
        layout: {height: 20, width: 100, left:290, top: 110}
    }),
    parcelCharacteristicsTitleView: SC.LabelView.extend({
        classNames: ['footprint-bold-title-view'],
        value: 'Parcel Hardscape/Softscape Square Feet',
        layout: {height: 20, width: 250, left:25, top:225}
    }),

    lotSizeView: Footprint.EditableFieldView.extend({
        layout: {top: 85, left: 30, width: 120, height:30},
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        contentValueKey: 'lot_size_square_feet',
        title: 'Lot Size (Square Feet)'
    }),
    buildingStoriesView: Footprint.EditableFieldView.extend({
        layout: {top: 130, left: 30, width: 120, height:30},
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        contentValueKey: 'floors',
        title: 'Building Stories'
    }),

    totalFarView: Footprint.EditableFieldView.extend({
        layout: {top: 175, left: 30, width: 120, height:30},
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        contentValueKey: 'total_far',
        title: 'Total FAR'
    }),
    surfaceParkingSpacesView: Footprint.EditableFieldView.extend({
        layout: {top: 85, left: 155, width: 140, height:30},
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        contentValueKey: 'surface_parking_spaces',
        title: 'Surface Parking Spaces'
    }),

    aboveStructuredParkingView: Footprint.EditableFieldView.extend({
        layout: {top: 130, left: 155, width: 140, height:30},
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        contentValueKey: 'above_ground_structured_parking_spaces',
        title: 'Structured - At/Above Ground'
    }),

    belowStructuredParkingView: Footprint.EditableFieldView.extend({
        layout: {top: 175, left: 155 , width: 140, height:30},
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        contentValueKey: 'below_ground_structured_parking_spaces',
        title: 'Structured - Below Ground'
    }),

    residentialVacancyView: Footprint.EditableFieldView.extend({
        layout: {top: 130, left: 290 , width: 140, height:30},
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        contentValueKey: 'vacancy_rate',
        title: 'Residential Vacancy Rate'
    }),

    householdSizeView: Footprint.EditableFieldView.extend({
        layout: {top: 175, left: 290 , width: 140, height:30},
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        contentValueKey: 'household_size',
        title: 'Household Size (avg)'
    }),

    averageParkingSqftView: Footprint.LeftEditableInputFieldView.extend({
        classNames: ['footprint-irrigated-percent-view'],
        layout: {top: 55, left: 220 , width: 125, height:25},
        decimalValueBinding: SC.Binding.from('.parentView*content.average_parking_space_square_feet'),
        contentLayout: {width:.3, top: 4, bottom: 4},
        contentLabel: '',
        title: 'Square Feet \n per Parking Space'
    }),

    buildingFootprintView: Footprint.EditableBottomLabelledView.extend({
        classNames: ['footprint-building-footprint-view'],
        layout: {top: 245, left: 30, width: 100, height:32},
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        contentValueKey: 'building_footprint_square_feet',
        title: 'Building Footprint SqFt'
    }),

    parkingSqFtView: Footprint.NonEditableBottomLabelledView.extend({
        classNames: ['footprint-parking-sqft-view'],
        layout: {top: 245, left: 150, width: 100, height:32},
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        statusBinding: SC.Binding.oneWay('.parentView*content.status'),

        computeValueObserver: function() {
            if (this.get('status') != SC.Record.READY_DIRTY) {
                return
            }
            var average_parking_sqft = parseFloat(this.getPath('content.average_parking_space_square_feet'));
            var surface_parking_spaces = parseFloat(this.getPath('content.surface_parking_spaces'));

            var surface_parking_sqft = parseFloat((average_parking_sqft * surface_parking_spaces).toFixed(1));

            if (surface_parking_sqft < 0 || surface_parking_sqft > 0 || surface_parking_sqft == 0) {
                this.get('content').setIfChanged(this.get('contentValueKey'), surface_parking_sqft);
            }
        }.observes('*content.average_parking_space_square_feet', '*content.surface_parking_spaces' , 'status'),

        contentValueKey: 'surface_parking_square_feet',
        title: 'Surface Parking SqFt'
    }),

    otherHardscapeSqFtView: Footprint.EditableBottomLabelledView.extend({
        classNames: ['footprint-other-hardscape-view'],
        layout: {top: 245, left: 270, width: 100, height:32},
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        contentValueKey: 'hardscape_other_square_feet',
        title: 'Other Hardscape SqFt'
    }),

    irrigatedSqFtView: Footprint.NonEditableBottomLabelledView.extend({
        classNames: ['footprint-irrigated-softscape-view'],
        layout: {top: 245, left: 510, width: 100, height:32},
        statusBinding: SC.Binding.oneWay('.parentView*content.status'),

        computeValueObserver: function() {
            if (this.get('status') != SC.Record.READY_DIRTY) {
                return
            }

            var building_footprint_square_feet = parseFloat(this.getPath('content.building_footprint_square_feet'));
            var surface_parking_square_feet = parseFloat(this.getPath('content.surface_parking_square_feet'));
            var hardscape_other_square_feet = parseFloat(this.getPath('content.hardscape_other_square_feet'));
            var lot_size_square_feet = parseFloat(this.getPath('content.lot_size_square_feet'));
            var irrigated_percent = parseFloat(this.getPath('content.irrigated_percent'));

            var irrigated_softscape_square_feet = parseFloat(((lot_size_square_feet - (building_footprint_square_feet + surface_parking_square_feet + hardscape_other_square_feet)) * irrigated_percent).toFixed(1));

            if (irrigated_softscape_square_feet < 0 || irrigated_softscape_square_feet > 0 || irrigated_softscape_square_feet == 0) {
                this.get('content').setIfChanged(this.get('contentValueKey'), irrigated_softscape_square_feet);
            }
        }.observes('*content.building_footprint_square_feet', '*content.surface_parking_square_feet', '*content.hardscape_other_square_feet', '*content.lot_size_square_feet', '*content.irrigated_percent', 'status'),

        contentBinding: SC.Binding.oneWay('.parentView.content'),
        contentValueKey: 'irrigated_softscape_square_feet',
        title: 'Irrigated SqFt'
    }),

    nonIrrigatedSqFtView: Footprint.NonEditableBottomLabelledView.extend({
        classNames: ['footprint-non-irrigated-softscape-view'],
        layout: {top: 245, left: 390, width: 100, height:32},
        statusBinding: SC.Binding.oneWay('.parentView*content.status'),

        computeValueObserver: function() {
            if (this.get('status') != SC.Record.READY_DIRTY) {
                return
            }

            var building_footprint_square_feet = parseFloat(this.getPath('content.building_footprint_square_feet'));
            var surface_parking_square_feet = parseFloat(this.getPath('content.surface_parking_square_feet'));
            var hardscape_other_square_feet = parseFloat(this.getPath('content.hardscape_other_square_feet'));
            var lot_size_square_feet = parseFloat(this.getPath('content.lot_size_square_feet'));
            var irrigated_percent = parseFloat(this.getPath('content.irrigated_percent'));

            var nonirrigated_softscape_square_feet = parseFloat(((lot_size_square_feet - (building_footprint_square_feet + surface_parking_square_feet + hardscape_other_square_feet)) * (1 - irrigated_percent)).toFixed(1));

            if (nonirrigated_softscape_square_feet < 0 || nonirrigated_softscape_square_feet > 0 || nonirrigated_softscape_square_feet == 0) {
                this.get('content').setIfChanged(this.get('contentValueKey'), nonirrigated_softscape_square_feet);
            }
        }.observes('*content.building_footprint_square_feet', '*content.surface_parking_square_feet', '*content.hardscape_other_square_feet', '*content.lot_size_square_feet', '*content.irrigated_percent', 'status'),

        contentBinding: SC.Binding.oneWay('.parentView.content'),
        contentValueKey: 'nonirrigated_softscape_square_feet',
        title: 'Non-Irrigated Softscape SqFt'
    }),

    irrigatedPercentView: Footprint.LeftEditableInputFieldView.extend({
        classNames: ['footprint-irrigated-percent-view'],
        layout: {top: 220, left: 510, width: 120, height:17},
        decimalValueBinding: SC.Binding.from('.parentView*content.irrigated_percent'),
        contentLayout: {width:.3},
        title: 'Percent Irrigated',
        contentLabel: '%',
        isPercent: YES
    })

})