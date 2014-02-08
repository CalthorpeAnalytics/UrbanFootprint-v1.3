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
module("Footprint.LayerLibraryView", {
    setup: function() {
        pane = viewSetup({
            contentSetup: function() {
                // Set the project so that the Scenario controllers will set an active Scenario
                Footprint.projectActiveController.set('content',
                    Footprint.store.find(SC.Query.local(Footprint.Project)).toArray()[0]
                );
            },

            views: function() {
                return [Footprint.LayerLibraryView.extend({
                    layout: { top:0, width:.30 }
                })];
            }
        });
        view = pane.childViews[0];
    },

    teardown: viewTeardown()
});

test("Tests that policy set tree was created correctly", function() {

    stop(100000000000); // delay main thread up to a second to allow any breakpoints to work
    var timeout=0;
    // Make sure the controller has content
    setTimeout(function() {

        listViewValidation(pane, {
            listController: Footprint.layersController,
            listControllerPath:'Footprint.layersController',
            contentView: view.getPath('listView.contentView'),
            contentViewPath: 'LayerLibraryView.listView.contentView',
            itemValidator: function(i, itemView, presentationMedium) {
                var nameView = itemView.nameView;
                equals(
                    presentationMedium.getPath('db_entity_interest.name'),
                    nameView.get('value'),
                    'Expecting a name for item index %@, representing instance %@'.fmt(i, presentationMedium.get('db_entity_interest').toString()));
                var name = nameView.get('value');
                var updatedName = '%@__Test'.fmt(name);
                editLabel(nameView, pane);
                equals(
                    updatedName,
                    nameView.get('value'),
                    'Expecting a view name to be updated to %@ for item index %@, representing instance %@'.fmt(updatedName, i, presentationMedium.get('db_entity_interest').toString()));
                equals(
                    updatedName,
                    nameView.$().text(),
                    'Expecting a view label text to be updated to %@ for item index %@, representing instance %@'.fmt(updatedName, i, presentationMedium.get('db_entity_interest').toString()));
            }
        });
        // Inline editing sets the positioning back to absolute
        pane.$().css('position', 'relative');
        Footprint.libraryContent.get('selectedDbEntityInterestsByKey');
        throw 'p';
        start();
    }, timeout+=8000);
});

/*
test("Tests the VisibilityPicker views", function() {
    stop(1000000); // delay main thread up to a second to allow any breakpoints to work
    var timeout=0;
    setTimeout(function() {
        // Find the first SegmentedView
        throw 'p';
        Footprint.store.find(SC.Query.local(Footprint.PresentationMedium)).mapProperty('id')
        var segmentedView = findChildViewByKind(view, SC.SegmentedView);
        equals(segmentedView.get('value'), Footprint.VISIBLE, 'Item should be visible');
        // Click the solo button to solo the item
        var soloView = $('.sc-segment-view').get(0);
        mouseClick(soloView);
        equals(segmentedView.get('value'), Footprint.SOLO, 'Item should be soloing');

        // Click the solo button again to unsolo the item
        mouseClick(soloView);
        equals(segmentedView.get('value'), Footprint.VISIBLE, 'Visible should be selected after unsoloing');

        // Click the visible button again to hide the item
        var visibleView = view.$('.sc-segment-view').get(1);
        mouseClick(visibleView);
        equals(segmentedView.get('value'), Footprint.HIDDEN, 'Item should be hidden after unvisiblizing');

        // Solo the hidden item. It should be soloing
        mouseClick(soloView);
        equals(segmentedView.get('value'), Footprint.SOLO, 'Item should be soloing after being hidden');

        // Unsolo the hidden item. It should go back to hidden
        mouseClick(soloView);
        equals(segmentedView.get('value'), Footprint.HIDDEN, 'Item should be hidden again after unsoloing');
        start();
    }, timeout+=5000);
});
*/
