/*
* UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
* 
* Copyright (C) 2013 Calthorpe Associates
* 
* This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
* 
* This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
* 
* You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
* 
* Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
*/

// FeatureControllers are always in the scope of the active ConfigEntity. They don't load all feature instances of a class but simply pull down those that make up a selection. Therefore the Datasource always expects an id list in the query to limit them

sc_require('controllers/layer_controllers');
sc_require('controllers/property_controllers');

/***
 * Controls the active features of the configEntity that are selected based on the LayerSelection
 * @type {*|void}
 */
Footprint.featuresActiveController = Footprint.ArrayController.create({

    /***
     * Delegate SC.Observable to extend dbEntityKeyToFeatureRecordType lookup
    */
    configEntityDelegateBinding: SC.Binding.oneWay('Footprint.scenarioActiveController.configEntityDelegate'),

    // Temporary hack to alert listeners when the content is updated by an edit session
    updateDate: null,

    layer:null,
    layerBinding:SC.Binding.oneWay('Footprint.layerSelectionActiveController.selection_layer'),
    layerStatus:null,
    layerStatusBinding:SC.Binding.oneWay('*layer.status'),

    recordType: function() {
        return this.get('layer') && (this.get('layerStatus') & SC.Record.READY) && this.getPath('layer.featureRecordType');
    }.property('layer', 'layerStatus').cacheable(),

    /***
     * Lookup the of Footprint.Feature subclass by db_entity_key
    */
    dbEntityKeyToFeatureRecordType: function () {
        return this.getPath('configEntityDelegate.dbEntityKeyToFeatureRecordType') || {};
    }.property('configEntityDelegate').cacheable(),

    calculateBounds: function() {
        this.mapProperty('wkb_geometry', function(geometry) {
            // TODO
        });
    }.property('features').cacheable()
});
Footprint.featuresEditController = Footprint.ArrayController.create(Footprint.EditControllerSupport, {
    allowsEmptySelection:YES,
    sourceController: Footprint.featuresActiveController,
    isEditable:YES
});

/***
 * Stores the properties of the active feature class
 */
Footprint.featuresActivePropertiesController = Footprint.PropertiesController.create({
    allowsMultipleSelection:NO,
    recordTypeBinding: SC.Binding.oneWay('Footprint.featuresActiveController.recordType')
});

Footprint.joinLayersController = SC.ArrayController.create(SC.SelectionSupport, {
    allowsMultipleSelection:NO,
    layerLibrary:null,
    layerLibraryBinding: SC.Binding.oneWay('Footprint.layerLibraryActiveController.content'),
    contentBinding: SC.Binding.oneWay('Footprint.mapLayerGroupsController.foregroundLayers'),
    sortProperties: ['name'],

    /*
     * When the selection is updated, update the active layerSelection
     */
    selectionObserver: function() {
        if (this.getPath('selection.length') && this.didChangeFor('selectionObserver', 'selection')) {
            // This soils the record. Don't do so until an actual selection is made
            var db_entity_keys = this.getPath('selection').mapProperty('db_entity_key').filter(function(db_entity_key) {
                return db_entity_key != 'None';
            });
            Footprint.layerSelectionEditController.set('joins', db_entity_keys);
        }
    }.observes('.selection'),

    /*
     * When the layer_selection updates, change the selection
     */
    layerSelectionObserver: function() {
        if (this.get('content') && Footprint.layerSelectionEditController.get('status') & SC.Record.READY) {
            var joins = Footprint.layerSelectionEditController.getPath('joins');
            var layers = this.get('content').filter(function(layer) {
                return (joins || []).contains(layer.get('db_entity_key'));
            });
            if (!SC.Set.create(layers).isEqual(SC.Set.create(this.get('selection'))))
                this.selectObjects(layers);
            this.updateSelectionAfterContentChange();
        }
    }.observes('.content',
            'Footprint.layerSelectionEditController.status',
            'Footprint.layerSelectionEditController.content',
            'Footprint.layerSelectionEditController.joins'
    ).cacheable()
});

Footprint.availableFieldsController = Footprint.PropertiesController.create({
    allowsMultipleSelection:NO,
    layer:null,
    layerBinding: SC.Binding.oneWay('Footprint.layerActiveController.content'),
    joinLayer:null,
    joinLayerBinding: SC.Binding.oneWay('Footprint.joinLayersController*selection.firstObject'),
    fields: function() {
        var dbEntityKey = this.getPath('layer.db_entity_key');
        var joinDbEntityKey = this.getPath('joinLayer.db_entity_key');
        return (joinDbEntityKey ?
                this.getPath('joinLayer.db_entity_interest.feature_fields').map(function(field) {
                    return '%@.%@'.fmt(joinDbEntityKey, field);
                }) : []
            ).concat(
            dbEntityKey ?
                this.getPath('layer.db_entity_interest.feature_fields').map(function(field) {
                        return '%@.%@'.fmt(dbEntityKey, field);
                }) : []
            );
    }.property('layer', 'joinLayer').cacheable()
});

/***
 * Stores features summary info. There is one instance per group-by combination
 */
Footprint.featureSummariesActiveController = Footprint.ArrayController.create({
    contentBinding: SC.Binding.oneWay('Footprint.layerSelectionActiveController.summary_results')
});
