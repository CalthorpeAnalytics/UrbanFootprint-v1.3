
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

 sc_require('resources/jqueryExtensions');

 // This must mirror the presentation ids in presentation fixtures. Redefined here to avoid circular references
 function presentationIds() {
     return {maps:[1],results:[2]};
 }
 // Clones the given associated id for the given configEntityId.
 // The given associated id will be a static id defined in the fixtures, like the presentation fixtures or db_entity_interest fixtures
 // Its assumed these are already multipled by 10 or something relative to the base configEntity. So when we pass in the cloned configEntityId here
 // we get a unique id
 function cloneAssociatedIdForClonedConfigEntity(associatedId, clonedConfigEntityId) {
     return associatedId + clonedConfigEntityId*100;
 }
 function clonePresentationIdsForClonedConfigEntity(configEntityId) {
     return $.mapObjectToObject(
         presentationIds(),
         function(key, presentationIds) {
            return [key, jQuery.map(presentationIds, function(presentationId) {
                return cloneAssociatedIdForClonedConfigEntity(presentationId, configEntityId);
            })];
         });
 }

Footprint.FIXTURES_MULTIPLIER = 4;
Footprint.FIXTURES_ID_MULTIPLIER = 10;
function multiplyScenarioId(baseId, index) {
    return baseId*Footprint.FIXTURES_ID_MULTIPLIER + index;
}
function generatedSortedLettersFromProjectName(scenario) {
    return generateSortedLetters(
        $.grep(Footprint.Project.FIXTURES, function(p) {
            return p.id==scenario.parent_config_entity})[0].name
    )
}
function generateSortedLetters(name) {
    return name.toUpperCase().slice(0,Footprint.FIXTURES_MULTIPLIER).split('').sort();
}

 function multiplyScenarios(scenarios) {
     return $.map(scenarios, function(scenario) {
         return jQuery.map(
             generatedSortedLettersFromProjectName(scenario),
             function(name, i) {
                 var new_scenario = jQuery.extend({}, scenario);
                 new_scenario.id = multiplyScenarioId(new_scenario.id, i);
                 //todo temp field
                 new_scenario.core_analytic_result = new_scenario.id*10 + i;
                 new_scenario.name += ' %@'.fmt(name);
                 new_scenario.key += '%@'.fmt(name);
                 new_scenario.presentations = $.mapObjectToObject(
                     scenario.presentations,
                     function(key, presentationList) {
                        return [key, $.map(
                            presentationList,
                            function(presentation) {
                                return cloneAssociatedIdForClonedConfigEntity(presentation, new_scenario.id);
                            })];
                     });
                 new_scenario.db_entity_interests = $.map(scenario.db_entity_interests, function(db_entity_interest) {
                     return cloneAssociatedIdForClonedConfigEntity(db_entity_interest, new_scenario.id);
                 });
                 return new_scenario;
             });
     })
 }

