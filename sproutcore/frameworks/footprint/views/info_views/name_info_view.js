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


sc_require('views/editable_model_string_view');
sc_require('views/info_views/info_view');
sc_require('views/info_views/info_view_configuration');

Footprint.NameInfoView = Footprint.InfoView.extend({
    classNames:'footprint-name-view'.w(),

    title:'Name',
    contentView: Footprint.EditableModelStringView.extend({
        classNames: ['footprint-editable-content-view'],
        layout: {left: .2, width: .8},
        valueBinding: parentViewPath(1, '.value'),
        isEditableBinding:SC.Binding.oneWay('.parentView.isEditable')
    })
});
