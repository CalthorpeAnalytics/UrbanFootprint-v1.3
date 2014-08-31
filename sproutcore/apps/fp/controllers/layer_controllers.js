/* 
 * UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
 * 
 * Copyright (C) 2012 Calthorpe Associates
 * 
 * This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
 * 
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * 
 * Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
 */

sc_require('controllers/controllers');
sc_require('controllers/selection_controllers');
sc_require('controllers/sets_controllers');
sc_require('models/presentation_models');
sc_require('models/layer_models');
sc_require('controllers/controller_mixins');
sc_require('controllers/scenarios/scenario_controllers');
sc_require('controllers/presentation_controllers');

Footprint.layerTagsController = Footprint.ArrayController.create(Footprint.ArrayContentSupport);

Footprint.layerLibrariesController = Footprint.PresentationsController.create({
    contentBinding:SC.Binding.oneWay('Footprint.scenarioActiveController*presentations.layers')
});

Footprint.layerLibraryActiveController = Footprint.PresentationController.create({
    presentationsBinding:SC.Binding.oneWay('Footprint.layerLibrariesController.content'),
    key: 'layer_library__default',
    keysBinding:SC.Binding.oneWay('.layers').transform(function(value) {
        if (value && value.get('status') & SC.Record.READY)
            return value.mapProperty('db_entity_interest').mapProperty('db_entity').mapProperty('key');
    })
});

/****
 * The flat version of the active layers. This controller sends the events layersDidChange
 * and layerDidChange when the whole set or active layer is updated
 * @type {RecordControllerChangeSupport}
 */
Footprint.layersController = Footprint.ArrayController.create(Footprint.RecordControllerChangeSupport, {
    contentBinding: SC.Binding.oneWay('Footprint.layerLibraryActiveController.layers'),
    selectionBinding: SC.Binding.oneWay('Footprint.layerCategoriesTreeController.selection'),

    selectedItemDidChangeEvent:'layerDidChange',
    contentDidChangeEvent:'layersDidChange'
});

/***
 * Nested store version of the Layers for editing. The selection is bound oneWay to the main controller, so that
 * when the main controller selection changes, this one updates its corresponding record
 */
Footprint.layersEditController = Footprint.EditArrayController.create({
    allowsEmptySelection:YES,
    sourceController: Footprint.layersController,
    recordType: Footprint.Layer,
    parentEntityKey: 'presentation',
    parentRecordBinding: 'Footprint.layerLibraryActiveController.content',
    nestedStore: null,
});

Footprint.layerEditController = SC.ObjectController.create({
    contentBinding: SC.Binding.oneWay('Footprint.layersEditController*selection.firstObject')
});

Footprint.layerCategoriesTreeController = Footprint.TreeController.create({

    layersVisibleForegroundContent: null,
    layersVisibleForegroundContentBinding: SC.Binding.oneWay('Footprint.layersVisibleForegroundController.firstObject'),
    firstSelectableObject: function() {
        return Footprint.layersVisibleForegroundController.get('firstObject');
    }.property('layersVisibleForegroundContent'),

    content: Footprint.TreeContent.create({
        // The container object holding nodes
        nodeSetBinding: SC.Binding.oneWay('Footprint.layerLibraryActiveController.content'),
        // The nodes of the tree
        nodesBinding: SC.Binding.oneWay('Footprint.layerLibraryActiveController.layers'),
        nodeStatus: null,
        nodeStatusBinding: SC.Binding.oneWay('*nodes.status'),

        // The toOne or toMany property of the node to access the keyObject(s). Here they are Tag instances
        keyProperty:'tags',
        // The property of the keyObject to use for a name. Here it the 'tag' property of Tag
        keyNameProperty:'tag',
        // Our default tag for layers whose db_entity doesn't have any tags that match are tag se
        undefinedKeyObject:SC.Object.create({tag:'Untagged'}),
        // Options for sorting the BuiltForms
        sortProperties: ['name'],

        /**
         * The keys of the tree, currentaly all tags in the system, to which BuiltForms might associate
         * TODO these tags should be limited to those used by BuiltForms
         */
        keyObjectsBinding: 'Footprint.layerTagsController.content'
    }),

    allowsEmptySelection: NO,
    /***
     * Override the default to select the first non-background layer.
     */
    firstSelectableObject: function() {
        return this.get('nodes').filter(function(layer) {
            return layer.get('applicationVisible') && layer.get('status') & SC.Record.READY &&
                layer.get('isForegroundLayer');
        })[0] || this.getPath('nodes.firstObject');
    }.property(),

    nodesStatus: null,
    nodesStatusBinding: SC.Binding.oneWay('*nodes.status'),
    contentDidChange: function() {
        // Clear the selection when the nodes change. firstSelectableObject will set it to something after.
        if (this.didChangeFor('layerCategoriesTreeControllerContent', 'nodes', 'nodesStatus')) {
            this.deselectObjects(this.getPath('selection'));
        }
    }.observes('.nodes', '.nodesStatus'),

    /***
     *  Initialize the selection when there is no selection yet but everything is ready
     */
    initialialSelectionObserver: function() {
        if (!this.getPath('selection.length') && Footprint.layerLibraryActiveController.getPath('layers.status') & SC.Record.READY && this.get('nodes')) {
            // Find the first visible layer
            this.selectObject(this.get('nodes').filter(function(layer) {
                return layer.get('applicationVisible');
            })[0]);
        }
    }.observes('Footprint.layerLibraryActiveController*layers.status', '.nodes').cacheable()
});

