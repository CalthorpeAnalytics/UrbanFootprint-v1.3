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

    layout: {left: 330, height:70, top: 0, width: 650},


    nameTitleView: SC.LabelView.extend({
       valueBinding: SC.Binding.oneWay('.parentView.titleValue'),
       fontWeight: 700,
       layout: {left: 30, width: 100, height:24, top: 18}
    }),
    contentView: Footprint.EditableModelStringView.extend({
       valueBinding: SC.Binding.oneWay('.parentView*content.name'),
       layout: {left: 150, width: 300, height:35, top: 15},
       backgroundColor: '#F8F8F8'
    }),
})
