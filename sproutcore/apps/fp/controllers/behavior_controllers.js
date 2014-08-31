

Footprint.behaviorsController = SC.ArrayController.create(Footprint.SingleSelectionSupport, {

});

/***
 * Nested store version of the Behaviors for editing the intersection of the currently edited feature_behavior.
 * Binds the singleSelection two-way to the feature_behavior.behavior
 */
Footprint.behaviorsEditController = Footprint.EditArrayController.create(Footprint.SingleSelectionSupport, {
    allowsEmptySelection:NO,
    sourceController: Footprint.behaviorsController,
    isEditable:YES,
    recordType: 'Footprint.Behavior',
    orderBy: ['key ASC'], // TODO switch to name when we get that set up
    nestedStoreBinding: SC.Binding.oneWay('Footprint.layersEditController.nestedStore'),

    dbEntity: null,
    dbEntityBinding: SC.Binding.oneWay('Footprint.layerEditController*db_entity_interest.db_entity'),
    dbEntityStatus: null,
    dbEntityStatusBinding: SC.Binding.oneWay('*dbEntity.status'),
    featureBehavior: function() {
        if ((this.getPath('dbEntity.status') & SC.Record.READY) &&
            this.getPath('dbEntity.feature_behavior.parentRecord')) // don't know why this is ever null, but it is
            return this.getPath('dbEntity.feature_behavior');
        return null;
    }.property('dbEntity', 'dbEntityStatus').cacheable(),

    // This junk is here because parentRecord (aka the DbEntity) is sometimes undefined
    parentRecord: null,
    parentRecordBinding: SC.Binding.oneWay('*featureBehavior.parentRecord'),
    parentRecordStatus: null,
    parentRecordStatusBinding: SC.Binding.oneWay('*parentRecord.status'),

    // Get/set the behavior of the featureBehavior.
    // For some reason the binding often fires when featureBehavior (a nested record) is
    // in a bad state where it has no parentRecord, which cause the write to fail
    // So we guard against that here
    behavior: function(propKey, value) {
        if (typeof(value) !== 'undefined') {
            if (this.getPath('parentRecord.status') & SC.Record.READY)
                this.setPath('featureBehavior.behavior', value);
        }
        return this.getPath('featureBehavior.behavior');
    }.property('featureBehavior', 'parentRecord').cacheable(),

    featureBehaviorObserver: function() {
        // When a dbEntity status becomes ready set the property if unset
        if ((this.getPath('dbEntity.status') & SC.Record.READY) &&
            this.getPath('featureBehavior.parentRecord') && // don't know why this is ever null, but it is
            !this.getPath('featureBehavior.behavior'))
                this.setPath('featureBehavior.behavior', this.get('singleSelection'));
    }.observes('*dbEntity.status', '.featureBehavior'),

    singleSelectionBinding: '*behavior',
    conditions: 'deleted != YES AND abstract != YES'
});

/***
 * Holds all the Footprint.Intersection records
 */
Footprint.intersectionsController = SC.ArrayController.create();

/***
 * Nested store version of the Intersections for editing the intersection of the currently edited feature_behavior.
 * Binds the singleSelection two-way to the feature_behavior.intersection.
 */
Footprint.intersectionsEditController = Footprint.EditArrayController.create(Footprint.SingleSelectionSupport, {
    allowsEmptySelection:NO,
    firstBehavior:null,

    sourceController: Footprint.intersectionsController,
    isEditable:YES,
    recordType: 'Footprint.Intersection',
    orderBy: ['description ASC'],

    nestedStoreBinding: SC.Binding.oneWay('Footprint.layersEditController.nestedStore'),

    dbEntity: null,
    dbEntityBinding: SC.Binding.oneWay('Footprint.layerEditController*db_entity_interest.db_entity'),
    dbEntityStatus: null,
    dbEntityStatusBinding: SC.Binding.oneWay('*dbEntity.status'),
    featureBehavior: function() {
        if ((this.getPath('dbEntity.status') & SC.Record.READY) &&
            this.getPath('dbEntity.feature_behavior.parentRecord')) // don't know why this is ever null, but it is
            return this.getPath('dbEntity.feature_behavior');
        return null;
    }.property('dbEntity', 'dbEntityStatus').cacheable(),

    featureBehaviorObserver: function() {
        // When a dbEntity status becomes ready set the property if unset
        if ((this.getPath('dbEntity.status') & SC.Record.READY) &&
            this.getPath('featureBehavior.parentRecord') && // don't know why this is ever null, but it is
            !this.getPath('featureBehavior.intersection'))
            return this.setPath('featureBehavior.intersection', this.get('singleSelection'));
    }.observes('*dbEntity.status', 'featureBehavior'),

    // The instance bound to the singleSelection
    singleSelectionBinding: '*featureBehavior.intersection'
});

/***
 * A simple controller that extracts the Tag instances from Footprint.behaviorsEditControllers
 * and flattens them into a list for use in selection
 */
Footprint.behaviorTagsEditController = SC.ArrayController.create({
    allowsEmptySelection: NO,
    layers: null,
    layersBinding: SC.Binding.oneWay('Footprint.layersEditController.content'),

    // Tags of the current layer--excluded from the list
    currentTags: null,
    currentTagsBinding: SC.Binding.oneWay('Footprint.layerEditController*db_entity_interest.db_entity.feature_behavior.computedTags'),
    // Get the tags of all current Layers.
    content: function() {
        return (this.get('layers') || []).map(function(layer) {
            return layer.getPath('db_entity_interest.db_entity.feature_behavior.computedBehaviorTags') || [];
        }).flatten().uniq().removeObjects(this.get('currentTags') || []);
    }.property('layers', 'currentTags').cacheable()
});
