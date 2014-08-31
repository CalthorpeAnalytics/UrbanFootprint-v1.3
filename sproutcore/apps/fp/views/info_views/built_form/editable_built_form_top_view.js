/**
 * Created with PyCharm.
 * User: calthorpe
 * Date: 11/26/13
 * Time: 4:58 PM
 * To change this template use File | Settings | File Templates.
 */




Footprint.EditableBuiltFormTopView = SC.View.extend({
    classNames: ['footprint-built-form-top-view'],
    childViews:'nameTitleView contentView'.w(),
    recordType: null,
    content: null,
    titleValue: null,

    nameTitleView: SC.LabelView.extend({
       classNames: ['footprint-bold-title-view'],
       valueBinding: SC.Binding.oneWay('.parentView.titleValue'),
       fontWeight: 700,
       layout: {left: 25, width: 100, height:24, top: 10}
    }),

    contentView: Footprint.EditableModelStringView.extend({
       classNames: ['footprint-editable-content-view'],
       valueBinding: SC.Binding.from('.parentView*content.name'),
       layout: {left: 30, height:20, top: 30, width: 450}
    })
})
