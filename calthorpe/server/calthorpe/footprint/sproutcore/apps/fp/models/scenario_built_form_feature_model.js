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

Footprint.FutureScenarioFeature = Footprint.Feature.extend({
    built_form: SC.Record.toOne("Footprint.BuiltForm", {
        isMaster: YES
    }),
    //TODO remove abbreviations!
    density_pct: SC.Record.attr(Number),
    dev_pct: SC.Record.attr(Number)
});

Footprint.AnalyticResult = Footprint.Record.extend({
    scenario: SC.Record.toOne('Footprint.Scenario', {isMaster: NO}),
    population: SC.Record.attr(Number),
    dwelling_units: SC.Record.attr(Number),
    employment: SC.Record.attr(Number),
    control_total: SC.Record.toMany('Footprint.ControlTotal', {isMaster: NO, nested: YES}),
    dwelling_unit_data: SC.Record.toMany('Footprint.DwellingUnitDatum', {isMaster: YES, nested: YES})
});

Footprint.AnalysisModule = Footprint.Record.extend({
    config_entity: SC.Record.toOne('Footprint.ConfigEntity', {isMaster: YES}),
    celery_task: SC.Record.attr(Object),
    previous_celery_task: SC.Record.attr(Object),
    start: SC.Record.attr(Boolean)
});

Footprint.Core = Footprint.AnalysisModule.extend({

});
