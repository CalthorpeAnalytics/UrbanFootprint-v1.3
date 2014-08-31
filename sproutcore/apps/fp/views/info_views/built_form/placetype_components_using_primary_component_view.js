/**
 * Created with PyCharm.
 * User: calthorpe
 * Date: 12/11/13
 * Time: 5:26 PM
 * To change this template use File | Settings | File Templates.
 */

sc_require('views/clear_button_view');


Footprint.PlacetypeComponentsUsingPrimaryComponentView = SC.View.extend({
    classNames: ['footprint-placetype-component-using-primary-component-view'],
    childViews:'titleView placetypeComponentListView'.w(),
    title: null,
    content:null,
    selection: null,

    titleView: SC.LabelView.extend({
        classNames: ['footprint-bold-title-view'],
        valueBinding: SC.Binding.oneWay('.parentView.title'),
        layout: {height: 20, top: 3},
        textAlign: SC.ALIGN_CENTER
    }),

    placetypeComponentListView:SC.ScrollView.extend({
        layout: { left:10, right:10, top: 23, bottom: 10},

        contentBinding: SC.Binding.oneWay('.parentView.content'),

        contentView: SC.SourceListView.extend({
            isEnabledBinding: SC.Binding.oneWay('.content').bool(),
            rowHeight: 34,
            isEditable: YES,
            actOnSelect: NO,
            canEditContent: YES,
            canDeleteContent: YES,
            canReorderContent: YES,

            contentBinding: SC.Binding.oneWay('.parentView.parentView*content.primary_component_percent_set'),
            contentValueKey: 'name',
            selection: null,

            exampleView: SC.View.extend(SC.Control, {
                classNames: ['footprint-building-type-member-example-view'],
                layout: { height: 34 },
                displayProperties: 'content'.w(),
                childViews: 'nameLabelView percentLabelView'.w(),
                placetypeComponent: null,
                placetypeComponentBinding: SC.Binding.oneWay('*content.placetype_component'),
                percent: null,
                percentBinding: SC.Binding.oneWay('*content.percent'),

                nameLabelView: SC.LabelView.extend({
                    layout: { left: 0.02, width: 0.7 },
                    valueBinding: SC.Binding.oneWay('.parentView*placetypeComponent.name')
                }),
                percentLabelView: SC.LabelView.extend({
                    layout: { left: 0.71, right: 0.02 },
                    percent: null,
                    percentBinding: SC.Binding.oneWay('.parentView.percent'),
                    textAlign: SC.ALIGN_CENTER,
                    value: function() {
                        return '%@ %'.fmt(100*parseFloat(this.get('percent')).toFixed(1));
                    }.property('percent').cacheable()
                })
            })
        })
    })
})

