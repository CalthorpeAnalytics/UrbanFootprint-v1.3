/*  * UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
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

sc_require('models/scenarios_models');
sc_require('controllers/projects_controllers');
sc_require('controllers/selection_controllers');
sc_require('controllers/controllers');
sc_require('controllers/tree_content');
sc_require('controllers/tree_controller');


/****
 * The flat version of the active scenarios. This controller sends the events scenariosDidChange
 * and scenarioDidChange when the whole set or active scenario is updated
 * @type {RecordControllerChangeSupport}
 */
Footprint.scenariosController = Footprint.ArrayController.create(Footprint.RecordControllerChangeSupport, {
    contentBinding:SC.Binding.oneWay('Footprint.projectActiveController.children'),
    selectionBinding: SC.Binding.oneWay('Footprint.scenarioCategoriesTreeController.selection'),

    selectedItemDidChangeEvent:'scenarioDidChange',
    contentDidChangeEvent:'scenariosDidChange'
});

/***
 * Represents the active Scenario. This is reset to the first item of Footprint.scenariosController whenever the latter is reset
 * @type {*}
 */
Footprint.scenarioActiveController = SC.ObjectController.create(Footprint.ConfigEntityDelegator, {

    contentBinding:SC.Binding.oneWay('Footprint.scenariosController*selection.firstObject'),
    parentConfigEntityDelegator: Footprint.projectActiveController,

    // Fetches the category value of the Scenario
    category:function() {
        return this.getPath('content.categories').filter(function(category) {
            return category.key=='category';
        })[0];
    }.property('content').cacheable()
});

/***
 * Nested store version of the Scenarios for editing. The selection is bound oneWay to the main controller, so that
 * when the main controller selection changes, this one updates its corresponding record
 */
Footprint.scenariosEditController = Footprint.EditArrayController.create({
    allowsEmptySelection:YES,
    sourceController: Footprint.scenariosController,
    isEditable:YES,
    recordType: Footprint.Scenario,
    parentEntityKey: 'parent_config_entity',
    parentRecordBinding:'Footprint.projectActiveController.content',
    nestedStore: null,
    sortProperties: ['name']
});

Footprint.scenarioCategoriesController = SC.ArrayController.create(Footprint.ArrayContentSupport);

/***
 *
 * Organizes the Scenarios by one of their Category keys. Currently this hard-coded to 'category' but it should be made a property so that the user can categorize Scenarios otherwise
 * @type {*|void
*/
Footprint.scenarioCategoriesTreeController = Footprint.TreeController.create({
    treeItemIsGrouped: YES,
    allowsMultipleSelection: NO,
    allowsEmptySelection: NO,
    content: Footprint.TreeContent.create({

        nodesBinding: 'Footprint.scenariosController.content',

        // The toOne or toMany property of the node to access the keyObject(s). Here they are Category instances
        keyProperty:'categories',

        // The property of the keyObject that access its name, thus the value of each Category of categories
        keyNameProperty:'value',
        undefinedKeyObject:SC.Object.create({key: 'category', value:'Unknown'}),

        // The unique Category instances assigned to Scenarios that we limited by the special key 'category'
        // We'll only show category values of Scenarios that fall within these categories
        keyObjectsBinding: 'Footprint.scenarioCategoriesController.content'
    })
});
