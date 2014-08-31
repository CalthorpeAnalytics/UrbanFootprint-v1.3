/**
 * Created with PyCharm.
 * User: calthorpe
 * Date: 12/5/13
 * Time: 12:32 PM
 * To change this template use File | Settings | File Templates.
 */
sc_require('views/info_views/built_form/editable_input_field_view');
sc_require('views/info_views/built_form/editable_built_form_source_list_view');
sc_require('views/info_views/built_form/editable_built_form_select_view');

Footprint.EditableCropsOfCropTypeView = SC.View.extend({

    classNames: ['footprint-editable-building-type-attributes-view'],
    childViews:['titleView', 'usePctTitleView','cropPercentScrollView',
        'builtFormsLabelSelectView', 'normalizePercentsView'],
    content: null,

    titleView: SC.LabelView.extend({
        value: 'Included Crops in Crop Type',
        layout: {left: 30, width: 250, height: 24, top: 0}
    }),

    usePctTitleView: SC.LabelView.extend({
        classNames: ['footprint-editable-crop-type-attributes-use-pct-label'],
        layout: {width: 50, height: 22, left: 575, top: 10},
        value: 'Percent'
    }),

    cropPercentScrollView: SC.ScrollView.extend({
        classNames: ['footprint-crop-type-percent-scroll-view'],
        layout: {left: 40, width: 600, top: 25, height: 160},
        contentView: SC.SourceListView.extend({
            isEnabledBinding: SC.Binding.oneWay('.content').bool(),
            rowHeight: 20,
            isEditable: YES,
            actOnSelect: NO,
            canEditContent: YES,
            canDeleteContent: YES,
            canReorderContent: YES,
            contentBinding: SC.Binding.oneWay('.parentView.parentView.parentView.content'),
            contentValueKey: 'name',

            exampleView: Footprint.EditableBuiltFormSourceListView.extend({
                editController: Footprint.cropTypesEditController,
                childViews: ['removeButtonView', 'nameLabelView', 'percentLabelView'],
                subclassedContentBinding:SC.Binding.oneWay('*content.subclassedComponent'),
                decimalValueBinding: '*content.percent'
            })
        })
    }),

    builtFormsLabelSelectView: Footprint.LabelSelectView.extend({
        layout: {left: 38, width: 500, top: 190, height: 24},
        contentBinding: SC.Binding.oneWay('Footprint.cropsEditController.arrangedObjects'),
        itemTitleKey: 'name',
        selectionAction: 'doPickComponentPercent',
        nullTitle: 'Add a Crop to the mix'
    }),

    normalizePercentsView: SC.ButtonView.extend({
        layout: {left: 575, width: 50, top:190, height: 24},
        title: '|| % ||',
        // This is here to sent to the action handler
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        action: 'doNormalizePercents'
    })
})