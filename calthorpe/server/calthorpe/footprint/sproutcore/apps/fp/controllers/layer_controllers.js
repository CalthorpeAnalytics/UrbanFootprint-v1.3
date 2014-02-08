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
sc_require('resources/jqueryExtensions');
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
    layers: null,
    // TODO this binding seems to get messed up and bind to this instead of the presentation_media
    layersBinding: SC.Binding.oneWay('.presentation_media'),
    key: 'layer_library__default'
});

Footprint.layerCategoriesTreeController = Footprint.TreeController.create({

    content: Footprint.TreeContent.create({
        // Respond to configEntity changes
        configEntityBinding: SC.Binding.oneWay('Footprint.scenarioActiveController.content'),
        // The container object holding nodes
        nodeSetBinding: SC.Binding.oneWay('Footprint.layerLibraryActiveController.content'),
        // The nodes of the tree
        nodesBinding: SC.Binding.oneWay('Footprint.layerLibraryActiveController.presentation_media'),
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

    contentDidChange: function() {
        if (this.get('nodes') && (this.get('status') & SC.Record.READY) &&  this.didChangeFor('layerCategoriesTreeControllerContent', 'nodes')) {
            // Tell the selection that the content has changed
            this.updateSelectionAfterContentChange();
            // Select the first visible layer or the first layer.
            // Todo layer selection should be stored per configEntity*user
            var selectLayer = this.get('nodes').filter(function(layer) {
                return layer.get('visible');
            })[0] || this.getPath('nodes.firstObject');
            this.selectObject(selectLayer);
        }
    }.observes('.nodes'),

    layerDidChange: function() {
        if (this.getPath('selection.firstObject'))
            Footprint.statechart.sendAction('doViewLayer', SC.Object.create({content : this.getPath('selection.firstObject')}));
    }.observes('.selection', '.selection[]')
});

/***
 * Binds to the currently selected PresentationMedium
 * @type {*}
 */
Footprint.layerActiveController = SC.ObjectController.create({
    contentBinding: SC.Binding.oneWay('Footprint.layerCategoriesTreeController*selection.firstObject')
});

Footprint.layerEditController = SC.ObjectController.create({
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
    layerIdBinding: SC.Binding.oneWay('*content.layer.id'),
    layerSelectionDidChange: function() {
        if (this.get('layerId') && this.didChangeFor('layerCategoriesTreeControllerContent', 'layerId')) // Since layerSelection instances share ids
            Footprint.statechart.sendAction('doUseLayerSelection', this);
    }.observes('.layerId')
});
