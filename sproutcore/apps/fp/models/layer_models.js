
/*
* UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
* 
* Copyright (C) 2014 Calthorpe Associates
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
        isMaster:YES,
        inverse: 'presentation'
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

    // NOTE: These properties are read-only, and permanently cached. If background-ness is ever editable,
    // or if layer tags are ever not nested, they will have to be reimplemented.
    isBackgroundLayer: function() {
        return this.get('tags').getEach('tag').contains('background_imagery');
    }.property('status').cacheable(),
    isForegroundLayer: function() {
        return !this.get('isBackgroundLayer');
    }.property('status').cacheable(),

    _skipProperties: function() {
        return ['origin_instance'];
    },

    _cloneSetup: function(sourceRecord) {
        this.set('origin_instance', sourceRecord);
    },

    /***
     * CRUDing a Layer is really about CRUDING the more fundamental DbEntityInterest
     * The DbEntityInterest is that record that actually tracks save progress.
     * We currently save the Layer as the main record with a reference to DbEntityInterest,
     * but that will need to be changed. Plus we might need to replace DbEntityInterest with DbEntity!
     * @returns {*|Array|The|Mixed|String|Array|Object}
     * @private
     */
    _recordForCrudUpdates: function() {
        return this.get('db_entity_interest')
    }
});
