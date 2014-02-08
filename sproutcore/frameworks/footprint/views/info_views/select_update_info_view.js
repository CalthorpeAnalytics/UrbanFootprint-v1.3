
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

/*
 * Base class for editing a model object which adds the ability to select the assigned object from a list
 */

sc_require('views/select_update_view');

Footprint.SelectUpdateInfoView = Footprint.InfoView.extend({

    classNames: "footprint-update-info-view".w(),
    childViews:'titleView contentView selectView'.w(),
    // Bind this to propagate items to the selectView
    items:null,
    // Bind this to propagate the objectPath to the selectView
    objectPath:null,

    selectView: Footprint.SelectUpdateView.extend({
        itemTitleKey: 'name',
        showCheckbox: YES,
        itemsBinding: SC.Binding.oneWay(parentViewPath(1, '.items')),
        // We want to trigger a cloneAndUpdate on the content whenever the selected value changes.
        // But we don't want to set the content to another instance
        targetBinding:SC.Binding.oneWay(parentViewPath(1, '.content')),
        // The relative path from the content and selected value to instance to actual copy from the value to the content
        objectPath:SC.Binding.oneWay(parentViewPath(1, 'objectPath')),
        // Bind the value to the current content. The user may change the value away from the content for copying values
        valueBinding: SC.Binding.oneWay(parentViewPath(1, '.content'))
    }),

    _toStringAttributes: function() {
        return sc_super().concat('items objectPath'.w());
    }
});
