/**
 * Created with PyCharm.
 * User: calthorpe
 * Date: 12/9/13
 * Time: 10:08 AM
 * To change this template use File | Settings | File Templates.
 */

sc_require('views/info_views/built_form/urban_built_forms/manage_building_view');
sc_require('views/info_views/built_form/urban_built_forms/manage_building_type_view');
sc_require('views/info_views/built_form/urban_built_forms/manage_placetype_view');


Footprint.BuiltFormInfoPane = SC.PalettePane.extend({
    classNames: ['footprint-add-building-pane'],
    layout: { centerX: 0, centerY: 0, width: 1250, height: 650 },
    nowShowing:function() {
        return this.getPath('context.nowShowing') || 'Footprint.ManageBuildingView';
    }.property('context').cacheable(),

    // Tells the pane elements that a save is underway, which disables user actions
    // In the case of BuiltForm management the first view to store the recordsEditController
    // is the nowShowing view below
    isSaving: null,
    isSavingBinding: SC.Binding.oneWay('.contentView*contentView.recordsEditController.isSaving'),

    contentView: SC.ContainerView.design({
        classNames: ['footprint-add-built-form-container-view'],
        childViews: ['toggleButtonsView', 'overlayView'],

        recordType: null,
        // The recordType is stored in the contentView of this view (the nowShowing view)
        recordTypeBinding: SC.Binding.oneWay('*contentView.recordType'),
        // Likewise for the current selectedItem
        selectedItemBinding: SC.Binding.oneWay('*contentView.selectedItem'),

        nowShowingBinding: SC.Binding.oneWay('.parentView.nowShowing'),
        overlayView: Footprint.SaveOverlayView.extend({
            isSaving: NO,
            isSavingBinding: SC.Binding.oneWay('.pane.isSaving'),
            isVisibleBinding: SC.Binding.oneWay('.isSaving')
        }),

        toggleButtonsView: SC.SegmentedView.extend({
            layout: {top: 5, centerY:0, height:22},
            crudType: 'view',
            selectSegmentWhenTriggeringAction: YES,
            itemTitleKey: 'title',
            itemActionKey: 'action',
            itemValueKey: 'title',
            items: [
                {title: 'Building',  action: 'doManageBuildings', recordType:Footprint.Building},
                {title: 'Building Type', action: 'doManageBuildingTypes', recordType:Footprint.BuildingType},
                {title: 'Placetype', action: 'doManagePlacetypes', recordType:Footprint.UrbanPlacetype},
                // todo move these to a parallel container view
                {title: 'Crop',  action: 'doManageCrops', recordType:Footprint.Crop},
                {title: 'Crop Type', action: 'doManageCropTypes', recordType:Footprint.CropType},
                {title: 'Landscape Type', action: 'doManageLandscapeTypes', recordType:Footprint.LandscapeType}
            ],
            value: null,
            valueObserver: function() {
                var recordType = Footprint.builtFormEditRecordTypeController.get('content');
                // Updates value so the right tab is highlighted. Clicking the tabs will do this automatically,
                // this is for launching the pane from elsewhere
                if (recordType) {
                    var matchingItem = this.get('items').filter(function(item) {
                        return item.recordType==recordType
                    })[0];
                    if (matchingItem)
                        this.setIfChanged('value', matchingItem.title);
                }
            }.observes('Footprint.builtFormEditRecordTypeController.content')
        })
    })
})



