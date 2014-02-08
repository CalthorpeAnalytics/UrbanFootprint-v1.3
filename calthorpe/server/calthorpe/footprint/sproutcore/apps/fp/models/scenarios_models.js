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

sc_require('models/config_entity_models');

Footprint.Scenario = Footprint.ConfigEntity.extend({
    year: SC.Record.attr(Number),
    // Override ConfigEntity's definition so that the API knows to look up a Project
    parent_config_entity:SC.Record.toOne('Footprint.Project'),
    origin_config_entity:SC.Record.toOne('Footprint.Project'),
    // The parent_config_entity is always a Project, so we can provide this synonym property
    project:function() {
        return this.get('parent_config_entity');
    }.property('parent_config_entity'),

    // Hopefully these attributes aren't required, but the idea is that Scenarios are the leaf nodes of the ScenarioCategory tree
    treeItemIsExpanded: NO,
    treeItemChildren: function(){
        return null;
    }.property('id').cacheable(),

    _cloneProperties: function() {
        return sc_super();
    },
    /**
     * The subset of properties to copy over to new instances. All Scenarios at least need the parent_config_entity
     * @returns {*|SC.Enumerator|SC.Builder}
     * @private
     */
    _propertiesForNew: function() {
        return SC.Object.create({
            parent_config_entity: this.get('parent_config_entity'),
            });
    },

    core_analytic_result: SC.Record.toOne('Footprint.AnalyticResult', { isMaster: YES, inverse:'scenario'})

});


Footprint.DwellingUnitDatum = Footprint.Record.extend({
    dwelling_unit_type: SC.Record.attr(String),
    value: SC.Record.attr(Number)
});

Footprint.ControlTotal = Footprint.Record.extend({
    value:SC.Record.attr(Number)
});

// TODO these are just used by the API for now
Footprint.FutureScenario = Footprint.Scenario.extend();
Footprint.BaseScenario = Footprint.Scenario.extend();
