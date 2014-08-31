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

sc_require('models/feature_model');

Footprint.CpadHoldingsFeature = Footprint.Feature.extend({

    agency_name: SC.Record.attr(String),
    unit_name: SC.Record.attr(String),
    access_type: SC.Record.attr(String),
    acres: SC.Record.attr(Number),
    county: SC.Record.attr(String),
    agency_level: SC.Record.attr(String),
    agency_website: SC.Record.attr(String),
    site_website: SC.Record.attr(String),
    layer: SC.Record.attr(String),
    management_agency: SC.Record.attr(String),
    label_name: SC.Record.attr(String),
    ownership_type: SC.Record.attr(String),
    site_name: SC.Record.attr(String),
    alternate_site_name: SC.Record.attr(String),
    land_water: SC.Record.attr(String),
    special_use: SC.Record.attr(String),
    hold_notes: SC.Record.attr(String),
    city: SC.Record.attr(String),

    desg_agncy: SC.Record.attr(String),
    desg_nat: SC.Record.attr(String),
    prim_purp: SC.Record.attr(String),
    apn: SC.Record.attr(String),
    holding_id: SC.Record.attr(String),
    unit_id: SC.Record.attr(String),

    superunit: SC.Record.attr(String),
    agency_id: SC.Record.attr(String),
    mng_ag_id: SC.Record.attr(String),
    al_av_parc: SC.Record.attr(String),
    date_revised: SC.Record.attr(String),
    src_align: SC.Record.attr(String),
    src_attr: SC.Record.attr(String),
    d_acq_yr: SC.Record.attr(String)
});