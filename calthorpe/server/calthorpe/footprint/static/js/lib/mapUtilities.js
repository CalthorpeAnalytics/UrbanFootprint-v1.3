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

/* Utility functions for working with openlayers */

/*
    Format the given latlon to a string
 */
function formatLonlats(lonLat) {
    var lat = lonLat.lat;
    var long = lonLat.lon;
    var ns = OpenLayers.Util.getFormattedLonLat(lat);
    var ew = OpenLayers.Util.getFormattedLonLat(long, 'lon');
    return $.format("{0}, {1} ({2}, {3})",
        ns,
        ew,
        Math.round(lat * 10000) / 10000,
        Math.round(long * 10000) / 10000);
}
/**
 * Delete vectors from the given layer
 */
function removeVectors(layer) {
    layer.destroyFeatures();
}

function calculateExtent(map, scenario, projection, gridLayer) {
    // By default zoom to the extent defined for the study area.
    // If undefined, resort to the gridLayer extent
    var extent;
    if (scenario.fields.study_area.fields.lat_min != 0) {
        studyArea = scenario.fields.study_area.fields
        points = $.map(['min', 'max'], function (prefix) {
            return new OpenLayers.LonLat(
                studyArea[jQuery.format('lon_{0}', prefix)], studyArea[$.format('lat_{0}', prefix)])
        });
        extent = new OpenLayers.Bounds(points[0].lon, points[0].lat, points[1].lon, points[1].lat).
            transform(projection, map.getProjectionObject());
    }
    else {
        // For some reason,  the gridLayer won't have valid extents until we set a map center point with the proper projection. TODO: verify this still holds true.
        var point = new OpenLayers.LonLat(-157.989, 21.487);
        map.setCenter(point.transform(projection, map.getProjectionObject()), 0, {});
        extent = gridLayer.getExtent()
    }
    return extent;
}

/*
    Creates a custom navigation panel which includes a navigation control, a zoom box, and a feature layer identification control. The panel is added to the map
 */
function createFeatureInfoControl(config, map, popupInfo) {

    // This control allows selection of one or more features from the grid layer, and possibly other layers if we desire it.
    var featureInfoControl = new OpenLayers.Control.WMSGetFeatureInfo({
        // The Geoserver to query for data
        url:config.geoserver_wms,
        // The layers that may receive the click
        layers: popupInfo.featureInfoLayers,
        title: 'Identify features by clicking',
        // Only query visible layers
        queryVisible: true,
        // An XML format that the getfeatureinfo event parses automatically to JSON
        infoFormat:'application/vnd.ogc.gml'
    });
    // Respond to featureInfo clicks with a popup window and by highlighting the selected features
    featureInfoControl.events.on({
        getfeatureinfo: function(event) {
            try {
                var features = this.format.read(event.text);
                if (features && features.length > 0) {
                    // Since we construct a new popup each time, remove any existing ones.
                    // We might want to add a modifier key to allow the user to keep multiple popups open
                    $.each(map.popups, function(i,popup) {map.removePopup(popup)});
                    framedCloud = new OpenLayers.Popup.FramedCloud(
                        "Feature Info",
                        map.getLonLatFromPixel(event.xy),
                        null,
                        popupInfo.showInfo(features),
                        null,
                        true
                    );
                    // Size needs to be set explicitly to avoid an exception in the highlight layer
                    framedCloud.setSize(new OpenLayers.Size(100,100));
                    map.addPopup(framedCloud);
                }
            }
            finally {
                // Always stop waiting on an error or not
                OpenLayers.Element.removeClass(map.viewPortDiv, "olCursorWait");
            }
        }
    });
    return featureInfoControl;
}

/*
    Creates a custom navigation toolbar by overriding a class defintion. The toolbar includes a pan, box zoom, and identify tool. featureInfoControl is the preconfigured identify tool.
*/
function setCustomNavToolbar(featureInfoControl) {
    OpenLayers.Control.CustomNavToolbar = OpenLayers.Class(OpenLayers.Control.Panel, {

        /**
         * Constructor: OpenLayers.Control.NavToolbar
         * Add our two mousedefaults controls.
         *
         * Parameters:
         * options - {Object} An optional object whose properties will be used
         *     to extend the control.
         */
        initialize: function(options) {
            OpenLayers.Control.Panel.prototype.initialize.apply(this, [options]);
            this.addControls([
                //new OpenLayers.Control.Navigation(),
                new OpenLayers.Control.ZoomBox({alwaysZoom:true}),
                featureInfoControl,
                new OpenLayers.Control.Navigation()
            ]);
            this.displayClass = 'olControlNavToolbar'
        },


        /**
         * Method: draw
         * calls the default draw, and then activates mouse defaults.
         */
        draw: function() {
            var div = OpenLayers.Control.Panel.prototype.draw.apply(this, arguments);
            this.defaultControl = this.controls[0];
            return div;
        }
    });
}

function createMultipaneControlActivationHandler(map) {
    var self = this;
    return function (control) {
        //if (!control.active) { return false; }
        if (control.type == OpenLayers.Control.TYPE_BUTTON) {
            control.trigger();
            this.redraw();
            return;
        }
        if (control.type == OpenLayers.Control.TYPE_TOGGLE) {
            if (control.active) {
                control.deactivate();
            } else {
                control.activate();
            }
            this.redraw();
            return;
        }

        var panelList = map.getControlsByClass("OpenLayers.Control.Panel");
        for (var j=0, pLen=panelList.length; j<pLen; j++) {
            var currPanel = panelList[j];
            for (var i=0, len=currPanel.controls.length; i<len; i++) {
                if (currPanel.controls[i] != control) {
                    if (currPanel.controls[i].type !=
                        OpenLayers.Control.TYPE_TOGGLE) {
                        currPanel.controls[i].deactivate();
                    }
                }
            }
        }
        control.activate();
    };
};

