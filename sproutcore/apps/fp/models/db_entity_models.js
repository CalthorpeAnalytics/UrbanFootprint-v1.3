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
sc_require('models/deletable_mixin');
sc_require('models/timestamps_mixin');

Footprint.DbEntity = Footprint.Record.extend(
    Footprint.Key,
    Footprint.Name,
    Footprint.Tags,
    Footprint.Deletable,
    Footprint.Timestamps,
{
    query: SC.Record.attr(String),
    schema: SC.Record.attr(String),
    table: SC.Record.attr(String),
    hosts: SC.Record.attr(Array),
    url: SC.Record.attr(String),
    origin_instance: SC.Record.toOne("Footprint.DbEntity"),
    feature_class_configuration: SC.Record.toOne("Footprint.FeatureClassConfiguration", {nested:YES}),
    feature_behavior: SC.Record.toOne("Footprint.FeatureBehavior", {softInverse:'db_entity', nested:YES}),

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

    _cloneProperties: function() {
        return ['feature_class_configuration', 'feature_behavior'];
    },

    _customCloneProperties:function() {
        return {'feature_class_configuration': function(clonedParentRecord, parentProperty, areNestedRecords) {
            // For feature_class_configuration, wipe out everything from the source record for now, except the abstract_class_name.
            // In the future we will pass more things through
            var clonedFeatureClassConfiguration = this.cloneRecord(clonedParentRecord, parentProperty, areNestedRecords);
            var keepAttrs = ['abstract_class_name'];
            var attributes = clonedFeatureClassConfiguration.get('attributes');
            for (var key in attributes) {
                if (!keepAttrs.contains(key))
                    delete attributes[key];
            }
            clonedFeatureClassConfiguration.writeAttribute('generated', YES);
            return clonedFeatureClassConfiguration
        }};
    },

    _nestedProperties: function() {
        return ['feature_behavior', 'feature_class_configuration'];
    },

    /***
     * Creates needed child records. For now this is just the FeatureBehavior
     * @param sourceRecord: The archetype record. Used only to pass essential info, such as the active project
     * @private
     */
    _createSetup: function(sourceRecord) {
        sc_super()
        this.set('feature_behavior', this.get('store').createRecord(Footprint.FeatureBehavior, {}, Footprint.Record.generateId()));
        this.get('feature_behavior')._createSetup(sourceRecord.get('feature_behavior'));
        // Create a simple feature_class_configuration. This is optional--the server will create it otherwise
        // At some point we'll preconfigure more in here so it will be useful
        this.set('feature_class_configuration', this.get('store').createRecord(Footprint.FeatureClassConfiguration, {generated:YES}, Footprint.Record.generateId()));
    },

    generated: null,
    generatedBinding: SC.Binding.oneWay('*feature_class_configuration.generated'),
    /***
     * Allow deletes
     * @param record
     */
    isDeletable: function() {
        // For now client-side-created layers and cloned layers are deletable. This will be overhauled
        // when we do user permissions
        return this.getPath('feature_class_configuration.generated') || this.getPath('origin_instance');
    }.property('generated', 'origin_instance').cacheable()
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

    // Use in conjunction with cloneProperties to prevent nested properties from being loaded prior to cloning (they are already loaded!)
    _nestedProperties:function() {
        return ['db_entity']
    },

    _copyProperties: function() {
        return ['config_entity'];
    },

    //_saveAfterProperties: function() {
    //    return ['db_entity.feature_behavior']
    //},

    _createSetup: function(sourceRecord) {
        sc_super();
        this.set('config_entity', sourceRecord.get('config_entity'));
        this.set('db_entity', this.get('store').createRecord(Footprint.DbEntity, {}, Footprint.Record.generateId()));
        this.get('db_entity')._createSetup(sourceRecord.get('db_entity'));
    },
    _initialAttributes: {
        interest: function (record, random) {
            // This is the only type of interest we use for now
            return 'owner';
        }
    }
});
SC.mixin(Footprint.DbEntityInterest, {
    // The user always sees these as layers for now
    friendlyName: function() {
        return 'Layers';
    }
});

