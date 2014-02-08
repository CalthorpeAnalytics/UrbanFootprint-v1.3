
/*
*UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
*
*Copyright (C) 2013 Calthorpe Associates
*
*This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
*
*This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
*
*You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
*
*Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
*/

sc_require('views/info_views/info_view');
sc_require('views/label_select_view');

Footprint.SelectInfoView = Footprint.InfoView.extend({
    classNames: "footprint-select-info-view".w(),
    /**
     * The content is the list of items to select from
     */
    content:null,
    selection: null,
    recordType:null,
    itemTitleKey:null,
    allowMultiple:null,
    emptyName:null,
    includeNullItem:NO,
    firstSelectedItem:null,
    // Indicates if items in the list can be selected
    isSelectable:YES,
    nullTitle: '----',
    // Max height of the panel popup
    maxHeight: 72,

    contentView: Footprint.LabelSelectView.extend({
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        selectionBinding: '.parentView.selection',
        isSelectableBinding: '.parentView.isSelectable',
        recordTypeBinding: SC.Binding.oneWay('.parentView.recordType'),
        itemTitleKeyBinding: SC.Binding.oneWay('.parentView.itemTitleKey'),
        allowMultipleBinding: SC.Binding.oneWay('.parentView.allowMultiple'),
        emptyNameBinding: SC.Binding.oneWay('.parentView.emptyName'),
        includeNullItemBinding: SC.Binding.oneWay('.parentView.includeNullItem'),
        nullTitleBinding: SC.Binding.oneWay('.parentView.nullTitle'),
        maxHeightBinding: SC.Binding.oneWay('.parentView.maxHeight')
    })
});
