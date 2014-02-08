/* 
 * UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
 *  * Copyright (C) 2012 Calthorpe Associates
 * 
 * This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
 * 
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * 
 * Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
 */
sc_require('models/config_entity_models');
sc_require('models/footprint_record');
sc_require('models/shared_key_mixin');
sc_require('models/name_mixin');
sc_require('models/db_entity_models');
sc_require('models/medium_models');

Footprint.Presentation = Footprint.Record.extend(
    Footprint.SharedKey,
    Footprint.Name, {

        isPolymorphic: YES,
        nestedRecordNamespace: Footprint,
        presentation_media: SC.Record.toMany("Footprint.PresentationMedium", {
            isMaster: YES,
            inverse: 'presentation',
            nested: YES
        }),
        config_entity: SC.Record.toOne("Footprint.ConfigEntity", {
            isMaster: NO,
            inverse: 'presentations'
        }),

        _cloneProperties: function () {
            return 'presentation_media'.w();
        },
        _mapAttributes: {
            key: function (key) {
                return key + 'New';
            },
            name: function (name) {
                return name + 'New';
            }
        }
    });

Footprint.VISIBLE = 'visible';
Footprint.HIDDEN = 'hidden';
Footprint.SOLO = 'solo';

Footprint.PresentationMedium = Footprint.Record.extend({
    isPolymorphic: YES,
    presentation: SC.Record.toOne("Footprint.Presentation", {
        isMaster: NO,
        inverse: 'presentation_media'
    }),
    tags: SC.Record.toMany("Footprint.Tag", {
        nested: YES
    }),
    medium: SC.Record.toOne("Footprint.Medium", {
        nested: YES
    }),
    // This is a read-only property generated from db_entity_key_interest on the server, since the PresentationMedium only actually references the db_entity_key. However setting this value will cause the server to update the db_entity_interest. Changing the db_entity_key will cause the server to return the DbEntityInterest of that key
    db_entity_interest: SC.Record.toOne("Footprint.DbEntityInterest", {
        nested: YES
    }),
    db_entity_key: SC.Record.attr(String),
    db_entity_property: SC.Record.attr(String),
    medium_context: SC.Record.attr(Object),
    configuration: SC.Record.attr(Object),
    rendered_medium: SC.Record.attr(Object),

    name: null,
    nameBinding: SC.Binding.oneWay('*db_entity_interest.db_entity.name'),

    visible: SC.Record.attr(Boolean, {defaultValue: YES}),
    solo: SC.Record.attr(Boolean, {defaultValue: NO}),

    visibility: function (propKey, value) {
        if (value === undefined) {
            return this.get('solo') ? Footprint.SOLO : (this.get('visible') ? Footprint.VISIBLE : Footprint.HIDDEN);
        }
        else {
            if ([Footprint.VISIBLE, Footprint.HIDDEN].contains(value)) {
                // Only change the value of the visible property if VISIBLE or HIDDEN are chosen
                // This allows us to maintain the visible property value while the item is soloing
                this.set('visible', value == Footprint.VISIBLE);
            }
            this.set('solo', value == Footprint.SOLO);
        }
    }.property('visible', 'solo').cacheable(),

    sortPriority: function () {
        return this.getPath('configuration.sort_priority') || 100;
    }.property('configuration'),

    _copyProperties: function () {
        return ''.w(); //presentation'.w();
    },
    _cloneProperties: function () {
        return 'db_entity_interest medium'.w();
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
        name: function (name) {
            return name + 'New';
        }
    },

    featureRecordType: function() {
        if (this.get('db_entity_key')) {
            var featureRecordType = Footprint.featuresActiveController.get('dbEntityKeyToFeatureRecordType')[this.get('db_entity_key')];
            if (!featureRecordType)
                throw Error("No Feature recordType for db_entity_key %@".fmt(this.get('db_entity_key')));
            return featureRecordType;
        }
    }.property('db_entity_key').cacheable()

});

Footprint.Style = Footprint.Medium.extend({
    isPolymorphic: YES
});
Footprint.Template = Footprint.Medium.extend();
Footprint.TemplateContext = Footprint.Medium.extend();
