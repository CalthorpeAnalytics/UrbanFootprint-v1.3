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
 *
 */


/***
 * The pane used to edit the settings of a new or existing PresentationMedium and the DbEntity to which it is associated (if any). The saving order of this will have to first save a created DbEntity and then the PresentationMedium if a DbEntity is being created here
 * @type {*}
 */
Footprint.PresentationMediumRemoveView = SC.PickerPane.extend({
    classNames:'footprint-presentation-medium-remove-view'.w(),
    layout:{width:200, height:200},
    // Use Browser positioning
    useStaticLayout:YES,
    contentView: SC.View.extend({
        childViews:['nameView', 'deleteView'],
        nameView: Footprint.EditableModelStringView.extend({
            valueBinding: 'Footprint.presentationMediumEditController.dbEntity.name'
        }),
        // The query for the DbEntity if relevant (if the DbEntity represents a query or a database view)
        deleteView: Footprint.EditableModelStringView.extend({

        })
    })
});
