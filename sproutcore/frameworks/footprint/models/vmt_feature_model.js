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

Footprint.VmtFeature = Footprint.Feature.extend({

    acres_gross: SC.Record.attr(Number), 
    pop: SC.Record.attr(Number),
    du: SC.Record.attr(Number),
    hh: SC.Record.attr(Number),
    emp: SC.Record.attr(Number),
    final_prod_hbo: SC.Record.attr(Number),
    final_prod_hbw: SC.Record.attr(Number),
    final_prod_nhb: SC.Record.attr(Number), 
    final_attr_hbo: SC.Record.attr(Number),
    final_attr_hbw: SC.Record.attr(Number),
    final_attr_nhb: SC.Record.attr(Number),
    vmt_daily: SC.Record.attr(Number),
    vmt_daily_w_trucks: SC.Record.attr(Number), 
    vmt_daily_per_capita: SC.Record.attr(Number), 
    vmt_daily_per_hh: SC.Record.attr(Number), 
    vmt_annual: SC.Record.attr(Number),
    vmt_annual_w_trucks: SC.Record.attr(Number),  
    vmt_annual_per_capita: SC.Record.attr(Number), 
    vmt_annual_per_hh: SC.Record.attr(Number), 
    raw_trips_total: SC.Record.attr(Number),
    internal_capture_trips_total: SC.Record.attr(Number),  
    walking_trips_total: SC.Record.attr(Number),
    transit_trips_total: SC.Record.attr(Number)
});