/**
 * Created with PyCharm.
 * User: calthorpe
 * Date: 1/9/14
 * Time: 4:34 PM
 * To change this template use File | Settings | File Templates.
 */

Footprint.TopLabeledResultView = SC.View.extend({
    classNames: "footprint-top-labeled-result-view".w(),
    childViews: ['titleSpaceView', 'valueSpaceView'],
    result: null,
    title: null,
    columnName: null,

    columnValue: function() {
        var content = this.get('result')
        var column_name = this.get('columnName')
        if (!content)
            return '--';
        var value = parseFloat(content[column_name]).toFixed(0)

        return value ? d3.format(',f')(value) : '--';
    }.property('result', 'columnName').cacheable(),

    titleSpaceView: SC.View.extend({
        classNames: "footprint-top-labeled-result-title-view".w(),
        childViews: ['titleView'],
        title:null,
        titleBinding: SC.Binding.oneWay('.parentView.title'),
        layout: {height: 0.5},

        titleView: SC.LabelView.extend({
            classNames: "footprint-top-labeled-result-title-space-view".w(),
            layout: {top:2, bottom: 2, left:5},
            valueBinding: SC.Binding.oneWay('.parentView.title')
        })
    }),

    valueSpaceView: SC.View.extend({
        classNames: "footprint-top-labeled-result-value-space-view".w(),
        childViews: ['valueView'],
        layout: {top: 0.5},
        columnValue: null,
        columnValueBinding: SC.Binding.oneWay('.parentView.columnValue'),
        valueView: SC.LabelView.extend({
            classNames: "footprint-top-labeled-result-value-view".w(),
            layout: {top: 4},
            valueBinding: SC.Binding.oneWay('.parentView.columnValue'),
            textAlign: SC.ALIGN_CENTER
        })
    })
});
