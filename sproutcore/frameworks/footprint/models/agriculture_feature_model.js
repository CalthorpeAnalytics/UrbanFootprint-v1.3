/* 
 * UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
 *
 * Copyright (C) 2012 Calthorpe Associates
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

Footprint.AgricultureFeature = Footprint.Feature.extend({

    built_form: SC.Record.toOne("Footprint.BuiltForm", {
        isMaster: YES
    }),
    built_form_key: SC.Record.attr(String),
    crop_yield: SC.Record.attr(Number),
    market_value: SC.Record.attr(Number),
    production_cost: SC.Record.attr(Number),
    water_consumption: SC.Record.attr(Number),
    labor_force: SC.Record.attr(Number),
    truck_trips: SC.Record.attr(Number)
});

Footprint.AgricultureFeature.mixin({
    priorityProperties: function () {
        return ['built_form'];
    },
    excludeProperties: function () {
        return ['config_entity', 'wkb_geometry', 'geometry']
    }
});

Footprint.BaseAgricultureFeature = Footprint.AgricultureFeature.extend({
});

Footprint.FutureAgricultureFeature = Footprint.AgricultureFeature.extend({
});