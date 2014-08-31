
/*
* UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
* 
* Copyright (C) 2014 Calthorpe Associates
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
 * A selection controller whose contents is a list of selectable values. Zero or one items in the list are selected,
 * depending on the property values of the editController.content indicated by the property at propertyKey. If all
 * of editController's content property values are identical, then that single identical item will be the selection
 * of this controller. If the controller's selection is updated to a new value or no value, all the editController's
 * content property values will be updated accordingly. If not all values are identical then there is no selected item.
 *
 */

sc_require('controllers/controllers.js');

Footprint.SyncedSelectionController = SC.ArrayController.extend(Footprint.SingleSelectionSupport, {

    /***
     * Set this to the controller whose content items are being bulk viewed or edited
     */
    editController:null,
    editControllerContent:null,
    editControllerContentBinding:SC.Binding.oneWay('.editController.content'),

    propKey:null,

    /***
     * Whenever the content changes select an item of the ArrayController if the content all have the same
     * property value
     */
    editControllerObserver: function() {
        if (this.get('editControllerContent').mapProperty(this.get('propKey')).uniq().length==1)
            this.selectObject(this.get('editControllerContent').firstObject().get(this.get('propKey')));
        else
            this.deselectObjects(this.get('selection'));
    }.observes('editControllerContent')
});

