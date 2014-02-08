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


Footprint.scenariosController = Footprint.ArrayController.create({
    contentBinding:SC.Binding.oneWay('Footprint.projectActiveController.children'),
    selectionBinding: SC.Binding.oneWay('Footprint.scenarioCategoriesTreeController.selection'),
    selectionDidChange: function() {
        Footprint.statechart.sendAction('doViewScenario', SC.Object.create({content : this.getPath('selection.firstObject')}));
    }.observes('.selection')
});

/***
 * Represents the active Scenario. This is reset to the first item of Footprint.scenariosController whenever the latter is reset
 * @type {*}
 */
Footprint.scenarioActiveController = SC.ObjectController.create({

    contentBinding:SC.Binding.oneWay('Footprint.scenariosController*selection.firstObject'),

    // Fetches the category value of the Scenario
    category:function() {
        return $.grep(this.getPath('content.categories').toArray() || [], function(category) { return category.key=='category';})[0];
    }.property('content').cacheable()
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
        // Bind to the active project
        configEntityBinding: 'Footprint.scenariosController.project',

        nodesBinding: 'Footprint.scenariosController.content',

        // The toOne or toMany property of the node to access the keyObject(s). Here they are Category instances
        keyProperty:'categories',

        // The property of the keyObject that access its name, thus the value of each Category of categories
        keyNameProperty:'value',

        // The unique Category instances assigned to Scenarios that we limited by the special key 'category'
        // We'll only show category values of Scenarios that fall within these categories
        keyObjectsBinding: 'Footprint.scenarioCategoriesController.content'
    })
});

/***
 * A controller to edit the active Scenario
 * @type {*}
 */
Footprint.scenarioEditController = SC.ObjectController.create({
    recordType: Footprint.Scenario,

    // This is to handle the delta in categories between what the user selected and what exists for the config_entity
    category: function(propKey, value) {
        if (this.get('content')) {
            var categories = this.getPath('singleContent.categories');
            var matchingCategory = categories && $.grep(categories.toArray(), function(category) {
                return category.key=='category';
            })[0];
            if (value !== undefined) {
                if (matchingCategory)
                    categories.remove(matchingCategory);
                categories.pushObject(value);
            }
            else
                return matchingCategory;
        }
    }.property('*content.categories')
});
