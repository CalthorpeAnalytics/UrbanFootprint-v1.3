/**
 * Created with PyCharm.
 * User: calthorpe
 * Date: 11/26/13
 * Time: 3:04 PM
 * To change this template use File | Settings | File Templates.
 */

sc_require('views/info_views/built_form/editable_input_field_view');

Footprint.editableBuildingUseTypeView = SC.View.extend({
    childViews:'titleView residentialView retailView officeView industrialView'.w(),
    classNames: ['footprint-editable-building-use-types-view'],
    content: null,
    layout: null,

    titleView: SC.View.extend({
       childViews:'useRateTitle efficiencyTitle sqftPerUnitTitle'.w(),
       useRateTitle: SC.LabelView.extend({
           value: 'Use Types',
           fontWeight: 700,
           textAlign: SC.ALIGN_CENTER,
           layout: {left: 0, width: 0.35, height:24, top: 0}
       }),
       efficiencyTitle: SC.LabelView.extend({
           value: 'Use Efficiency',
           fontWeight: 700,
           textAlign: SC.ALIGN_CENTER,
           layout: {left: 0.35, width: 0.25, height:24, top: 0}
       }),
       sqftPerUnitTitle: SC.LabelView.extend({
           value: 'SqFt Per Unit',
           fontWeight: 700,
           textAlign: SC.ALIGN_CENTER,
           layout: {left: 0.6, width: 0.4, height:24, top: 0}
        })
    }),

    residentialView: Footprint.editableUseTypeRowView.extend({
        use: 'Residential',
        efficiencyValueBinding: SC.Binding.oneWay('.parentView.content').buildingUseFilter('efficiency', 'Residential'),
        sqftValueBinding: SC.Binding.oneWay('.parentView.content').buildingUseFilter('square_feet_per_unit', 'Residential'),
        layout: {height:24, top: 25}
    }),
    retailView: Footprint.editableUseTypeRowView.extend({
        use: 'Retail',
        efficiencyValueBinding: SC.Binding.oneWay('.parentView.content').buildingUseFilter('efficiency', 'Retail'),
        sqftValueBinding: SC.Binding.oneWay('.parentView.content').buildingUseFilter('square_feet_per_unit', 'Retail'),
        layout: {height:24, top: 50}
    }),
    officeView: Footprint.editableUseTypeRowView.extend({
        use: 'Office',
        efficiencyValueBinding: SC.Binding.oneWay('.parentView.content').buildingUseFilter('efficiency', 'Office'),
        sqftValueBinding: SC.Binding.oneWay('.parentView.content').buildingUseFilter('square_feet_per_unit', 'Office'),
        layout: {height:24, top: 75}
    }),

    industrialView: Footprint.editableUseTypeRowView.extend({
        use: 'Industrial',
        efficiencyValueBinding: SC.Binding.oneWay('.parentView.content').buildingUseFilter('efficiency', 'Industrial'),
        sqftValueBinding: SC.Binding.oneWay('.parentView.content').buildingUseFilter('square_feet_per_unit', 'Industrial'),
        layout: {height:24, top: 100}
    })
})