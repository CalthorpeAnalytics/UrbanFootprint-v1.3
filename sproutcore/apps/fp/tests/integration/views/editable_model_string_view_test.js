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

/***
 * Tests the Footprint.LayerLibraryView data binding, event handling, and rendering.
 */
module("Footprint.EditableModelStringView", {
    setup: function() {
        pane = viewSetup({
            contentSetup: function() {

                Footprint.scenarioActiveController.set('content',
                    Footprint.store.find(SC.Query.local(Footprint.Scenario)).toArray()[0]
                );
            },

            views: function() {
                return [Footprint.EditableModelStringView.extend({
                    layout: { top:0, width:.30, height:20},
                    valueBinding : 'Footprint.scenarioActiveController.name'
                })];
            }
        });
        view = pane.childViews[0];
        view.isEditingObserver = function() {
            pane.$().css('position', 'relative');
        }.observes('Footprint.scenarioActiveController.name');
    },

    teardown: viewTeardown()
});

test("Tests editing and binding of a Footprint.EditableModelStringView", function() {

    stop(1000000); // delay main thread up to a second to allow any breakpoints to work
    // Make sure the controller has content
    setTimeout(function() {
        var value = view.get('value');
        var updatedValue = '%@__Test'.fmt(value);
        editLabel(view);
        // The inline editor resets positioning to absolute, hiding the test results
        equals(updatedValue, view.get('value'), "Expected value %@ to become %@".fmt(value, updatedValue));
        start();

    }, 1000);
});
