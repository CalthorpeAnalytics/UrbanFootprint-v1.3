
/*
 *UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
 * *Copyright (C) 2014 Calthorpe Associates *
 *This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
 *
 *This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
 *
 *You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 *Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
 */

/***
 * The default post-login state, whether for an authenticated session or an anonymous demo session
 * @type {Class}
 */
Footprint.ShowingAppState = SC.State.design({

    /***
     * loadingApp has substates for all of the panels of the application
     */
    substatesAreConcurrent: YES,

    enterState: function() {
        Footprint.mainPage.get('mainPane').append();
    },

    /***
     * Listens for socketIO messages
     */
    socketIOState: SC.State.plugin('Footprint.SocketIOState'),
    /***
     * The top bar of the application showing project info
     */
    showingProjectsState:SC.State.plugin('Footprint.ShowingProjectsState'),
    /***
     * The scenario panel in the top-left
     */
    showingScenariosState:SC.State.plugin('Footprint.ShowingScenariosState'),
    /***
     * The results panel in the top-right
     */
    showingResultsState:SC.State.plugin('Footprint.ShowingResultsState'),
    /***
     * The layers panel in the middle-left
     */
    showingLayersState:SC.State.plugin('Footprint.ShowingLayersState'),
    /***
     * The toolbar panel in the middle-left
     scenario_in*/
    showingToolsState:SC.State.plugin('Footprint.ShowingToolsState'),
    /***
     * The built forms panel in the bottom-left
     */
    showingBuiltFormsState:SC.State.plugin('Footprint.ShowingBuiltFormsState'),
    /***
     * The map panel in the bottom-center
     */
    showingMapState:SC.State.plugin('Footprint.ShowingMapState'),
    /***
     * The policies panel in the bottom-right
     scenario_in*/
    showingAnalysisModulesState:SC.State.plugin('Footprint.ShowingAnalysisModulesState'),

    showingCurrentAnalysisModuleState: SC.State.plugin('Footprint.ShowingAnalysisToolsState'),

    crudState:SC.State.plugin('Footprint.CrudState'),

    exitState: function() {
        Footprint.getPath('mainPage.mainPane').remove();
    }
});
