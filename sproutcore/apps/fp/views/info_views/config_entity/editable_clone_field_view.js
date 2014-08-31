/**
 * Created with PyCharm.
 * User: calthorpe
 * Date: 12/11/13
 * Time: 10:25 AM
 * To change this template use File | Settings | File Templates.
 */


Footprint.EditableCloneFieldView = SC.View.extend({
    classNames:'footprint-editable-clone-field-view'.w(),
    childViews:['titleView', 'editableContentView'],

    value: null,
    title:null,
    titleViewLayout: { height: 17 },
    editableContentViewLayout: { top: 17, left: 15 },
    isEditable: YES,

    titleView: SC.LabelView.extend({
        layoutBinding: SC.Binding.oneWay('.parentView.titleViewLayout'),
        valueBinding: SC.Binding.oneWay('.parentView.title')
    }),

    editableContentView: Footprint.EditableModelStringView.extend({
        classNames:['footprint-editable-clone-field-content-view', 'footprint-editable-content-view'],
        layoutBinding: SC.Binding.oneWay('.parentView.editableContentViewLayout'),
        isEditableBinding: SC.Binding.oneWay('.parentView.isEditable'),
        valueBinding: '.parentView.value'
    })
});
