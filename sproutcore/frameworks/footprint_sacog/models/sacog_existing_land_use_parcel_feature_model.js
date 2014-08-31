/*
 * UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
 *
 * Copyright (C) 2014 Calthorpe Associates
 *
 * This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
 *
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
 */

FootprintSacog.SacogExistingLandUseParcelFeature = Footprint.PrimaryParcelFeature.extend({
    land_use_definition: SC.Record.toOne("Footprint.ClientLandUseDefinition", {
        isMaster: YES,
    }),
    geography: SC.Record.toOne("Footprint.Geography", {
        isMaster: YES,
    }),
    census_blockgroup: SC.Record.attr(Number),
    census_block: SC.Record.attr(Number),
    land_use: SC.Record.attr(String),
    acres: SC.Record.attr(Number),
    du: SC.Record.attr(Number),
    jurisdiction: SC.Record.attr(String),
    notes: SC.Record.attr(String),
    emp: SC.Record.attr(Number),
    ret: SC.Record.attr(Number),
    off: SC.Record.attr(Number),
    pub: SC.Record.attr(Number),
    ind: SC.Record.attr(Number),
    other: SC.Record.attr(Number),
    assessor: SC.Record.attr(String),
    gp: SC.Record.attr(String),
    gluc: SC.Record.attr(String)

});

FootprintSacog.SacogExistingLandUseParcelFeature.mixin({

    /***
     * A Lookup object that maps a property name to a more friendly representation of the instance, such as
     * built_form: function(built_form) { return built_form.get('name') })
     * @returns {*}
     */
    mapProperties: function () {
        return SC.Object.create(Footprint.Feature.mapProperties(), {
            land_use_definition: function () {
                return 'land_use';
            }.property(),
            // Just overrides the Feature version of this function
            census_block: function () {
                return 'census_block';
            }.property()
        });
    }
});
