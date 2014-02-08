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
    nestedStore: null
});

Footprint.layerEditController = SC.ObjectController.create({
    contentBinding: SC.Binding.oneWay('Footprint.layersEditController*selection.firstObject')
});

Footprint.layerCategoriesTreeController = Footprint.TreeController.create({

    content: Footprint.TreeContent.create({
        // Respond to configEntity changes
        configEntityBinding: SC.Binding.oneWay('Footprint.scenarioActiveController.content'),
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

    nodesStatus: null,
    nodesStatusBinding: SC.Binding.oneWay('*nodes.status'),
    contentDidChange: function() {
        if (this.get('nodes') && (this.getPath('nodesStatus') & SC.Record.READY) &&
            this.didChangeFor('layerCategoriesTreeControllerContent', 'nodes', 'nodesStatus')) {
            // Tell the selection that the content has changed
            this.updateSelectionAfterContentChange();
            // Select the first visible layer that isn't a background layer
            var selectLayer = this.get('nodes').filter(function(layer) {
                return layer.get('applictionVisible') && layer.get('status') & SC.Record.READY &&
                    !layer.get('tags').mapProperty('tag').contains('background_imagery');
            })[0] || this.getPath('nodes.firstObject');
            this.selectObject(selectLayer);
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
    }.observes('.content', '.status').cacheable(),
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
    layerIdBinding: SC.Binding.oneWay('*content.layer.id'),
});
