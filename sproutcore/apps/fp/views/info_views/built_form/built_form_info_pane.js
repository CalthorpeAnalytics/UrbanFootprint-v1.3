/**
 * Created with PyCharm.
 * User: calthorpe
 * Date: 12/9/13
 * Time: 10:08 AM
 * To change this template use File | Settings | File Templates.
 */

sc_require('views/info_views/built_form/manage_building_view');
sc_require('views/info_views/built_form/manage_building_type_view');
sc_require('views/info_views/built_form/manage_placetype_view');


Footprint.BuiltFormInfoPane = SC.PalettePane.extend(SC.ActionSupport,{
    classNames: ['footprint-add-building-pane'],
    layout: { top: 100, width: 1250, right: 280, height: 650 },
    nowShowing:function() {
        return this.getPath('context.nowShowing') || 'Footprint.ManageBuildingView';
    }.property('context').cacheable(),
    contentView: SC.ContainerView.design({
        classNames: ['footprint-add-built-form-container-view'],
        childViews: ['copyButtonView', 'deleteButtonView', 'buttonsView'],

        recordType: null,
        // The recordType is stored in the contentView of this view (the nowShowing view)
        recordTypeBinding: SC.Binding.oneWay('*contentView.recordType'),
        // Likewise for the current selectedItem
        selectedItemBinding: SC.Binding.oneWay('*contentView.selectedItem'),


        buttonsView: SC.SegmentedView.extend({
            layout: {top: 5, centerY:0, height:22},
            crudType: 'view',
            itemTitleKey: 'title',
            itemActionKey: 'action',
            items: [
                {title: 'Building',  action: 'doManageBuildings'},
                {title: 'Building Type', action: 'doManageBuildingTypes'},
                {title: 'Placetype', action: 'doManagePlaceTypes'}
            ]
        }),
        nowShowingBinding: SC.Binding.oneWay('.parentView.nowShowing')
    })
})