/****
 * Foreground layers.
 */

Footprint.layersBackgroundController = SC.ArrayController.create({
    layers: null,
    layersBinding: SC.Binding.oneWay('F.layersController.arrangedObjects'),
    layersDidChange: function() { this.invokeOnce('doUpdateContent'); }.observes('*layers.@each.isBackgroundLayer'),
    doUpdateContent: function() { this.notifyPropertyChange('content'); },
    content: function() {
        return (this.get('layers') || SC.EMPTY_ARRAY).filterProperty('isBackgroundLayer');
    }.property().cacheable()
});
Footprint.layersForegroundController = SC.ArrayController.create({
    layers: null,
    layersBinding: SC.Binding.oneWay('F.layersController.arrangedObjects'),
    layersDidChange: function() { this.invokeOnce('doUpdateContent'); }.observes('*layers.@each.isForegroundLayer'),
    doUpdateContent: function() { this.notifyPropertyChange('content'); },
    content: function() {
        return (this.get('layers') || SC.EMPTY_ARRAY).filterProperty('isForegroundLayer');
    }.property().cacheable()
});

/****
 * Layers that have been selected to be on the map.
 */
Footprint.layersVisibleController = SC.ArrayController.create({
    // Convenience flag for the menu panel.
    layersMenuSectionIsVisible: NO,
    layers: null,
    layersBinding: SC.Binding.oneWay('F.layersController.arrangedObjects'),
    // Manually observe membership and invalidate content to work around annoyances.
    layersDidChange: function() {
        this.notifyPropertyChange('content');
    }.observes('*layers.@each.applicationVisible'),
    content: function() {
        var layers = this.get('layers');
        if (!layers) return null;
        else return layers.filterProperty('applicationVisible', YES);
    }.property().cacheable()
});

/****
 * The class for the foreground and background list controllers.
 */
Footprint.LayersVisibleListController = SC.ArrayController.extend({
    layers: null,
    layersBinding: SC.Binding.oneWay('F.layersVisibleController.content'),
    layersDidChange: function() {
        this.set('content', (this.get('layers') || SC.EMPTY_ARRAY).filter(this._matches).sortProperty('sortPriority'))
    }.observes('*layers.[]'),

    // Override this to filter layers into content.
    _matches: function(item) { return NO; },

    // This updates the content's sort property, then alerts the authorities.
    contentDidUpdate: function() {
        var content = this.get('content');
        if (!content) return;
        // Scan ourselves and update sortPriority appropriately.
        var i, len = content.get('length'),
            obj, objPriority,
            nextObj, nextPriority,
            currentPriority = 0;
        for (i = 0; i < len; i++) {
            obj = content.objectAt(i);
            objPriority = obj.get('sortPriority');
            currentPriority += 10;
            obj.setIfChanged('sortPriority', currentPriority);
        }
        this.invokeOnce('_doUpdateMap');
    }.observes('*content.[]'),
    _doUpdateMap: function() {
        F.statechart.sendAction('visibleLayersDidChange');
    }
});

/****
 * Background layers that have been made visible on the map.
 */
Footprint.layersVisibleBackgroundController = Footprint.LayersVisibleListController.create({
    _matches: function(item) {
        return item.getPath('tags.firstObject.tag') === 'background_imagery'
    }
});

/****
 * Foreground layers that have been made visible on the map.
 */
Footprint.layersVisibleForegroundController = Footprint.LayersVisibleListController.create({
    _matches: function(item) {
        return item.getPath('tags.firstObject.tag') !== 'background_imagery'
    }
});

/***
 * Binds to the currently selected PresentationMedium
 * @type {*}
 */
Footprint.layerActiveController = SC.ObjectController.create({
    contentBinding: SC.Binding.oneWay('Footprint.layerCategoriesTreeController*selection.firstObject')
});

