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

sc_require('views/label_select_view');
sc_require('views/info_views/key_info_view');

/***
 * The pane used to import a PresentationMedium or at least a DbEntity (the former is a combination of a DbEntity and medium, such as a style file)
 * @type {*}
 */
Footprint.PresentationMediumImportView = SC.PickerPane.extend({
    classNames:'footprint-presentation-medium-import-view'.w(),
    contentView: SC.View.extend({
        childViews:['fileUpload', 'uri', 'ownerSelect', 'keySelect', 'errorMessage'],
        fileUpload: SC.View.extend(),
        // The query for the DbEntity if relevant (if the DbEntity represents a query or a database view)
        uri: Footprint.EditableModelStringView.extend({
            valueBinding: 'Footprint.presentationMediumEditController.dbEntity.name'
        }),
        ownerSelect: Footprint.LabelSelectView.extend({
            itemTitleKey: 'name'
            // What ConfigEntity context will own the DbEntity (Scenario or Project)
        }),
        keySelect: Footprint.KeyInfoView.extend({
            valueBinding: 'Footprint.presentationMediumEditController.dbEntity'
        }),
        errorMessage: SC.View.extend()
    })
});
