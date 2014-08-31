/*
 * UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
 *
 * Copyright (C) 2014 Calthorpe Associates
 *
 * This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
 *
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
*/

Footprint.AnalysisModulesPrepareState = SC.State.extend({
    initialSubstate: 'choicepointState',

    /***
     * On entry, decides which peer substate we should end up in.
     */
    choicepointState: SC.State.extend({
        enterState: function(context) {
            if (!(Footprint.analysisModulesController.get('status') & SC.Record.READY)) {
                Footprint.statechart.gotoState('loadingAnalysisModulesState');
            }
            else {
                Footprint.statechart.gotoState('analysisModulesAreReadyState', context);
            }
        }
    }),

    /***
     * No analysis_module selection because no analysis_module! Once it loads, we will reenter choicepointState.
     */
    analysisModuleNotReadyState: SC.State,

    /***
     * AnalysisModule selection is loading.
     */
    loadingAnalysisModulesState: Footprint.LoadingState.extend({
        recordType:Footprint.AnalysisModule,
        loadingController: Footprint.analysisModulesController,
        didLoadEvent:'analysisModulesControllerIsReady',
        didFailEvent:'analysisModulesControllerDidFail',

        recordArray: function(context) {
            var configEntity = Footprint.scenariosController.getPath('selection.firstObject');
            if (!configEntity)
                return;

            // Check to see if these are already loaded
            var localResults = Footprint.store.find(SC.Query.create({
                recordType: this.get('recordType'),
                location: SC.Query.LOCAL,
                conditions: 'config_entity $ {configEntity}',
                configEntity: configEntity,
                orderBy: 'id'
            }));
            if (localResults.get('length') > 0) {
                return localResults;
            }

            return Footprint.store.find(SC.Query.create({
                recordType: this.get('recordType'),
                location: SC.Query.REMOTE,
                parameters: {
                    config_entity: configEntity
                }
            }));
        },
        analysisModulesControllerIsReady: function() {
            // Start over now that we have a analysis_moduleSelection
            // invokeLast to allow the active controller to bind
            this.invokeNext(function() {
                Footprint.analysisModulesEditController.deselectObjects(
                    Footprint.analysisModulesEditController.get('selection')
                );
                Footprint.analysisModulesEditController.updateSelectionAfterContentChange();
                this.gotoState(this.getPath('parentState.parentState.fullPath'),
                               SC.ArrayController.create({content:Footprint.analysisModulesController.get('content')}));
            });
        }
    })
});
