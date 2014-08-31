
sc_require('models/key_mixin');
sc_require('models/name_mixin');
sc_require('models/tags_mixin');
sc_require('models/deletable_mixin');

Footprint.Behavior = Footprint.Record.extend(Footprint.Key, Footprint.Name, Footprint.Tags, Footprint.Deletable, {
    /***
     * This is used by the Footprint.Key mixin to form the key corresponding to the Name
     * Behavior keys always prefix 'behavior__'
     */
    keyPrefix:'behavior__',
    parents: SC.Record.toMany('Footprint.Behavior'),
    intersection: SC.Record.toOne('Footprint.Intersection'),
    // All tags of the behavior and its parents
    computed_tags: SC.Record.toMany(Footprint.Tag, {nested:true, isMaster:YES}),
    readonly: SC.Record.attr(Boolean),
    abstract: SC.Record.attr(Boolean)
});

Footprint.Intersection = Footprint.Record.extend({
    join_type: SC.Record.attr(String),
    from_type: SC.Record.attr(String),
    to_type: SC.Record.attr(String),
    db_entity_key: SC.Record.attr(String),

    description: function() {
        return "%@ join %@".fmt(
            this.get('join_type').titleize(),
            this.get('join_type')=='geographic' ?
                'from %@ to %@'.fmt(this.get('from_type'), this.get('to_type')) :
                'from id to primary table id'
        )
    }.property('join_type', 'from_type', 'to_type', 'db_entity_key').cacheable(),

    db_entity: function() {
        if (this.get('db_entity_key')) {
            var layer = Footprint.layersController.find(function(layer) {
                return layer.getPath('db_entity_key')==this.get('db_entity_key');
            }, this);
            return layer && layer.getPath('db_entity_intereset.db_entity.name');
        }
    }.property('db_entity_key').cacheable()
});
Footprint.Intersection.mixin({
    JOIN_TYPES: ['geographic', 'attribute'],
    GEOGRAPHIC_JOINS: ['polygon', 'centroid']
});

