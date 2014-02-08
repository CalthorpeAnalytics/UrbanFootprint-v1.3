/*
 * UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
 *
 * Copyright (C) 2013 Calthorpe Associates
 *
 * This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
 *
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
 */

Footprint.Feature = Footprint.Record.extend({
    geometry: SC.Record.attr(Object),
    config_entity: SC.Record.toOne("Footprint.ConfigEntity", {
        isMaster: YES
    })
});
Footprint.Feature.mixin({
    /***
     * Properties that have priority in the info view table
     * @returns {Array}
     */
    priorityProperties: function () {
        return [];
    },
    /***
     * Properties to exclude from the info view table
     * @returns {Array}
     */
    excludeProperties: function () {
        return ['config_entity', 'geometry', 'geography'];
    },
    /***
     * A Lookup object that maps a property name to a more friendly representation of the instance, such as
     * built_form: function(built_form) { return built_form.get('name') })
     * @returns {*}
     */
    mapProperties: function () {
        return SC.Object.create({
            built_form: function () {
                return 'built_form.name';
            }.property(),
            land_use_definition: function () {
                return 'land_use_definition.land_use';
            }.property(),
            census_block: function () {
                return 'census_block.block';
            }.property()
        });
    }

});

Footprint.CensusTract = Footprint.Record.extend({
    tract: SC.Record.attr(Number)

});

Footprint.CensusBlockgroup = Footprint.Record.extend({
    blockgroup: SC.Record.attr(Number),
    census_tract: SC.Record.toOne("Footprint.CensusTract", {
        isMaster: YES,
        nested: YES
    })
});

Footprint.CensusBlock = Footprint.Record.extend({
    block: SC.Record.attr(Number),
    census_blockgroup: SC.Record.toOne("Footprint.CensusBlockgroup", {
        isMaster: YES,
        nested: YES
    })
});

Footprint.Geography = Footprint.Record.extend({
    source_id: SC.Record.attr(Number)
});
