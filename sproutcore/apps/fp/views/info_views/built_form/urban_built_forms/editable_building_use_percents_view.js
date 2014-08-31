/**
 * Created with PyCharm.
 * User: calthorpe
 * Date: 11/26/13
 * Time: 4:08 PM
 * To change this template use File | Settings | File Templates.
 */

sc_require('views/info_views/built_form/editable_input_field_view');

Footprint.EditableBuildingUsePercentView = SC.View.extend({
    classNames: ['footprint-editable-building-use-percents-view'],
    childViews:'titlesView buildingUsePercentScrollView'.w(),

    // The editable BuildingUsePercents of a BuiltForm
    content: null,
    allContent: null,

    titlesView: SC.View.extend({
        layout: {left: 30, width: 600, height: 24, top: 10},
        childViews:'nameTitleView sqftTitleView efficiencyTitleView percentTitleView'.w(),

        nameTitleView: SC.LabelView.extend({
            classNames: ['footprint-bold-title-view'],
            value: 'Building Uses',
            layout: {left: 0, width: .3}
        }),
        sqftTitleView: SC.LabelView.extend({
            classNames: ['footprint-use-percent-title-view'],
            textAlign: SC.ALIGN_CENTER,
            value: 'Square Feet Per Unit',
            layout: {left: .3, width: .2}
        }),
        efficiencyTitleView: SC.LabelView.extend({
            classNames: ['footprint-use-percent-title-view'],
            textAlign: SC.ALIGN_CENTER,
            value: 'Efficiency (%)',
            layout: {left: .55, width: .2}
        }),
        percentTitleView: SC.LabelView.extend({
            classNames: ['footprint-use-percent-title-view'],
            value: 'Use Percents',
            textAlign: SC.ALIGN_CENTER,
            layout: {left: .8, width: .2}
        })
    }),

    buildingUsePercentScrollView: SC.ScrollView.extend({
        classNames: ['footprint-building-use-percent-scroll-view'],
        layout: {right: 15, left: 30, top: 25, bottom: 7},
        contentBinding: SC.Binding.oneWay('Footprint.buildingUseDefinitionsEditController.arrangedObjects'),

        contentView: SC.SourceListView.extend({
            classNames: ['footprint-building-use-percent-source-list-view'],
            rowHeight: 20,
            isEditable: YES,
            content:null,
            contentBinding: SC.Binding.oneWay('.parentView.parentView.parentView.content'),

            exampleView: Footprint.EditableUsePercentFieldView.extend({
                decimalValueBinding: '*content.percent'
            })
        })
    })
})