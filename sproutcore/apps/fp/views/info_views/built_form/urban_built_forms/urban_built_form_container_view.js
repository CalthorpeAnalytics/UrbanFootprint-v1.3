/**
 * Created by calthorpe on 3/25/14.
 */
Footprint.UrbanBuiltFormContainerView = SC.ContainerView.design({
        classNames: ['footprint-add-built-form-container-view'],
        childViews: ['toggleButtonsView'], //'overlayView'],

        recordType: null,
        // The recordType is stored in the contentView of this view (the nowShowing view)
        recordTypeBinding: SC.Binding.oneWay('*contentView.recordType'),
        // Likewise for the current selectedItem
        selectedItemBinding: SC.Binding.oneWay('*contentView.selectedItem'),

        nowShowingBinding: SC.Binding.oneWay('.parentView.nowShowing'),

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
                {title: 'Placetype', action: 'doManagePlacetypes', recordType:Footprint.UrbanPlacetype}
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