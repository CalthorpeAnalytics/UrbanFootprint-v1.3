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


var pane, view;

/**
 * Tests the entire MainPane
 */
module("Footprint.MainPane", {
    setup: function() {
        pane = viewSetup({
            contentSetup: function() {
                // Rather than explicity controller bindings like we usually do for view tests, just start the statechart and skip the login state
                Footprint.statechart.initStatechart();
                bypassLoginState();
            },
            mainPane: Footprint.MainPane
        });
        view = pane.childViews[0];
    },

    teardown: viewTeardown()
});

test("Tests that policy set tree was created correctly", function() {

    stop(20000); // delay main thread to allow break points to take
    // Make sure the controller has content
    setTimeout(function() {
//        start()
    }, 1000);
});
