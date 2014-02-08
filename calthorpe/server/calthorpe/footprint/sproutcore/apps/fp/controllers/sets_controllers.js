
/*
* UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
* 
* Copyright (C) 2013 Calthorpe Associates
* 
* This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
* 
* This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
* 
* You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
* 
* Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
*/

sc_require('controllers/controllers');
sc_require('binding_extensions');
/**
 * Manages a configEntity set, such as 'policy_sets' or 'built_form_sets' by storing the array of sets and setting its initial selection to the configEntity's selection
 * Mixes in SingleSelectionSupport, which updates the singleSelection property when the selection change, and updates the selection when the singleSelection property is set. When the singleSelection is update it in turn updates the configEntity's set
 *
 * This is a 2-way binding. 1) The ConfigEntity's specific selections.set property, 2) The ArrayController selection, which is simplified with the property singleSelection.
 * @type {Class}
 */
Footprint.SetsController = SC.ArrayController.extend(Footprint.SingleSelectionSupport, Footprint.ArrayContentSupport, {
    allowsEmptySelection:NO,
    listController: null,
    property:null,

    configEntity:null,
    configEntityBinding:SC.Binding.oneWay('*listController.selection.firstObject'),
    configEntityStatus:null,
    configEntityStatusBinding:SC.Binding.oneWay('*configEntity.status'),

    configEntitySet:function() {
        return this.getPath('configEntity.%@'.fmt(this.get('property')));
    }.property('configEntityStatus', 'property').cacheable(),

    contentBinding:SC.Binding.oneWay('.configEntitySet').convertToRecordArray(),

    selectionPath:function() {
        return 'configEntity.selections.sets.%@'.fmt(this.get('property'));
    }.property('configEntity', 'property').cacheable(),

    contentObserver: function() {
        if (this.getPath('configEntity.status')===SC.Record.READY_CLEAN) {
            this.updateSelectionAfterContentChange();
            this.set('singleSelection', this.get('configEntitySelection'));
        }
    }.observes('*configEntity.status').cacheable(),

    /*
     * Property to read and update the value referenced by the selectionPath
     * The selection sj
     */
    configEntitySelection: function(keyProp, value) {
        if (value !== undefined) {
            // Update the configEntity selection. Note that this will make the ConfigEntity dirty
            this.setPath(this.get('selectionPath'), value)
        }
        return this.getPath(this.get('selectionPath'));
    }.property('configEntity', 'selectionPath'),

    /*
     * When singleSelection is updated via set, we update the configEntitySelection property
     */
    singleSelectionObserver: function() {
        this.set('configEntitySelection', this.get('singleSelection'));
    }.observes('.singleSelection'),

    toString: function() {
        return this.toStringAttributes('content configEntity property selectionPath configEntitySelection'.w());
    }
});
