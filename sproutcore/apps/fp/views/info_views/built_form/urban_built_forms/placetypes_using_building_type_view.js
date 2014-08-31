/**
 * Created with PyCharm.
 * User: calthorpe
 * Date: 12/5/13
 * Time: 12:32 PM
 * To change this template use File | Settings | File Templates.
 */
sc_require('views/info_views/built_form/editable_input_field_view');

Footprint.PlacetypesUsingBuildingTypeView = SC.View.extend({

    classNames: ['footprint-placetypes-using-building-type-view'],
    childViews:'titleView placetypePercentScrollView'.w(),
    content: null,

    titleView: SC.LabelView.extend({
        value: 'Placetypes using BuildingType',
        layout: {left: 30, width: 250, height: 24, top: 0}
    }),

    placetypePercentScrollView: SC.ScrollView.extend({
        classNames: ['footprint-placetype-percent-scroll-view'],
        layout: {left: 40, top: 25, height: 200},
        content: null,
        contentBinding: SC.Binding.oneWay('.parentView.content'),

        contentView: SC.SourceListView.extend({
            isEnabledBinding: SC.Binding.oneWay('.content').bool(),
            rowHeight: 34,
            isEditable: YES,
            actOnSelect: NO,

            contentBinding: SC.Binding.oneWay('.parentView.parentView*content.placetype_component_percent_set'),
            contentValueKey: 'name',
            selection: null,

            exampleView: SC.View.extend(SC.Control, {
                classNames: ['footprint-building-type-member-example-view'],
                layout: { height: 34 },
                displayProperties: 'content'.w(),
                childViews: 'nameLabelView percentLabelView'.w(),
                placetype: null,
                placetypeBinding: SC.Binding.oneWay('*content.placetype'),
                percent: null,
                percentBinding: SC.Binding.oneWay('*content.percent'),

                nameLabelView: SC.LabelView.extend({
                    layout: { top: 0.1, width: 0.7 },
                    valueBinding: SC.Binding.oneWay('.parentView*placetype.name')
                }),
                percentLabelView: SC.LabelView.extend({
                    layout: { left: 0.71, right: 0.02 },
                    percent: null,
                    textAlign: SC.ALIGN_CENTER,
                    percentBinding: SC.Binding.oneWay('.parentView.percent'),
                    value: function() {
                        return '%@ %'.fmt(100*parseFloat(this.get('percent')).toFixed(1));
                    }.property('percent').cacheable()
                })
            })
        })
    })
})