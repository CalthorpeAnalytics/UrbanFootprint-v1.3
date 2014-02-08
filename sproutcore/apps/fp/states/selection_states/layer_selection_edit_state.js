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

Footprint.LayerSelectionEditState = SC.State.extend({
    initialSubstate: 'choicepointState',

    /***
     * On entry, decides which peer substate we should end up in.
     */
    choicepointState: SC.State.extend({
        enterState: function(layerContext) {
            if (!(Footprint.layerLibraryActiveController.getPath('layers.status') & SC.Record.READY) ||
                // Hack to keep background layers from trying to load layer selection
                // When we have a better definition of DbEntity functional types, we'll use that to prevent loading
                Footprint.layerActiveController.get('tags').mapProperty('tag').contains('background_imagery')) {
                Footprint.statechart.gotoState('layerNotReadyState', layerContext);
            }
            else if (!(Footprint.layerSelectionActiveController.get('status') & SC.Record.READY)) {
                // TODO temp fix for weird binding problem--this assignment isn't binding reliably
                Footprint.mapLayerGroupsController.set('activeLayer', Footprint.layerActiveController.get('content'));
                Footprint.statechart.gotoState('loadingLayerSelectionsState', layerContext);
            }
            else {
                // TODO temp fix for weird binding problem--this assignment isn't binding reliably
                Footprint.mapLayerGroupsController.set('activeLayer', Footprint.layerActiveController.get('content'));
                Footprint.statechart.gotoState('layerSelectionIsReadyState', SC.ObjectController.create({content:layerContext}));
            }            
        }
    }),

    /***
     * No layer selection because no layer! Once it loads, we will reenter choicepointState.
     */
    layerNotReadyState: SC.State.extend({
        enterState: function() {
            Footprint.toolController.set('featurerIsEnabled', NO);
            Footprint.toolController.set('selectorIsEnabled', NO);
        }
    }),

    /***
     * Layer selection is loading.
     */
    loadingLayerSelectionsState: Footprint.LoadingState.extend({
        enterState: function(context) {
            Footprint.toolController.set('featurerIsEnabled', NO);
            Footprint.toolController.set('selectorIsEnabled', NO);
            return sc_super();
        },
        recordType:Footprint.LayerSelection,
        loadingController: Footprint.layerSelectionsController,
        didLoadEvent:'layerSelectionsControllerIsReady',
        didFailEvent:'layerSelectionsControllerDidFail',

        recordArray: function(context) {
            // TODO there's no need to load the LayerSections every time we enter the state
            // They should be cached once loaded--it's unlikely they will be updated outside this app in the meantime
            //var configEntity = Footprint.scenarioActiveController.get('content');
            var layer = context.get('content');
            if (layer) {
                return Footprint.store.find(SC.Query.create({
                    recordType: this.get('recordType'),
                    location: SC.Query.REMOTE,
                    parameters: {
                        layer:layer
                    }
                }));
            }
        },

        layerSelectionsControllerIsReady: function() {
            // Start over now that we have a layerSelection
            // invokeLast to allow the active controller to bind
            this.invokeNext(function() {
                this.gotoState(this.getPath('parentState.parentState.fullPath'), Footprint.layerSelectionsController.getPath('selection.firstObject'));
            });
        }
    }),

    /***
     * Layer selection is ready!
     */
    layerSelectionIsReadyState: SC.State.plugin('Footprint.LayerSelectionIsReadyState')
});
