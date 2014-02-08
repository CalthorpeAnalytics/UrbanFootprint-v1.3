/**
 *
 * Created by calthorpe on 12/27/13.
 */

Footprint.PresentationMedium = Footprint.Record.extend({
    isPolymorphic: YES,
    deleted: SC.Record.attr(Boolean),
    presentation: SC.Record.toOne("Footprint.Presentation", {
        isMaster: NO
    }),
    tags: SC.Record.toMany("Footprint.Tag", {
        nested: YES
    }),
    medium: SC.Record.toOne("Footprint.Medium", {
        nested: YES
    }),
    // Layers and Results are the primary users of DbEntityInterests. Hence they nest them and can edit them.
    db_entity_interest: SC.Record.toOne("Footprint.DbEntityInterest", {
        nested: YES
    }),
    // This is what is actually owned by the PresentationMedium
    // DbEntityInterest is a property of presentation.config_entity but needs to be modeled
    // here so that it can be created and saved beforehand when new presentation_media are created
    db_entity_key: SC.Record.attr(String),
    medium_context: SC.Record.attr(Object),
    configuration: SC.Record.attr(Object),
    rendered_medium: SC.Record.attr(Object),

    /***
     * The resource name is formed from the db_entity_key by dasherizing and titlizing
     * This works as a setter to by slugifying
     */
    name: function(key, value) {
        // Getter
        if (value === undefined) {
            var name = this.getPath('db_entity_interest.db_entity.name');
            return name;
        }
        // Setter
        else {
            // Protect us from bad state errors (hopefully).
            if (this.get('status') & SC.Record.READY) {
                var db_entity_key = (value || '').dasherize().replace(/-/g, '_');
                var db_entity = this.getPath('db_entity_interest.db_entity');
                // This will trigger a change on the DbEntity.key if it's new
                db_entity.setIfChanged('name', value);
                // Only update the key if the record is new
                if (this.get('status') === SC.Record.READY_NEW)
                    this.setIfChanged('db_entity_key', db_entity_key);
            }
        }
    }.property('status', 'db_entity_key').cacheable(),

    visible: SC.Record.attr(Boolean, {defaultValue: YES}),
    solo: SC.Record.attr(Boolean, {defaultValue: NO}),
    applicationVisible: null,
    visibleObserver: function() {
        this.setIfChanged('applicationVisible', this.get('visible'))
    }.observes('.visible'),

    visibility: function (propKey, value) {
        if (value === undefined) {
            return this.get('solo') ? Footprint.SOLO : (this.get('applicationVisible') ? Footprint.VISIBLE : Footprint.HIDDEN);
        }
        else {
            if ([Footprint.VISIBLE, Footprint.HIDDEN].contains(value)) {
                // Only change the value of the visible property if VISIBLE or HIDDEN are chosen
                // This allows us to maintain the visible property value while the item is soloing
                // TODO We don't update the actual visible property because we don't want to dirty the record
                this.set('applicationVisible', value == Footprint.VISIBLE);
            }
            this.set('solo', value == Footprint.SOLO);
        }
    }.property('applicationVisible', 'solo').cacheable(),

    sortPriority: function () {
        return this.getPath('configuration.sort_priority') || 100;
    }.property('configuration'),

    _copyProperties: function () {
        return ['presentation'];
    },
    _cloneProperties: function () {
        // medium is nested so needs clone but saves with the main record
        // TODO medium is done on the server for now
        return ['db_entity_interest']; //['medium'];
    },
    _saveBeforeProperties: function () {
        return [];
    },
    _customCloneProperties: function () {
        return {
            /***
             * When cloning a db_entity seek out the cloned config_entity of the cloned presentationMedium
             * @param clonedPresentationMedium
             * @param db_entity
             * @returns {*}
             */
            //   'db_entity': function(clonedPresentationMedium, clonedPresentation, db_entity) {
            //       return clonedPresentation.get('config_entity').db_entity_by_key(this.get('db_entity_key'));
            //   }
        };
    },

    _mapAttributes: {
        name: function (record, name, random) {
            return '%@_%@'.fmt(name, random)
        }
    },
    _initialAttributes: {
        name: function (record, random) {
            return 'New %@'.fmt(random);
        }
    },

    // Setup for brand new instances
    // sourceRecord is the architype in the case of new instance
    // we have to have a presentation and medium structure based on a peer record
    _createSetup: function(sourceRecord) {
        // Create the DbEntityInterest first
        // We need to do this before sc_super since setting name of the Layer sets that of the DbEntityInterest.DbEntity
        this.set('db_entity_interest', this.get('store').createRecord(Footprint.DbEntityInterest, {}, Footprint.Record.generateId()));
        this.get('db_entity_interest')._createSetup(sourceRecord.get('db_entity_interest'));
        sc_super()

        this.set('presentation', sourceRecord.get('presentation'));

        // This will be replaced by the server, but is required, so copy and null out
        // TODO cloneRecord should support a param to do a structural clone without copying primitive values
        this.set('medium', sourceRecord.get('medium').cloneRecord());
        this.setPath('medium.key', null);
        this.setPath('medium.name', null);
        this.setPath('medium.description', null);

        // TODO these will be created by the server for now.
        // When we start doing a style editor these will need ot be exposed
        //this.set('configuration', sourceRecord.get('configuration'));
        //this.set('medium_configuration', sourceRecord.get('medium_configuration'));
        this.set('db_entity_key', 'Layer_' + SC.DateTime.create().get('milliseconds'));
    },


    _deleteSetup: function() {
        sc_super()
        // Set nested records to be deleted as well
        this.setPath('medium.deleted', YES);
        this.setPath('db_entity_interest.deleted', YES);
        this.setPath('db_entity_interest.db_entity.deleted', YES);
    },

    featureRecordType: function() {
        if (this.get('db_entity_key')) {
            // Try to get the Feature subclass of the db_entity_key or default to Feature
            return Footprint.featuresActiveController.getPath(
                'dbEntityKeyToFeatureRecordType.%@'.fmt(this.get('db_entity_key'))) ||
                Footprint.Feature;
        }
    }.property('db_entity_key').cacheable(),

    undoManager: null,
    solo:null
});
