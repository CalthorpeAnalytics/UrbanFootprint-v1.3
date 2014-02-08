
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

/***
 * For items that are stored in set, like BuiltForms and Policies, this extension takes care of adding newly saved items to the active set via postSave
 * @type {*}
 */
Footprint.ContainerItemEditController = SC.ObjectController.extend({
    /**
     * This is the EditController of the container to which new items need to be added
     */
    containerEditController: null,
    /**
     * The property of the container that contains the items (e.g. 'built_forms' for BuiltFormSet)
     */
    containerItemProperty:null,

    /*
    * Used to make sure the conterEditController.objectController is READY_CLEAN before editing the active container
     */
    _containerObjectController:null,
    /***
     * After saving the item we need to add it to the active container if it's new.
     * TODO in the future it should be possible to add it to multiple sets based on the UI.
     * @param records: The saved records
     * @param created: YES if the item is newly created, NO if it was simply updated
     */
    onSaved: function(records, created) {
        if (created) {
            var containerEditController = this.get('containerEditController');
            this.set('_containerObjectController', containerEditController.get('objectController'));
        }
    },
    _updatingContainer: function() {
        if (this.getPath('_containerObjectContent.status')===SC.Record.READY_CLEAN) {
            this.set('_containerObjectController', null);
            var containerEditController = this.get('containerEditController');
            containerEditController.updateCurrent();
            var container = containerEditController.get('content');
            container.get('containerItemProperty').pushObject(this.get('content'));
            containerEditController.save();
        }
    }.observes('._containerObjectContent'),

    _toStringAttributes: function() {
        return 'recordType state content objectController'.w();
    }
});
