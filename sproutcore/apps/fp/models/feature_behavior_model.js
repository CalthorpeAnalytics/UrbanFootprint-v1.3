
Footprint.FeatureBehavior = Footprint.Record.extend(Footprint.Tags, {

    // db_entity: SC.Record.toOne('Footprint.DbEntity', {isMaster: NO, inverse:'feature_behavior'}),
    db_entity: function() {
        return this.get('parentRecord');
    }.property('parentRecord').cacheable(),
    behavior: SC.Record.toOne('Footprint.Behavior', {isMaster: YES}),
    intersection: SC.Record.toOne('Footprint.Intersection'),
    readonly: SC.Record.attr(Boolean),

    computedBehaviorTags: null,
    computedBehaviorTagsBinding: SC.Binding.oneWay('*behavior.computed_tags'),
    computedTags: function() {
        return (this.get('tags') || []).sortProperty('tag').toArray().concat(
            (this.get('computedBehaviorTags') || []).sortProperty('tag').toArray()
        );
    }.property('tags', 'computedBehaviorTags').cacheable(),

    _copyProperties: function () {
        return ['behavior', 'intersection', 'tags'];
    }
});
