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


FootprintScag.ScagExistingLandUseParcelFeature = Footprint.PrimaryParcelFeature.extend({

//    land_use: SC.Record.attr(String),
    land_use_definition: SC.Record.toOne("Footprint.ClientLandUseDefinition", {
        isMaster: YES,
        nested: YES
    }),

    land_use_description: SC.Record.attr(String),

    geography: SC.Record.toOne("Footprint.Geography", {
        isMaster: YES,
        nested: YES
    }),

    scaguid12 : SC.Record.attr(Number),
    city : SC.Record.attr(String),
    county : SC.Record.attr(String),
    apn : SC.Record.attr(String),
    acres : SC.Record.attr(Number),
    comments : SC.Record.attr(String)
});

FootprintScag.ScagExistingLandUseParcelFeature({

    /***
     * A Lookup object that maps a property name to a more friendly representation of the instance, such as
     * built_form: function(built_form) { return built_form.get('name') })
     * @returns {*}
     */
    mapProperties: function () {
        return SC.Object.create(Footprint.Feature.mapProperties(), {
            land_use_definition: function () {
                return 'land_use_definition.land_use';
            }.property()
        });
    }
});

