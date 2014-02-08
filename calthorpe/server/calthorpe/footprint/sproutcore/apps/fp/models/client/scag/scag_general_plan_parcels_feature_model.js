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

Footprint.ScagGeneralPlanParcelsFeature = Footprint.Feature.extend({
    geography: SC.Record.toOne("Footprint.Geography", {
        isMaster: YES,
        nested: YES
    }),
    land_use_definition: SC.Record.toOne("Footprint.ClientLandUseDefinition", {
        isMaster: YES
    }),
    zone_code: SC.Record.attr(String),
    general_plan_code: SC.Record.attr(String),
    land_use : SC.Record.attr(Number),
    land_use_description : SC.Record.attr(String),
    land_use_type : SC.Record.attr(String),
    apn: SC.Record.attr(String),
    scag_general_plan_code: SC.Record.attr(Number),
    comments: SC.Record.attr(String)
});

// Use this name in all subclasses for the api resource name
SC.mixin(Footprint.ScagGeneralPlanParcelsFeature, {
    apiClassName: function () {
        return 'scag_general_plan_feature';
    }
});