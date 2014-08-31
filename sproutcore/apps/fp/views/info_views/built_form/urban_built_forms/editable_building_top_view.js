/**
 * Created by calthorpe on 4/22/14.
 */

Footprint.EditableBuildingTopView = SC.View.extend({
    classNames: ['footprint-built-form-top-view'],
    childViews:'nameTitleView contentView addressNameTitleView addressContentView'.w(),
    recordType: null,
    content: null,

    nameTitleView: SC.LabelView.extend({
       classNames: ['footprint-bold-title-view'],
       value: 'Building Name',
       fontWeight: 700,
       layout: {left: 25, width: 100, height:24, top: 10}
    }),
    contentView: Footprint.EditableModelStringView.extend({
        layout: {left: 30, width: 280, height:20, top: 30},
        valueBinding: SC.Binding.from('.parentView*content.name'),
        classNames: ['footprint-editable-content-view']
    }),
    addressNameTitleView: SC.LabelView.extend({
       classNames: ['footprint-bold-title-view'],
       value: 'Building Address',
       fontWeight: 700,
       layout: {left: 325, width: 100, height:24, top: 10}
    }),
    addressContentView: Footprint.EditableModelStringView.extend({
       classNames: ['footprint-editable-content-view'],
       valueBinding: SC.Binding.from('.parentView*content.building_attribute_set.address'),
       layout: {left: 330, width: 280, height:20, top: 30}
    })
});


