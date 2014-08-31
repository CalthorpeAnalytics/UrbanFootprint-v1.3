/**
 * Created with PyCharm.
 * User: calthorpe
 * Date: 11/26/13
 * Time: 3:07 PM
 * To change this template use File | Settings | File Templates.
 */
sc_require('views/info_views/built_form/editable_input_field_view');
sc_require('views/info_views/built_form/placetype_components_using_primary_component_view');

Footprint.EditableAgricultureAttributeSetView = SC.View.extend({
    classNames: ['footprint-crop-input-view'],
    childViews: [
        'cropYieldView',
        'unitPriceView',
        'costView',
        'waterConsumptionView',
        'laborInputView',
        'truckTripsView',
        'placetypeComponentsUsingPrimaryComponentView'],

    content: null,
    allContent: null,

    cropYieldView: Footprint.EditableInputFieldView.extend({
        layout: {top: 10, left: 30, width: 260, height:20},
        contentBinding: SC.Binding.from('.parentView.content'),
        contentValueKey: 'crop_yield',
        title: 'Crop yield (units) per acre'
    }),
    unitPriceView: Footprint.EditableInputFieldView.extend({
        layout: {top: 40, left: 30, width: 260, height:20},
        contentBinding: SC.Binding.from('.parentView.content'),
        contentValueKey: 'unit_price',
        title: 'Market price of one crop unit'
    }),
    costView: Footprint.EditableInputFieldView.extend({
        layout: {top: 70, left: 30, width: 260, height:20},
        contentBinding: SC.Binding.from('.parentView.content'),
        contentValueKey: 'cost', 
        title: 'Production cost per acre'
    }),
    waterConsumptionView: Footprint.EditableInputFieldView.extend({
        layout: {top: 100, left: 30, width: 260, height:20},
        contentBinding: SC.Binding.from('.parentView.content'),
        contentValueKey: 'water_consumption', 
        title: 'Water consumption per acre'
    }),
    laborInputView: Footprint.EditableInputFieldView.extend({
        layout: {top: 130, left: 30, width: 260, height:20},
        contentBinding: SC.Binding.from('.parentView.content'),
        contentValueKey: 'labor_input', 
        title: 'Labor input per acre'
    }),
    truckTripsView: Footprint.EditableInputFieldView.extend({
        layout: {top: 160, left: 30, width: 260, height:20},
        contentBinding: SC.Binding.from('.parentView.content'),
        contentValueKey: 'truck_trips', 
        title: 'Truck trips per acre of crop'
    }),

    placetypeComponentsUsingPrimaryComponentView: Footprint.PlacetypeComponentsUsingPrimaryComponentView.extend({
        title: "CropTypes using Crop",
        layout: {left: 310, top:10, height: 180},
        contentBinding: SC.Binding.oneWay('.parentView.allContent')
    })
})