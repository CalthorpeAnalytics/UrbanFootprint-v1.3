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

sc_require('models/shared_key_mixin');
sc_require('models/name_mixin');
sc_require('models/tags_mixin');

Footprint.DbEntity = Footprint.Record.extend(
    Footprint.Key,
    Footprint.Name,
    Footprint.Tags,
{
    deleted: SC.Record.attr(Boolean),
    query: SC.Record.attr(String),
    schema: SC.Record.attr(String),
    table: SC.Record.attr(String),
    hosts: SC.Record.attr(Array),
    url: SC.Record.attr(String),
    origin_instance: SC.Record.toOne("Footprint.DbEntity"),

    // Mapping of primitive attributes to other values
    _mapAttributes: {
        name: function(record, name, random) {
            return '%@_%@'.fmt(name, random);
        },
        key: function(record, key, random) {
            return '%@_%@'.fmt(key, random).slice(0,50);
        },
        // The server will have to assign the schema, table, and url--never copy the values from others
        schema: function(schema) {
            return null;
        },
        table: function(table) {
            return null;
        },
        url: function(url) {
            return null;
        }
    },
    _initialAttributes: {
        name: function (record, random) {
            return 'New %@'.fmt(random);
        },
        key: function (record, random) {
            return 'new_%@'.fmt(random);
        }
    },

    _skipProperties: function() {
        return ['origin_instance'];
    },

    _cloneSetup: function(sourceRecord) {
        this.set('origin_instance', sourceRecord);
    },

    _createSetup: function(sourceRecord) {
        sc_super();
    }
});

Footprint.DbEntityInterest = Footprint.Record.extend({
    deleted: SC.Record.attr(Boolean),
    interest: SC.Record.attr(String),
    db_entity: SC.Record.toOne('Footprint.DbEntity', {
        nested: YES
    }),
    config_entity: SC.Record.toOne("Footprint.ConfigEntity", {
        isMaster:YES
    }),

    _cloneProperties: function() {
        return ['db_entity'];
    },

    _copyProperties: function() {
        return ['config_entity'];
    },

    _saveBeforeProperties: function() {
    },

    _createSetup: function(sourceRecord) {
        sc_super();
        this.set('config_entity', sourceRecord.get('config_entity'));
        this.set('db_entity', this.get('store').createRecord(Footprint.DbEntity, {}, Footprint.Record.generateId()));
    },
    _initialAttributes: {
        interest: function (record, random) {
            // This is the only type of interest we use for now
            return 'owner';
        }
    },

    // DbEntityInterests need to be saved after its config_entity in the case of a new Scenario, since it is an
    // association between the ConfigEntity and a DbEntity, the latter will have been saved beforehand.
    // This tells the EditController to save them after the config_entity is saved, then save them
    // If we nested DbEntityInterests in ConfigEntity, we could simply save them at the same time as the ConfigEntity--the API supports it
    _saveAfterParent:YES
});

