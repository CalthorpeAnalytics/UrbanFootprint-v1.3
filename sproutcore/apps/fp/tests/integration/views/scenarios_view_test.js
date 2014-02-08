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

var pane = null, view = null;
module("Footprint.ScenariosView", {

    setup: function () {

        pane = viewSetup({
            contentSetup: function () {
                Footprint.projectActiveController.set('content',
                    Footprint.store.find(SC.Query.local(Footprint.Project)).toArray()[0]
                );
            },

            scenariosLoaded: function () {
                logStatus(Footprint.scenariosController, 'Footprint.scenariosController');
                if (Footprint.scenariosController.get('status') === Footprint.Record.READY_CLEAN) {
                    // Default to the first Scenario for now
                    Footprint.scenarioActiveController.set('content', Footprint.scenariosController.content.toArray()[0]);
                }
            }.observes('Footprint.scenariosController.status'),

            views: function () {
                return [Footprint.ScenarioSectionView.extend({
                    layout: { top: 0, width: .50 }
                })];
            }
        });
        view = pane.childViews[0];
    },

    teardown: viewTeardown()
});

test("Tests that scenarios tree was created correctly", function () {

    // Make sure the controller has content
    stop(20000); // delay main thread up to a second to allow breakpoints to work

    var contentViewPath = 'listView.contentView';
    var params = {
        controllers: Footprint.scenarioControllers,
        controllersPath: 'Footprint.scenarioControllers',
        contentView: view.getPath(contentViewPath),
        contentViewPath: 'Footprint.ScenariosView.' + contentViewPath,
        editbarView: view.toolbarView.editbarView
    };
    treeViewValidation(pane, params);
});