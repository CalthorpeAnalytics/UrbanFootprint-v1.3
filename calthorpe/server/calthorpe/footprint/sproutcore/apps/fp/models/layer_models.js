
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

// LayerLibrary is configuration of various Layers
Footprint.LayerLibrary = Footprint.Presentation.extend({
    childRecordNamespace: Footprint,
    // We currently use the layer attribute instead of presentation_media. In theory Sproutcore supports subclassing on nested records, so we should be able to use the presentation_media attribute instead of results, but this is more readable anyway.
    layers: SC.Record.toMany("Footprint.Layer", {
        nested:YES
    })
});

// TODO not currently used. The Library contains presentationMedium instances instead
// We'll need to use this as soon as we need to access Layer specific attributes
Footprint.Layer = Footprint.Record.extend(Footprint.PresentationMedium);

/***
 * Represents the sub selection of a Footprint.Layer (which is currently modeled as Footprint.PresentationMedium)
 * instance's Feature instances.
 *
 * @type {*}
 */
Footprint.LayerSelection = Footprint.Record.extend({

    selection_layer:SC.Record.toOne("Footprint.PresentationMedium", {
        isMaster:YES
    }),
    user:SC.Record.toOne("Footprint.User", {
        isMaster:YES
    }),
    layer:null,
    layerBinding:'.selection_layer',

    features: SC.Record.attr(Array),

    // Bounds are set to a geojson geometry to update the selection
    bounds:SC.Record.attr(Object),

    // Holds the raw query string
    query_string: SC.Record.attr(String),
    // Holds the parsed SC query tree
    query:SC.Record.attr(Object),
    joins:SC.Record.attr(Array),

    // Defines an undo manager for the Feature records of the label. This allows a separate undoManager per layer
    featureUndoManager:null,

    destroy:function() {
        sc_super();
        if (this.featureUndoManager)
            this.featureUndoManager.destroy();
    }
});

