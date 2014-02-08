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
        sortProperties: ['building_attribute_set.combined_pop_emp_density','name'],
        // Reverse sorting for appropriate keys
        reverseSortDict: {'building_attribute_set.combined_pop_emp_density': YES},

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
                    Footprint.Medium, {
                        conditions: "key BEGINS_WITH 'built_form_'",
                        orderBy: 'key'
                    }));
        }.property().cacheable()
    }),
    selectionDidChange: function() {
        if (this.getPath('selection.firstObject'))
            Footprint.statechart.sendAction('builtFormDidChange', SC.Object.create({content : this.getPath('selection.firstObject')}));
    }.observes('.selection')
});

/***
 * The active builtForm, as dictated by the user's selection
 * @type {*}
 */
Footprint.builtFormActiveController = Footprint.ActiveController.create({
    listController:Footprint.builtFormCategoriesTreeController
});

/***
 *  Supports reading of the FlatBuiltForm versions of BuiltForms. These contain extra attributes not currentlty stored in the builtForm
 * @type {SelectionSupport}
 */
Footprint.flatBuiltFormsController = SC.ArrayController.create(SC.SelectionSupport, {
    allowsEmptySelection:NO
});
/***
 * The flatBuildForm corresponding to the builtFormActiveController content
 */
Footprint.flatBuiltFormActiveController = SC.ObjectController.create({
    contentBinding:SC.Binding.oneWay('Footprint.flatBuiltFormsController*selection.firstObject')
});

/**
 * Provides a detailed view of the media of the active BuiltForm
 * @type {SelectionSupport}
 */
Footprint.builtFormMediaController = SC.ArrayController.create(SC.SelectionSupport, Footprint.ArrayContentSupport, {
    allowsEmptySelection:NO,
    contentBinding: SC.Binding.oneWay('Footprint.builtFormActiveController.media'),
    updateSelection: function() {
        this.updateSelectionAfterContentChange();
    }.observes('.firstObject')
});


/***===== BuiltForm CRUD controllers =====***/

/***
 * A flat list of all Building records
 * @type {SelectionSupport}
 */
Footprint.buildingsController = SC.ArrayController.create(SC.SelectionSupport, Footprint.RecordControllerChangeSupport, {
    allowsEmptySelection:YES,
    orderBy: ['name ASC'],
    contentDidChangeEvent: 'buildingControllerDidChange',
    selectedItemDidChangeEvent: 'selectedBuildingControllerDidChange',
    sourceSelection: null,
    sourceSelectionBinding: SC.Binding.oneWay('Footprint.builtFormCategoriesTreeController.selection'),
    selection: function() {
        if (!this.get("sourceSelection") || !this.get('content'))
            return;
        var builtForms = this.get('sourceSelection').filter(function(builtForm) {
            return this.get('content').contains(builtForm);
        }, this);
        var selectionSet = SC.SelectionSet.create();
        selectionSet.addObjects(builtForms);
        return selectionSet;
    }.property('sourceSelection', 'controller').cacheable()
});

/***
 * Nested store version of the buildings for editing. The selection is bound oneWay to the main controller, so that
 * when the main controller selection changes, this one updates its corresponding record
 */
Footprint.buildingsEditController = Footprint.EditArrayController.create({
    allowsEmptySelection:NO,
    sourceController: Footprint.buildingsController,
    isEditable:YES,
    recordType: Footprint.PrimaryComponent,
    orderBy: ['name ASC']
});

/***
 * A flat list of all BuildingType records
 * @type {SelectionSupport}
 */
Footprint.buildingTypesController = SC.ArrayController.create(SC.SelectionSupport, Footprint.RecordControllerChangeSupport, {
    allowsEmptySelection:YES,
    orderBy: ['name ASC'],
    contentDidChangeEvent: 'buildingTypesControllerDidChange',
    selectedItemDidChangeEvent: 'selectedBuildingTypesControllerDidChange',
    sourceSelection: null,
    sourceSelectionBinding: SC.Binding.oneWay('Footprint.builtFormCategoriesTreeController.selection'),
    selection: function() {
        if (!this.get("sourceSelection") || !this.get('content'))
            return;
        var builtForms = this.get('sourceSelection').filter(function(builtForm) {
            return this.get('content').contains(builtForm);
        }, this);
        var selectionSet = SC.SelectionSet.create();
        selectionSet.addObjects(builtForms);
        return selectionSet;
    }.property('sourceSelection', 'controller')
});

/***
 * Nested store version of the buildingTypes for editing. The selection is bound oneWay to the main controller, so that
 * when the main controller selection changes, this one updates its corresponding record
 */
Footprint.buildingTypesEditController = Footprint.EditArrayController.create({
    allowsEmptySelection:NO,
    sourceController: Footprint.buildingTypesController,
    isEditable:YES,
    recordType: Footprint.PlacetypeComponent,
    orderBy: ['name ASC']
});

/***
 * A flat list of all PlaceType records
 * @type {SelectionSupport}
 */
Footprint.placetypesController = SC.ArrayController.create(SC.SelectionSupport, Footprint.RecordControllerChangeSupport, {
    allowsEmptySelection:YES,
    orderBy: ['name ASC'],
    contentDidChangeEvent: 'placetypesControllerDidChange',
    selectedItemDidChangeEvent: 'selectedPlacetypesControllerDidChange',
    sourceSelection: null,
    sourceSelectionBinding: SC.Binding.oneWay('Footprint.builtFormCategoriesTreeController.selection'),
    selection: function() {
        if (!this.get("sourceSelection") || !this.get('content'))
            return;
        var builtForms = this.get('sourceSelection').filter(function(builtForm) {
            return this.get('content').contains(builtForm);
        }, this);
        var selectionSet = SC.SelectionSet.create();
        selectionSet.addObjects(builtForms);
        return selectionSet;
    }.property('sourceSelection', 'controller')
});

/***
 * Nested store version of the placeTypes for editing. The selection is bound oneWay to the main controller, so that
 * when the main controller selection changes, this one updates its corresponding record
 */
Footprint.placetypesEditController = Footprint.EditArrayController.create({
    allowsEmptySelection:NO,
    sourceController: Footprint.placetypesController,
    isEditable:YES,
    recordType: Footprint.Placetype,
    orderBy: ['name ASC']
});


