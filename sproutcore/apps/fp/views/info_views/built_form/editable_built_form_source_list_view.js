/**
 *
 * Created by calthorpe on 2/19/14.
 */

Footprint.EditableBuiltFormSourceListView = SC.View.extend(SC.Control, {
    classNames: ['footprint-built-form-percent-list-scroll-view'],
    layout: { height: 24 },
    childViews: ['removeButtonView', 'nameLabelView', 'dwellingUnitLabelView', 'employmentLabelView', 'percentLabelView'],
    // Content is what we are editing, which is a BuildingTypeComponentPercent instance a PlacetypeComponentPercent instance, or similar
    content: null,
    // The decimal that is editable, which is the percent that the component is of the set
    decimalValue: null,
    subclassedContent: null,
    editController: null,

    removeButtonView: Footprint.DeleteButtonView.extend({
        layout: { left: 0, width: 16, centerY: 0, height: 16},
        action: 'doRemoveRecord',
        contentBinding: SC.Binding.oneWay('.parentView.content')
    }),

    nameLabelView: SC.LabelView.extend({
        layout: { left: 20, width:370 },
        valueBinding: SC.Binding.oneWay('.parentView*subclassedContent.name')
    }),
    dwellingUnitLabelView: SC.LabelView.extend({
        layout: { right: 135, width:45 },
        rawData: null,
        rawDataBinding: SC.Binding.oneWay('.parentView*subclassedContent.flat_building_densities.dwelling_unit_density'),
        value: function(){
            return parseFloat(this.get('rawData')).toFixed(1);
        }.property('rawData').cacheable(),
        backgroundColor: '#F0F8FF',
        textAlign: SC.ALIGN_CENTER
    }),
    employmentLabelView: SC.LabelView.extend({
        layout: { right: 90, width:45 },
        rawData: null,
        rawDataBinding: SC.Binding.oneWay('.parentView*subclassedContent.flat_building_densities.employment_density'),
        value: function(){
            return parseFloat(this.get('rawData')).toFixed(1);
        }.property('rawData').cacheable(),
        backgroundColor: '#F0F8FF',
        textAlign: SC.ALIGN_CENTER
    }),
    percentLabelView: Footprint.EditableModelStringView.extend({
        classNames: ['footprint-editable-content-view'],
        layout: { right: 0, width: 90 },
        editController: null,
        editControllerBinding: SC.Binding.oneWay('.parentView.editController'),
        decimalValue: null,
        decimalValueBinding: SC.Binding.from('.parentView.decimalValue'),
        value: function(propKey, value) {
            editController = this.get('editController');

            if (editController) {
                editController.set('updateSummaryAttributes', YES);
            }
            if (value) {
                // parse the float and round. This eliminates anything the user enters beyond 2 decimal places.
                var roundedValue = parseFloat(value).toFixed(1);
                // Parse the rounded value and divide to a decimal for setting
                this.set('decimalValue', parseFloat(roundedValue)/100);

                // Still return the percent with rounding
                return roundedValue;
            }
            else {
                // Multiply to a percent
                return (100*parseFloat(this.get('decimalValue'))).toFixed(1);
            }
        }.property('decimalValue').cacheable(),

        backgroundColor: '#F0F8FF',
        textAlign: SC.ALIGN_CENTER
    })
});

