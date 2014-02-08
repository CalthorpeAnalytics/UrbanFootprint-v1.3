
/*
* UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
* 
* Copyright (C) 2013 Calthorpe Associates
* 
* This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
* 
* This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
*  * You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
* 
* Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
*/

sc_require('models/presentation_medium_model');

// LayerLibrary is configuration of various Layers
Footprint.LayerLibrary = Footprint.Presentation.extend({
    // We currently use the results attribute instead of presentation_media.
    // In theory Sproutcore supports subclassing on nested records,
    // so we should be able to use the presentation_media attribute instead of results.
    // A Result is a subclass of PresentationMedium
    layers: SC.Record.toMany("Footprint.Layer", {
        isMaster:YES
    }),

    _copyProperties: function () {
        return sc_super().concat([]);
    },
    _cloneProperties: function () {
         return sc_super().concat(['layers']);
    }
});

Footprint.Layer = Footprint.PresentationMedium.extend({
    // Override superclass property to specify correct related model.
    presentation: SC.Record.toOne("Footprint.LayerLibrary", {
        isMaster: NO
    }),

    origin_instance: SC.Record.toOne("Footprint.Layer"),
    // A simple flag to indicate that a cloned layer's db_entity features should be created based on the
    // current layer_selection of the origin_instance
    create_from_selection: SC.Record.attr(Boolean),

    _skipProperties: function() {
        return ['origin_instance'];
    },

    _cloneSetup: function(sourceRecord) {
        this.set('origin_instance', sourceRecord);
    }
});
