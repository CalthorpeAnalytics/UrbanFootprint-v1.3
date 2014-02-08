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

sc_require('models/feature_model');
sc_require('models/client/client_land_use_definition_model');

Footprint.SacogPrimaryParcelFeature = Footprint.PrimaryParcelFeature.extend({
    land_use_definition: SC.Record.toOne("Footprint.ClientLandUseDefinition", {
        isMaster: YES
    }),
    geography: SC.Record.toOne("Footprint.Geography", {
        isMaster: YES,
        nested: YES
    }),
    census_block: SC.Record.toOne("Footprint.CensusBlock", {
        isMaster: YES,
        nested: YES
    }),
    dev_pct: SC.Record.attr(Number),
    density_pct: SC.Record.attr(Number),

    acres: SC.Record.attr(Number),

    plcshpid: SC.Record.attr(Number),

    jurisdiction: SC.Record.attr(String),
    acres: SC.Record.attr(Number),

    du12: SC.Record.attr(Number),
    emp12: SC.Record.attr(Number),

    ret_rest: SC.Record.attr(Number),
    ret_ret: SC.Record.attr(Number),
    ret_svc: SC.Record.attr(Number),
    off_off: SC.Record.attr(Number),
    off_gov: SC.Record.attr(Number),
    off_svc: SC.Record.attr(Number),
    pub_gov: SC.Record.attr(Number),
    pub_edu: SC.Record.attr(Number),
    off_med: SC.Record.attr(Number),
    pub_med: SC.Record.attr(Number),
    ind: SC.Record.attr(Number),
    other: SC.Record.attr(Number)
});
