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

sc_require('models/footprint_record');
sc_require('models/shared_key_mixin');
sc_require('models/name_mixin');
sc_require('models/tags_mixin');

Footprint.DbEntity = Footprint.Record.extend(
    Footprint.SharedKey,
    Footprint.Name,
    Footprint.Tags,
{
    query: SC.Record.attr(String),
    schema: SC.Record.attr(String),
    table: SC.Record.attr(String),
    hosts: SC.Record.attr(Array),
    url: SC.Record.attr(String),

    // Mapping of primitive attributes to other values, (e.g. key: function(key) { return key+'new';}
    _mapAttributes: {
        name: function(name) { return name+'__new';},
        // The server will have to assign the schema to new db_entities based on the config_entity it associates with
        schema: function(schema) {
            return ''
        }
    }

});

Footprint.DbEntityInterest = Footprint.Record.extend({
    childRecordNamespace: Footprint,
    interest: SC.Record.attr(String),
    db_entity: SC.Record.toOne('Footprint.DbEntity', {
        nested: true
    }),
    config_entity: SC.Record.toOne("Footprint.ConfigEntity", {
        isMaster:YES
    }),

    _cloneProperties: function() { return 'db_entity'.w(); },
    _copyProperties: function() { return 'config_entity'.w(); },

    _saveBeforeProperties: function() { return 'db_entity'.w() },

    // DbEntityInterests need to be saved after its config_entity in the case of a new Scenario, since it is an
    // association between the ConfigEntity and a DbEntity, the latter will have been saved beforehand.
    // This tells the EditController to save them after the config_entity is saved, then save them
    // If we nested DbEntityInterests in ConfigEntity, we could simply save them at the same time as the ConfigEntity--the API supports it
    _saveAfterParent:YES
});

