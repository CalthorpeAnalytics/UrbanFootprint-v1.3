
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

sc_require('controllers/scenarios/scenario_controllers');
sc_require('controllers/controllers');
sc_require('controllers/selection_controllers');
sc_require('controllers/sets_controllers');

Footprint.builtFormSetsController = Footprint.SetsController.create({
    listControllerBinding: SC.Binding.oneWay('Footprint.scenariosController'),
    property:'built_form_sets'
});

/***
 * The active builtFormSet bound to that of the ConfigEntity's selected BuiltFormSet so that the user can change it.
 * Changing it causes the ConfigEntity to be updated on the server
 * @type {*}
 */
Footprint.builtFormSetActiveController = Footprint.ActiveController.create({
    listController:Footprint.builtFormSetsController,
    /***
     * Observe the active layer and change the built form set if the layer corresponds to a specific built_form_set
     */
    layerActiveControllerObserver: function() {
        if ((Footprint.layerActiveController.get('status') & SC.Record.READY) === SC.Record.READY) {
            if (!Footprint.layerActiveController.didChangeFor('showingBuiltFormPanel', 'content'))
                return this;
            var built_form_set_key = Footprint.layerActiveController.getPath('configuration.built_form_set_key');
            if (built_form_set_key) {
                Footprint.builtFormSetsController.selectObject(
                    Footprint.store.find(SC.Query.local(
                        Footprint.BuiltFormSet, {
                            conditions: 'key = {key}',
                            key: built_form_set_key
                        })).firstObject());
            }
        }
    }.observes('Footprint.layerActiveController.status')
});

