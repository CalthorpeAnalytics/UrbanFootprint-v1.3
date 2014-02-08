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
sc_require('models/built_form_models');
sc_require('controllers/controllers');
sc_require('controllers/scenarios/scenario_controllers');
sc_require('controllers/tree_content');
sc_require('controllers/tree_controller');
sc_require('controllers/container_item_edit_controller');
sc_require('controllers/selection_controllers');

Footprint.builtFormTagsController = Footprint.ArrayController.create(Footprint.ArrayContentSupport);

Footprint.builtFormCategoriesTreeController = Footprint.TreeController.create({
    /***
     *
     * Organizes the BuiltForms by their tags.
     * @type {*|void
     */
    content: Footprint.TreeContent.create({
        // Respond to configEntity changes
        configEntityBinding: SC.Binding.oneWay('Footprint.scenarioActiveController.content'),
        // The container object holding nodes
        nodeSetBinding: SC.Binding.oneWay('Footprint.builtFormSetActiveController.content'),
        // The nodes of the tree
        nodesBinding: SC.Binding.oneWay('Footprint.builtFormSetActiveController.built_forms'),
        // The toOne or toMany property of the node to access the keyObject(s). Here they are Tag instances
        keyProperty:'tags',
        // The property of the keyObject to use for a name. Here it the 'tag' property of Tag
        keyNameProperty:'tag',
        // Options for sorting the BuiltForms
        sortProperties: ['building_attributes.combined_pop_emp_density','name'],
        // Reverse sorting for appropriate keys
        reverseSortDict: {'building_attributes.combined_pop_emp_density': YES},

        /**
         * The keys of the tree, currentaly all tags in the system, to which BuiltForms might associate
         * TODO these tags should be limited to those used by BuiltForms
        */
        keyObjectsBinding: 'Footprint.builtFormTagsController.content',

        /**
         * All media used by BuiltForms, so the user can select a Medium to go assign to the BuiltForm, or clone one.
         * TODO this doesn't make sense
         */
        media: function() {
            return  Footprint.store.find(
                SC.Query.local(
                    Footprint.Medium,
                    "key BEGINS_WITH 'built_form_'",
                    { orderBy: 'key' }
            ));
        }.property().cacheable()
    }),
    selectionDidChange: function() {
        if (this.getPath('selection.firstObject'))
            Footprint.statechart.sendAction('selectedBuiltFormDidChange', SC.Object.create({content : this.getPath('selection.firstObject')}));
    }.observes('.selection')
});

/***
 * The active builtForm, as dictated by the user's selection
 * @type {*}
 */
Footprint.builtFormActiveController = Footprint.ActiveController.create({
    listController:Footprint.builtFormCategoriesTreeController
});

Footprint.builtFormControllers = Footprint.ControllerConfiguration.create({
    editController:Footprint.builtFormEditController,
    itemsController:Footprint.builtFormCategoriesTreeController,
    recordSetController:Footprint.builtFormCategoriesTreeController
});

Footprint.flatBuiltFormsController = SC.ArrayController.create(SC.SelectionSupport, {
    allowsEmptySelection:NO
});
Footprint.flatBuiltFormActiveController = SC.ObjectController.create({
    contentBinding:SC.Binding.oneWay('Footprint.flatBuiltFormsController*selection.firstObject')
});
Footprint.builtFormMediaController = SC.ArrayController.create(SC.SelectionSupport, Footprint.ArrayContentSupport, {
    allowsEmptySelection:NO,
    contentBinding: SC.Binding.oneWay('Footprint.builtFormActiveController.media'),
    updateSelection: function() {
       this.updateSelectionAfterContentChange();
    }.observes('.firstObject')
});
