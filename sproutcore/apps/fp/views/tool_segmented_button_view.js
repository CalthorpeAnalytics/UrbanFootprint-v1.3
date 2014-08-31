/**
 * Created with PyCharm.
 * User: calthorpe
 * Date: 3/31/14
 * Time: 12:24 PM
 * To change this template use File | Settings | File Templates.
 */


Footprint.ToolSelectionStandardItems = ['zoomToProjectExtent', 'navigate', 'paintBox', 'paintPolygon', 'doFeatureIdentify', 'doFeatureQuery', 'doClearSelection'];

Footprint.ToolSegmentedButtonView = SC.SegmentedView.extend({
    classNames: ['footprint-tool-segmented-button-view', '.ace.sc-regular-size.sc-segment-view'],
    selectSegmentWhenTriggeringAction: YES,
    itemActionKey: 'action',
    itemIconKey: 'icon',
    itemTitleKey: 'title',
    itemKeyEquivalentKey: 'keyEquivalent',
    itemValueKey: 'action',
    itemIsEnabledKey: 'isEnabled',

    rawItems: null,
    activeLayer: null,
    activeLayerStatus: null,

    isEnabledBinding: SC.Binding.oneWay('.activeLayerStatus').matchesStatus(SC.Record.READY_CLEAN),
        /***
     * Configuration of what tools should be available to each layer according to their db_entity_key
     * TODO moved to a separate configuration that has client specific stuff.
     */
    layerLookup: null,
    activeLayerConfig: function () {
        if (this.get('activeLayerStatus') & SC.Record.READY)
            return this.getPath('layerLookup.%@'.fmt(this.getPath('activeLayer.db_entity_key')));
    }.property('activeLayer', 'activeLayerStatus').cacheable(),

        /**
     * Returns YES if the given item is configured for the active layer and the toolsController says its type is isEnabled
     * @param item
     * @returns {*|boolean|*}
     */
    isItemEnabled: function (item) {
        var layerConfig = this.get('activeLayerConfig');
        // Find the optional toolController boolean for this item type
        var controllerEnabled = Footprint.toolController.get('%@IsEnabled'.fmt(item.get('type')));
        // Return YES if the layerConfig (or default config) and tool enables the item
        return (layerConfig ? layerConfig.isEnabledItems : Footprint.ToolSelectionStandardItems).contains(item.action) &&
            (typeof(controllerEnabled) == 'undefined' || controllerEnabled);
    },
    /**
     * The items that may or may not be isEnabled, based on the current activeLayer
     * This fires whenever the active layer or its status changes, and depends on the configuration of the layer
     * type ('selector', 'featurer', etc) and on any specific configuration for that layer.
     */
    items: function () {
        return this.get('rawItems').map(function (item) {
            return SC.Object.create($.extend({},
                item,
                // merge a dict that enables it if it's configured for the active layer, otherwise disables
                {isEnabled: this.isItemEnabled(item)}));
        }, this);
    }.property('activeLayer', 'activeLayerStatus').cacheable(),

    // Don't allow stateless buttons to remain selected
    valueObserver: function () {
        var value = this.get('value');
        if (value) {
            var item = this.get('items').filter(function (item) {
                return item.get('action') == value;
            })[0];
            if (item.get('isStatelessButton'))
                // Set it back. This will refire the observer once
                this.set('value', this._statefulValue);
            else
                // Update it
                this._statefulValue = value;
        }
    }.observes('.value'),

    _statefulValue: null,

    // Trigger a changes to items whenever a relevant toolController boolean changes
    toolControllerObserver: function () {
        this.propertyDidChange('items');
    }.observes(
            'Footprint.toolController.navigatorIsEnabled',
            'Footprint.toolController.selectorIsEnabled',
            'Footprint.toolController.featurerIsEnabled',
            'Footprint.toolController.deselectorIsEnabled'
    ),
    value: 'navigate'
})