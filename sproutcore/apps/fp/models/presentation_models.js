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
sc_require('models/shared_key_mixin');
sc_require('models/name_mixin');
sc_require('models/name_mixin');
sc_require('models/db_entity_models');
sc_require('models/medium_models');

Footprint.Presentation = Footprint.Record.extend(
    Footprint.Key,
    Footprint.Name,
    Footprint.Deletable, {

    isPolymorphic: YES,
    config_entity: SC.Record.toOne("Footprint.ConfigEntity", {
        isMaster: NO,
        inverse: 'presentations'
    }),

    _mapAttributes: {
        key: function (record, key) {
            return key + 'New';
        },
        name: function (record, name) {
            return name + 'New';
        }
    },
    solos:null,
    // TODO The controller's keys property is causing a recordDidChange for some reason.
    // I'm thus putting this here to prevent that. It serves no purpose here
    keys: null
});

Footprint.Style = Footprint.Medium.extend({
    isPolymorphic: YES
});
Footprint.Template = Footprint.Medium.extend();
Footprint.TemplateContext = Footprint.Medium.extend();
