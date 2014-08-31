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

Footprint.ConfigEntitySelections = {
    selections:SC.Record.toOne('Footprint.ConfigEntitySelection', { nested:true, isMaster: YES }),

    /**
     * This only is needed for db_entity_interests right now, because they keyed
     * In cases where the user changes an item's key, where the item is potentially part of a selection dictionary, updates the specified selection dictionary to make sure that every unique key is represented and that non-existent keys are removed.
     * @param property: Access the base items with this.get(property)
     * @param keyItemPath: Default 'key'. The path to the key for each item
     * @param keyUpdate a dictionary of key changes from new to old, if available. This can reveal that 'foo' was updated to 'bar', thus allowing the selection for 'foo' to move to 'bar'
     */
    updateSelections: function(property, keyItemPath, keyUpdate) {
        // TODO Not used. Selections need to be saved at a user scope, not a ConfigEntity scope.
        // Get all items
        var self = this;
        var items = this.get(property);
        keyItemPath = keyItemPath || 'key';
        var itemsByKey = $.mapToCollectionsObject(
            items.toArray(),
            function(item) {
                return [item.getPath(keyItemPath)];
            },
            function(item) { return item;});
        var selectionObject = this.get('selections').get(property);
        // Remove selections whose key has disappeared.
        var clonedSelectionObject = $.extend({}, selectionObject);
        $.each(selectionObject, function(key, items) {
            if (!itemsByKey[key]) {
                delete selectionObject[key];
            }
        });
        // Make selection for any new keys, using keyUpdate if provided
        $.map(itemsByKey, function(items, key) {
            if (!selectionObject[key]) {
                var oldKey = keyUpdate[key];
                // Assign the object from the old key if available, otherwise assign the first item having the matching key
                selectionObject[key] = (oldKey && clonedSelectionObject[oldKey]) || itemsByKey[key][0]
            }
        })
    }
};

/***
 *
 * Represents a dictionary (object) keyed by DbEntity key and valued by DbEntityInterest. This is used to store the DbEntityInterests that are selected for each key. The custom transform defined below takes care of transforming the incoming dictionary from the datasources to a dictionary with the same keys that Footprint.DbEntityInterest records as the values
 * @type {*}
 */

Footprint.DbEntityInterestDictionary = Footprint.Record.extend({
    _internal:YES,
    /**
     * Used by the Footprint.Datasource to learn the type of the dictionary items, which are all DbEntityInterests. Normally the DataSource inquires with the RecordAttribute for the type
     * @param key
     */
    resolveAttributeType: function(key) {
       return Footprint.DbEntityInterest;
    }
});
SC.RecordAttribute.registerTransform(Footprint.DbEntityInterestDictionary, {
    /** @private - convert the object into a DbEntityInterestDictionary instance with DbEntity values */
    to: function(obj, attr, recordType, parentRecord) {
        var store = parentRecord.get('store');
        return $.mapObjectToObject(
            // Incoming json object. This is a dictionary of DbEntityInterest ids, keyed by its DbEntity key
            obj || {},
            // Map each key and id to the key and the resolved DbEntityInterest
            function(key, id) {
                return [key, store.find(Footprint.DbEntityInterest, id)];
            },
            // This is the output object, which we need to be a DbEntityInterestDictionary. This will contain an attribute for each mapped key, whose value is naturally the DbEntityInterest
            function() { return Footprint.store.createRecord(Footprint.DbEntityInterestDictionary); }
        );
    },



    /** @private - convert an object to the raw form **/
    from: function(dbEntityDictionary) {
        return $.mapObjectToObject(
            // The DbEntityInterest object created in the to function above.
            dbEntityDictionary || {},
            // Map each attribute name and DbEntityInterest value to a key-value pair where the value is simply the DbEntityInterest id
            function(key, dbEntityInterest) {
                // Filter by kind so that we don't try to map internal SC attributes
                return isSCObjectOfKind(dbEntityInterest, Footprint.DbEntityInterest) ?
                    [key, dbEntityInterest.get('id')]:
                    null;
            }
        );
    },
    /***
     * Override Footprint.Record to copy the keys without cloning the values. Make the values null and set later.
     * @param record
     */
    copyAttributes: function(record) {
        $.each(this, function(key, value) {
            record.set(key, null);
        });
        return record;
    }

    // TODO it might be possible to use this instead of updateSelections above
    //observersChildren: []
});

Footprint.ConfigEntitySelection = Footprint.ChildRecord.extend({
    _internal: YES,

    // A list of selected or default DbEntities for every unique Key
    db_entity_interests: SC.Record.toOne(Footprint.DbEntityInterestDictionary, {isMaster:YES}),

    _cloneProperties: function() { return 'db_entity_interests'.w(); },

    /***
     * Returns YES if the given DbEntity is the one selected for its key according to the ConfigEntitySelection.db_entities dictionary
     * @param dbEntity The DbEntity to test
     * @return {Boolean}
     */
    isSelectedDbEntityForKey: function(dbEntity) {
       return this.get('db_entities')[dbEntity.get('key')]==dbEntity;
    },

    sets: SC.Record.toOne('Footprint.ConfigEntitySelectionSet', { nested:true, isMaster:YES})
});

Footprint.ConfigEntitySelectionSet = Footprint.ChildRecord.extend({
    // Points to the single selected or default built_form_set
    built_form_sets: SC.Record.toOne("Footprint.BuiltFormSet", {
        isMaster:YES
    }),
    // Points to the single selected or default policy_set
    policy_sets: SC.Record.toOne("Footprint.PolicySet", {
        isMaster:YES
    })
});
