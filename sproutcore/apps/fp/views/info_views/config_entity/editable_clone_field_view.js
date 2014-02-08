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
    layout: null,

    titleView: SC.LabelView.extend({
        layout: { height: 17 },
        valueBinding: SC.Binding.oneWay('.parentView.title')
    }),

    editableContentView: Footprint.EditableModelStringView.extend({
        classNames:'footprint-editable-clone-field-content-view'.w(),
        layout: { top: 17, left: 15 },
        valueBinding: '.parentView.value'
    })
});
