/**
 * Created with PyCharm.
 * User: calthorpe
 * Date: 12/11/13
 * Time: 5:26 PM
 * To change this template use File | Settings | File Templates.
 */

sc_require('views/clear_button_view');


Footprint.EditableBuildingTypesTaggedBuildingsView = SC.View.extend({
    layout: {left: 975, top: 0.55, bottom: 50},
    childViews:'titleView buildingTypeListView buildingTypeSelectButtonView'.w(),

    content:null,
    selection: null,

    titleView: SC.LabelView.extend({
        value: 'Building Type Membership',
        layout: {height: 20, top: 3},
        textAlign: SC.ALIGN_CENTER
    }),

    buildingTypeListView:SC.ScrollView.extend({
        layout: { left:10, right:10, top: 23, bottom: 60},

        contentBinding: SC.Binding.oneWay('.parentView*selection.firstObject'),

        contentView: SC.SourceListView.extend({
            isEnabledBinding: SC.Binding.oneWay('.content').bool(),
            rowHeight: 34,
            isEditable: YES,
            actOnSelect: NO,
            canEditContent: YES,
            canDeleteContent: YES,
            canReorderContent: YES,

            contentBinding: SC.Binding.oneWay('.parentView.parentView*content.placetype_components'),
            contentValueKey: 'name',
            selection: null,

            exampleView: SC.View.extend(SC.Control, {
                classNames: ['footprint-building-type-member-example-view'],
                layout: { height: 34 },
                displayProperties: 'content'.w(),
                childViews: 'nameLabelView removeBuildingTypeButtonView'.w(),
                content: null,
                contentBinding: SC.Binding.oneWay('*content'),

                nameLabelView: SC.LabelView.extend({
                    layout: { left: 0.02, top: 0.1, right: 24 },
                    valueBinding: SC.Binding.oneWay('.parentView.content.name')
                }),
                removeBuildingTypeButtonView: Footprint.ClearButtonView.extend({
                    isVisibleBinding: SC.Binding.oneWay('.parentView*content.name').bool(),
                    layout: {right: 0, width: 24},
                    action: 'doRemoveBuildingType'
                })
            })
        })
    }),

    buildingTypeSelectButtonView: Footprint.SelectInfoView.extend({
        classNames:'footprint-query-info-group-by-view'.w(),
        layout: {bottom:25, left:.05, right: 0.05, height: 24},
        includeNullItem:YES,
        nullTitle: 'None',
        recordType: Footprint.PlacetypeComponent,
        contentBinding: SC.Binding.oneWay('Footprint.buildingTypesEditController.content'),
        selectionBinding: 'Footprint.buildingTypesEditController.selection',
        itemTitleKey:'name'
    })
})