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

sc_require('models/config_entity_selections_mixin');
sc_require('models/geographic_bounds_mixin');
sc_require('models/name_mixin');
sc_require('models/key_mixin');
sc_require('models/categories_mixin');
sc_require('models/backup_properties_mixin');

/***
 * Creates a special equality operator $ to evaluate if two records have the same id to get around the query
 * language's uncanny inability to handle inheritance
 */
SC.Query.registerQueryExtension(
    '$', {
        reservedWord: true,
        leftType: 'PRIMITIVE',
        rightType: 'PRIMITIVE',
        evalType: 'BOOLEAN',

        /** @ignore */
        evaluate: function (r, w) {
            var left = this.leftSide.evaluate(r, w);
            var right = this.rightSide.evaluate(r, w);
            return left && right && left.get('id') == right.get('id')
        }});

Footprint.ConfigEntity = Footprint.Record.extend(
    Footprint.ConfigEntitySelections,
    Footprint.GeographicBounds,
    Footprint.Name,
    Footprint.Key,
    Footprint.Categories,
    Footprint.BackupProperties, {

    isPolymorphic: YES,
    deleted: SC.Record.attr(Boolean),
    parent_config_entity: SC.Record.toOne('Footprint.ConfigEntity', { isMaster: YES}),
    origin_config_entity: SC.Record.toOne('Footprint.ConfigEntity', { isMaster: YES}),
    media: SC.Record.toMany('Footprint.Medium', { nested: NO}),

    presentations: SC.Record.toOne("Footprint.PresentationTypes", {
        nested:YES
    }),

    policy_sets: SC.Record.toMany("Footprint.PolicySet"),

    built_form_sets: SC.Record.toMany("Footprint.BuiltFormSet"),

    // The API returns the DbEntities within DbEntityInterests
    db_entity_interests : SC.Record.toMany("Footprint.DbEntityInterest"),

    /***
     * Maps the db_entity_interests to retrieve the underlying db_entities
     */
    db_entities: function() {
        return this.get('db_entity_interests').mapProperty('db_entity');
    }.property('db_entity_interests').cacheable(),

    db_entity_by_key: function(key) {
        return this.get('db_entities').grep(function(db_entity) {
            return db_entity.get('key') == key;
        })[0];
    },

    // When cloning, reference these properties--don't clone them
    _copyProperties: function () {
        return ['parent_config_entity'];
    },
    // When cloning, clone these properties, creating new records for each
    _cloneProperties: function () {
        // This is done on the server for now
        return [];
    },
    _skipProperties: function() {
        // Skip most everything from now and let the server handle it
        return 'policy_sets built_form_sets categories db_entity_interests presentations selections scope schema'.w();
    },

    // Distinguish the key and name in the cloned item
    _mapAttributes: {
        key: function (record, key, random) {
            // Take the last segment to keep the key size down. The limit is the database schema
            return 'new_%@_%@'.fmt(key.split('_').slice(-1)[0], random).slice(0,50);
        },
        name: function (record, name, random) {
            return 'New %@ %@'.fmt(name, random);
        }
    },

    // Even a newly created ConfigEntity needs a parent
    _createSetup: function(sourceRecord) {
        sc_super()
        this.set('parent_config_entity', sourceRecord.get('parent_config_entity'));
    },
    // Set the origin config_entity
    _cloneSetup: function(sourceRecord) {
        this.set('origin_config_entity', sourceRecord);
    },

    _nonTransferableProperties: function () {
        return ['origin_config_entity'];
    },

    _saveAfterProperties: function() {
        return [];
        // This is all just done on the server for simplicity for now
        //return 'db_entity_interests presentations selections'.w();
    },

    /**
     * record type of the child ConfigEntities
     */
    childRecordType: null,
    /*
     * Find the children based on childRecordType
     * The $ makes it match on id in case the class types differ
     */
    children: function () {
        return Footprint.store.find(SC.Query.local(
            SC.objectForPropertyPath(this.get('childRecordType')), {
                conditions: 'parent_config_entity $ {configEntity} AND deleted=NO',
                configEntity: this,
                orderBy: 'id'
            }
        ))
    }.property().cacheable(),

    // Defines an undo manager for the children records of this ConfigEntity. This allows CRUD operations on
    // all of its children to be buffered for undo/redo actions. Thus a user might edit one child, create
    // another, remove another, etc, and it would all be in a single undo buffer. This also allows bulk operations
    // to be in the buffer, such as changing the Category values of several children at once.
    childrenUndoManager:null,

    // Undo manager for the individual instance,
    undoManager: null,

    writeStatus: function() {
        sc_super()
    },
    statusDidChange: function() {
        if (this.get('status') === SC.Record.READY_DIRTY) {
            logWarning("Scenario %@ became DIRTY!".fmt(this));
        }
    }.observes('.status')
});

Footprint.ConfigEntity.mixin({
    // Strip out stuff that shouldn't be saved to the server
    processDataHash: function(dataHash, record) {
        dataHash = $.extend({}, dataHash);
        if (dataHash.analysis_modules)
            delete dataHash.analysis_modules;
        return dataHash;
    }
});

Footprint.GlobalConfig = Footprint.ConfigEntity.extend({
    childRecordType: 'Footprint.Region'
});

Footprint.Region = Footprint.ConfigEntity.extend({
    childRecordType: 'Footprint.Project',

    // The Region's parent_config_entity may be the GlobalConfig singleton or the another Region.
    // Use a computed relationship to determine the record type.
    // TODO this doesn't make sense
    parent_config_entity: SC.Record.toOne(function () {
        return this.readAttribute('parent_config_entity') ==
            Footprint.store.find(SC.Query.local(Footprint.GlobalConfig)).toArray()[0].get('id') ?
            Footprint.GlobalConfig : Footprint.Region;
    })
});

Footprint.Project = Footprint.ConfigEntity.extend({
    init: function() {
        sc_super();
        // Since Projects will usually make use of the childrenUndoManager, create it on init.
        if (!this.get('childrenUndoManager'))
            this.childrenUndoManager = SC.UndoManager.create();
    },

    childRecordType: 'Footprint.Scenario',
    base_year: SC.Record.attr(Number),
    // Override ConfigEntity's definition so that the API knows to look up a Region
    parent_config_entity: SC.Record.toOne('Footprint.Region', { isMaster: YES }),
    // The parent_config_entity is always a Region, so we can provide this synonym property
    region: function () {
        return this.get('parent_config_entity');
    }.property('parent_config_entity')
});
