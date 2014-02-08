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


FootprintScag.ScagPrimarySpzFeature = Footprint.Feature.extend({

    geography: SC.Record.toOne("Footprint.Geography", {
        isMaster: YES,
        nested: YES
    }),
    comments: SC.Record.attr(String),
    spzid: SC.Record.attr(String),
    population: SC.Record.attr(Number),
    households: SC.Record.attr(Number),
    employees: SC.Record.attr(Number)
});


// Use this name in all subclasses for the api resource name
SC.mixin(FootprintScag.ScagPrimarySpzFeature, {
    apiClassName: function () {
        return 'scag_primary_spz_feature';
    }
});