Footprint.layerSelectionsController = SC.ArrayController.create(SC.SelectionSupport, Footprint.ArrayContentSupport, {
    // Update the layer property whenever the user layer or user statuses change
    activeLayer:null,
    activeLayerBinding:SC.Binding.oneWay('Footprint.layerActiveController.content'),
    user:null,
    // TODO firstObject simple binding doesn't work
    userBinding:SC.Binding.oneWay('Footprint.userController.firstObject'),
    contentObserver:function() {
        if (this.get('content') && this.get('status') & SC.Record.READY) {
            this.forEach(function(layerSelection) {
                if (layerSelection.get('user') === this.get('user')) {
                    this.selectObject(layerSelection);
                }
            }, this)
        }
    }.observes('.content', '.status').cacheable()
});

/***
 * Binds to the LayerSelection instance of the active Layer
 * @type {*|void}
 */
Footprint.layerSelectionActiveController = SC.ObjectController.create({
    contentBinding: SC.Binding.oneWay('Footprint.layerSelectionsController.firstObject'),
    layerId: null,
    layerIdBinding: SC.Binding.oneWay('*content.layer.id')
});

Footprint.layerSelectionEditController = SC.ObjectController.create({
    layerId: null,
    layerIdBinding: SC.Binding.oneWay('*content.layer.id')
});

/***
 * Creates an ArrayController from the DbEntityInterests of each layer and tracks overall status
 * @type {SC.ArrayStatus}
 */
Footprint.dbEntityInterestsAndLayersController = SC.ArrayController.create(SC.ArrayStatus, {
    layers: null,
    layersBinding: SC.Binding.oneWay('F.layerCategoriesTreeController.nodes'),
    layersObserver: function() {
        this.notifyPropertyChange('content');
    }.observes('*layers.@each.db_entity_interest'),
    content: function() {
        var layers = this.get('layers');
        return layers ? layers.mapProperty('db_entity_interest').compact().concat(layers.toArray()) : null;
    }.property('layers').cacheable()
});

/***
 * Offers a list of ConfigEntity scopes for a DbEntity to belong to. It is bound two-way to the DbEntity currently being edited
 * @type {Footprint.SingleSelectionSupport}
 */
Footprint.dbEntityInterestScopesController = SC.ArrayController.create(Footprint.SingleSelectionSupport, {
    allowsEmptySelection: NO,
    scenario: null,
    scenarioBinding: SC.Binding.oneWay('Footprint.scenarioActiveController.content'),
    dbEntityInterest: null,
    dbEntityInterestBinding: 'Footprint.layerEditController*db_entity_interest',
    dbEntityInterestStatus: null,
    dbEntityInterestStatusBinding: SC.Binding.oneWay('*dbEntityInterest.status'),
    // New Layers can create a DbEntityIntereset scoped to the Scenario or Project
    // This property serves as a liaison between scope and singleSelection to convert between
    // ConfigEntity and subclassed ConfigEntity, respectively
    // For non-new layers this is readonly--we use the schema to show the scope
    scopeConfigEntity: function(propKey, value) {
        if (this.getPath('dbEntityInterest.status') === SC.Record.READY_NEW) {
            if (typeof(value) !== 'undefined' && (this.getPath('dbEntityInterest.status') & SC.Record.READY)) {
                // No conversion needed here. scope can accept a subclass instance
                this.setPath('dbEntityInterest.config_entity', value);
            }
            // Return the content matching the scope's id
            return this.get('content').find(function(configEntity) {
                    return configEntity.get('id')==this.getPath('dbEntityInterest.config_entity.id')
            }, this);
        }
        else {
            // Find the ConfigEntity matching the schema
            if (this.getPath('dbEntityInterest.status') & SC.Record.READY) {
                return this.get('content').filterProperty('schema', this.getPath('dbEntityInterest.db_entity.schema'))[0];
            }
        }
    }.property('dbEntityInterest', 'dbEntityInterestStatus').cacheable(),

    singleSelectionBinding: '.scopeConfigEntity',
    // Sets up scopeConfigEntity when the DbEntityInterest becomes ready
    dbEntityInterestObserver: function() {
        if ((this.getPath('dbEntityInterest.status') & SC.Record.READY) &&
            !this.getPath('dbEntityInterest.config_entity')) {
                this.set('scopeConfigEntity', this.get('singleSelection'))
        }
    }.observes('.dbEntityInterest', '*dbEntityInterest.status'), // don't use dbEntityStatusProperty--it lags

    project: null,
    projectBinding: SC.Binding.oneWay('*scenario.project'),
    content: function() {
        return [this.get('scenario'), this.get('project')].compact();
    }.property('scenario', 'project').cacheable()
});
