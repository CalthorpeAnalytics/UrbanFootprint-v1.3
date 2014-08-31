/*
 * UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
 *
 * Copyright (C) 2012 Calthorpe Associates
 *
 * This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License. *
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
 */

sc_require('views/tool_segmented_button_view');


Footprint.ToolSectionView = SC.View.extend({
    classNames: "footprint-tool-section-view".w(),
    childViews: ['searchView', 'analysisProgressOverlayView', 'builtFormButtonView', 'selectStatusView', 'paintAndSelectButtonView'],
    /***
     * The delegate for the active configEntity, used to override settings
     */
    configEntityDelegate: null,
    /***
     * Bind this to the active layer in the layer library.
     * The active layer determines what tools are available
     */

    activeLayer: null,
    activeLayerBinding: SC.Binding.oneWay('Footprint.layerActiveController.content'),
    activeLayerStatus: null,
    activeLayerStatusBinding: SC.Binding.oneWay('Footprint.layerActiveController*content.status'),

    selectStatusView: Footprint.OverlayView.extend({
        layout: {left: 0, width:25, top:1, height: 26},
        // The overlay is visible if either feature of layerSelection status is BUSY
        featuresStatus:null,
        featuresStatusBinding: SC.Binding.oneWay('Footprint.featuresActiveController.status'),
        layerSelectionStatus: null,
        layerSelectionStatusBinding: SC.Binding.oneWay('Footprint.layerSelectionEditController.status'),
        status: function() {
            return Math.max(this.get('featuresStatus'), this.get('layerSelectionStatus'));
        }.property('featuresStatus', 'layerSelectionStatus').cacheable()
    }),

        // Shows post-save progress. The other overlay view is for saving
    analysisProgressOverlayView: Footprint.ProgressOverlayForNestedStoreView.extend({
        layout: {height: 16, top: 4, right: 5, width: 274},
        nestedStoreContentBinding: SC.Binding.oneWay('Footprint.analysisModulesEditController*selection.firstObject')
    }),

    searchView: SC.TextFieldView.extend({
        classNames: 'footprint-map-search-view'.w(),
        layout: {left:28, width:200, top: 1, height:24},

        // This example adds a search box to a map, using the
        // Google Places autocomplete feature. People can enter geographical searches.
        // The search box will return a pick list containing
        // a mix of places and predicted search terms.
        // render: function(context) {
        //     var context = context.begin();
        //     context.push('<input id="target" type="text" placeholder="Search Box">');
        //     context.end();
        // },

        // update: function() {
        // },

        didCreateLayer: function() {

            // Create the search box and link it to the UI element.
            var $input = this.$input(),
                input = $input[0];

            $input.attr('placeholder', 'Search Map');

            try {
                var searchBox = new google.maps.places.SearchBox(input);
                var self = this.get('parentView');
                // Listen for the event fired when the user selects an item from the
                // pick list. Retrieve the matching places for that item.
                google.maps.event.addListener(searchBox, 'places_changed', function() {
                    var places = searchBox.getPlaces();

                    var place = places[0];
                    if (place) {
                        map = Footprint.mapController.get('content');
                        if (map)
                            map.center({lat:place.geometry.location.lat(), lon:place.geometry.location.lng()});
                    }
                });
            }
            catch(e) {
                logWarning("Google Search Box failed to load");
            }

            // Bias the SearchBox results towards places that are within the bounds of the
            // current map's viewport.
            // TODO need map integration first
            /*
            google.maps.event.addListener(map, 'bounds_changed', function() {
                var bounds = map.getBounds();
                searchBox.setBounds(bounds);
            });
            */
        }
    }),

    builtFormButtonView: SC.ButtonView.extend({
        classNames: ['theme-button', 'theme-button-gray', 'label.sc-button-label', 'theme-button-tool-section'],
        layout: {height: 21, top: 1, left:250, width: 30 },
        icon: sc_static('images/built_form.png'),
        action: 'doManageBuiltForms'
    }),

    paintAndSelectButtonView: Footprint.ToolSegmentedButtonView.extend({
        layout: {height: 26, right:300, width: 450, top: 1},
        rawItems: [
            // View and edit the selected item's attributes
            // View and edit the selected item's attributes
            SC.Object.create({ icon: sc_static('images/zoom_to_extent.png'), action: 'zoomToProjectExtent', isEnabled: YES, type: 'navigator', isStatelessButton:YES}),
            SC.Object.create({ icon: sc_static('images/pointer.png'), keyEquivalent: 'ctrl_n', action: 'navigate', isEnabled: YES, type: 'navigator'}),
            SC.Object.create({ icon: sc_static('images/painter_point.png'), keyEquivalent: 'ctrl_p', action: 'paintPoint', isEnabled: NO, type: 'selector'}),
            SC.Object.create({ icon: sc_static('images/painter_box.png'), keyEquivalent: 'ctrl_b', action: 'paintBox', isEnabled: NO, type: 'selector'}),
            SC.Object.create({ icon: sc_static('images/painter_polygon.png'), keyEquivalent: 'ctrl_o', action: 'paintPolygon', isEnabled: NO, type: 'selector'}),
            SC.Object.create({ icon: sc_static('images/identify.png'), keyEquivalent: 'ctrl_i', action: 'doFeatureIdentify', isEnabled: NO, type: 'featurer', isStatelessButton:YES}),
            SC.Object.create({ icon: sc_static('images/query.png'), keyEquivalent: 'ctrl_q', action: 'doFeatureQuery', isEnabled: NO, type: 'selector', isStatelessButton:YES}),
            SC.Object.create({ icon: sc_static('images/clear.png'), keyEquivalent: 'esc', action: 'doClearSelection', isEnabled: NO, type: 'deselector', isStatelessButton:YES})
        ],
        activeLayerBinding: SC.Binding.oneWay('.parentView.activeLayer'),
        activeLayerStatusBinding: SC.Binding.oneWay('.parentView.activeLayerStatus')
    })
});
