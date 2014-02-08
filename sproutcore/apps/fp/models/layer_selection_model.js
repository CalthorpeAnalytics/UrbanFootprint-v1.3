/**
 * Created by calthorpe on 12/27/13.
 */

/***
 * Represents the sub selection of a Footprint.Layer (which is currently modeled as Footprint.PresentationMedium)
 * instance's Feature instances.
 *
 * @type {*}
 */
Footprint.LayerSelection = Footprint.Record.extend({

    // The unique id for the record is its combination of user id and layer id
    primaryKey: 'unique_id',

    selection_layer:SC.Record.toOne("Footprint.Layer", {
        isMaster:YES
    }),
    user:SC.Record.toOne("Footprint.User", {
        isMaster:YES
    }),
    layer:null,
    layerBinding:SC.Binding.oneWay('.selection_layer'),

    // These are generic features. We only use them in conjunction with the layer to resolve the full Feature.
    features: SC.Record.attr(Array),
    // The result fields of the query
    result_fields: SC.Record.attr(Array),
    // The pretty version of those fields to display as column titles
    // TODO how do I model these?
    //result_field_title_lookup: SC.Record.attr(Object),

    // The summary results, and array of dicts that the API converts to SC.Objects on load
    summary_results: SC.Record.attr(Array),
    // The summary fields of the summary query
    summary_fields: SC.Record.attr(Array),
    // The pretty version of those fields to display as column titles
    // TODO how do I model these?
    //summary_field_title_lookup: SC.Record.attr(Object),

    // Bounds are set to a geojson geometry to update the selection
    bounds:SC.Record.attr(Object),
    boundsAsString: function() {
        // This does lat,lon | lat,lon rounded to four digits.
        // Assumes a single polygon in multi-polygons, hence the firstObject.firstObject
        lonLats = this.getPath('bounds.coordinates.firstObject.firstObject');
        return lonLats ? lonLats.map(
            function(lonLat) {
                return lonLat.map(function(l) {return SC.Math.round(l,4)}).join(',');
            }).join('|') : null;
    }.property('bounds').cacheable(),

    // A dictionary of the raw query strings
    // This includes 'filter_string', 'aggregates_string', and 'group_by_string'
    query_strings: SC.Record.attr(Object),

    // Holds the parsed filter token tree
    filter:SC.Record.attr(Object),
    // Holds the list of join db_entity_keys
    joins:SC.Record.attr(Array),
    // Holds the list of aggregate token trees
    aggregates:SC.Record.attr(Object),
    // Holds the list of group by terms as parsed token tress
    group_bys:SC.Record.attr(Object),

    // The extent of the currently selection features
    selection_extent:SC.Record.attr(Object),

    // Defines an undo manager for the Feature records of the label. This allows a separate undoManager per layer
    featureUndoManager:null,
    // Defines an undo manager for this instance
    undoManager: null,

    destroy:function() {
        sc_super();
        if (this.get('featureUndoManager'))
            this.get('featureUndoManager').destroy();
    },

    /***
     * Restore the user generated attributes
     * @param attributes: object of raw attributes
     */
    restore: function(attributes) {
        ['query_strings', 'joins'].map(function(attr) {
            this.set(attr, attributes[attr]);
        }, this);
    }
});

Footprint.LayerSelection.mixin({
    processDataHash: function(dataHash, record) {
        // Strip out the the features. We never want to send these.
        dataHash = $.extend({}, dataHash);
        delete dataHash.features;
        delete dataHash.summary_results;
        delete dataHash.summary_fields;
        delete dataHash.summary_field_title_lookup;
        delete dataHash.query_sql;
        delete dataHash.summary_query_sql;

        dataHash.query_strings = {}
        dataHash.query_strings.filter_string = record.getPath("query_strings.filter_string");
        dataHash.query_strings.aggregates_string = record.getPath("query_strings.aggregates_string");
        dataHash.query_strings.group_by_string = record.getPath("query_strings.group_by_string");
        return dataHash;
    }
});

