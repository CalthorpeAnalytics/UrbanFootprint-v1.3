/*
 * UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
 *
 * Copyright (C) 2012 Calthorpe Associates
 *
 * This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License. *
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
 */

Footprint.ToolSelectionStandardItems = ['Navigate', 'Box', 'Polygon', 'Identify', 'Query'];
Footprint.ToolSectionView = SC.View.extend({
    classNames: "footprint-tool-section-view".w(),
    childViews: 'toolbarView navigateAndSelectButtonView featurerBarView'.w(),

    /***
     * The delegate for the active configEntity, used to override settings
     */
    configEntityDelegate: null,

    isEnabledBinding: SC.Binding.oneWay('Footprint.layerActiveController.status').matchesStatus(SC.Record.READY_CLEAN),

    /***
     * Bind this to the active layer in the layer library.
     * The active layer determines what tools are available
     */
    activeLayer: null,
    activeLayerBinding: SC.Binding.oneWay('Footprint.layerActiveController.content'),
    activeLayerStatus: null,
    activeLayerStatusBinding: SC.Binding.oneWay('Footprint.layerActiveController*content.status'),

    /***
     * Configuration of what tools should be available to each layer according to their db_entity_key
     * TODO moved to a separate configuration that has client specific stuff.
     */
    layerLookup: SC.Object.create({
        'future_scenario_feature': {
            subtitle: 'Scenario Painting',
            isEnabledItems:  Footprint.ToolSelectionStandardItems.concat(['Apply', 'Clear'])
        }
    }),

    toolbarView: Footprint.TitleView.extend({
        anchorLocation: SC.ANCHOR_TOP,
        layout: { height: 18 },
        classNames: "footprint-title-view".w(),
        labelViewLayout: {left:0, right:0},
        title:'Tools',
        contentBinding:SC.Binding.oneWay('.parentView.activeLayer')
    }),

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
        return (layerConfig ? layerConfig.isEnabledItems : Footprint.ToolSelectionStandardItems).contains(item.title) &&
            (typeof(controllerEnabled) == 'undefined' || controllerEnabled);
    },

    navigateAndSelectButtonView: SC.SegmentedView.extend({
        layout: { top: 18, height: 26 },
        selectSegmentWhenTriggeringAction: YES,
        itemActionKey: 'action',
        itemTitleKey: 'title',
        itemKeyEquivalentKey: 'keyEquivalent',
        itemValueKey: 'title',
        itemIsEnabledKey: 'isEnabled',

        rawItems: [
            // View and edit the selected item's attributes
            SC.Object.create({ title: 'Navigate', keyEquivalent: 'ctrl_n', action: 'navigate', isEnabled: YES, type: 'navigator'}),
            SC.Object.create({ title: 'Point', keyEquivalent: 'ctrl_p', action: 'paintPoint', isEnabled: NO, type: 'selector'}),
            SC.Object.create({ title: 'Box', keyEquivalent: 'ctrl_b', action: 'paintBox', isEnabled: NO, type: 'selector'}),
            SC.Object.create({ title: 'Polygon', keyEquivalent: 'ctrl_o', action: 'paintPolygon', isEnabled: NO, type: 'selector', isStatelessButton:YES}),
            SC.Object.create({ title: 'Identify', keyEquivalent: 'ctrl_i', action: 'doFeatureIdentify', isEnabled: NO, type: 'featurer', isStatelessButton:YES}),
            SC.Object.create({ title: 'Query', keyEquivalent: 'ctrl_q', action: 'doFeatureQuery', isEnabled: NO, type: 'selector', isStatelessButton:YES})
            //{ title: 'Undo', keyEquivalent: ['ctrl_u'], action:'navigateOrSelectUndo', isEnabled:NO},
            //{ title: 'Redo', keyEquivalent: ['ctrl_r'], action:'navigateOrSelectRedo', isEnabled:NO}
        ],
        activeLayer: null,
        activeLayerBinding: SC.Binding.oneWay('.parentView.activeLayer'),
        activeLayerStatus: null,
        activeLayerStatusBinding: SC.Binding.oneWay('.parentView.activeLayerStatus'),
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
                    {isEnabled: this.parentView.isItemEnabled(item)}));
            }, this);
        }.property('activeLayer', 'activeLayerStatus').cacheable(),

        // Don't allow stateless buttons to remain selected
        valueObserver: function () {
            var value = this.get('value');
            if (value) {
                var item = this.get('items').filter(function (item) {
                    return item.get('title') == value;
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
                'Footprint.toolController.featurerIsEnabled'
        ),

        value: 'Navigate'
    }),

    featurerBarView: SC.View.extend({
        layout: { top: 44 },
        childViews: 'param1View param2View toggleView applyView clearView bufferView'.w(),
        classNames: ['featurer-bar'],

        param1View: Footprint.SliderInfoView.extend({
            layout: { left: 0.02, width: 0.3, height:43, top: 5},
            classNames: ['featurer-bar-param1'],
            valueSymbol: '%',
            title: 'Dev Pct',
            minimum: 0,
            maximum: 100,
            step: 1,
            rawValue: null,
            rawValueBinding: SC.Binding.from('Footprint.paintingController.developmentPercent'),
            value: function (propKey, value) {
                if (value !== undefined) {
                    this.set('rawValue', value / 100);
                    return value;
                }
                return this.get('rawValue') * 100;
            }.property('rawValue').cacheable()
        }),
        param2View: Footprint.SliderInfoView.extend({
            layout: { left: 0.38, width: 0.3, height:43, top: 5},
            classNames: ['featurer-bar-param2'],
            valueSymbol: '%',
            title: 'Density Pct',
            minimum: 0,
            maximum: 100,
            step: 1,
            rawValue: null,
            rawValueBinding: SC.Binding.from('Footprint.paintingController.densityPercent'),
            value: function (propKey, value) {
                if (value !== undefined) {
                    this.set('rawValue', value / 100);
                    return value;
                }
                return this.get('rawValue') * 100;
            }.property('rawValue').cacheable()
        }),
        toggleView: Footprint.CheckboxInfoView.extend({
            layout: { left: 0.76, width: 0.2, height:43, top:5 },
            classNames: ['featurer-bar-toggle'],
            title: 'Full Redev.',
            valueBinding: 'Footprint.paintingController.isFullRedevelopment'
        }),
        applyView: SC.ButtonView.extend({
            layout: { left: 0.8, bottom: 0.02, right: 10, height: 24, border: 1},
            classNames: ['theme-button', 'theme-button-blue'],
            classNameBindings: ['isFullRedevelopment:is-full-redevelopment'], // adds the is-editable when isEditable is YES
            title: 'Apply',
            action: 'doPaintApply',
            activeLayer: null,
            activeLayerBinding: SC.Binding.oneWay('.parentView.parentView.activeLayer'),
            isFullRedevelopment: null,
            isFullRedevelopmentBinding: SC.Binding.oneWay('.parentView.toggleView.value'),
            isEnabled: function () {
                return this.parentView.parentView.isItemEnabled(SC.Object.create({ title: 'Apply', isEnabled: NO, type: 'featurer'}))
            }.property('activeLayer', 'toolState').cacheable(),
            toolState: null,
            toolStateBinding: SC.Binding.oneWay('Footprint.toolController.featurerIsEnabled')
        }),
        clearView: SC.ButtonView.extend({
            layout: { left: 0.1, right:.7, bottom: 0.02, height: 24, border: 1},
            classNames: ['theme-button', 'theme-button-gold'],
            title: 'Clear',
            action: 'doPaintClear',
            activeLayer: null,
            activeLayerBinding: SC.Binding.oneWay('.parentView.parentView.activeLayer'),
            isEnabled: function () {
                return this.parentView.parentView.isItemEnabled(SC.Object.create({ title: 'Clear', isEnabled: NO, type: 'featurer'}))
            }.property('activeLayer', 'toolState').cacheable(),
            toolState: null,
            toolStateBinding: SC.Binding.oneWay('Footprint.toolController.featurerIsEnabled')
        }),
        resetButtonView: SC.ButtonView.extend({
            action: 'paintReset',
            name: 'Reset'
        }),
        applyStatusView: SC.ImageView.extend({
            layout: { left: 0.8, right: 10, height: 16, width: 16},
            value: sc_static('images/loader.gif')

        }),
        bufferView: SC.SegmentedView.extend({
            layout: { bottom: 0, left:.3, height: 26, right: 0.2 },
            selectSegmentWhenTriggeringAction: NO,
            itemActionKey: 'action',
            itemTitleKey: 'title',
            itemKeyEquivalentKey: 'keyEquivalent',
            itemValueKey: 'title',
            itemIsEnabledKey: 'isEnabled',

            items: [
                // View and edit the selected item's attributes
                SC.Object.create({ title: 'Undo', keyEquivalent: 'ctrl_u', action: 'doPaintUndo', isEnabledBinding: SC.Binding.oneWay('Footprint.layerSelectionActiveController*featureUndoManager.canUndo').bool(), type: 'chronicler'}),
                SC.Object.create({ title: 'Redo', keyEquivalent: 'ctrl_r', action: 'doPaintRedo', isEnabledBinding: SC.Binding.oneWay('Footprint.layerSelectionActiveController*featureUndoManager.canRedo').bool(), type: 'chronicler'})
            ]
        })
    })
});
