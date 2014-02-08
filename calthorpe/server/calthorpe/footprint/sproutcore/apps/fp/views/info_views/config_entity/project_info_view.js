/* 
 * UrbanFootprint-California (v1.0), Land Use Project Development and Modeling System.
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

sc_require('views/editable_model_string_view');
sc_require('views/info_views/geography_info_view');
sc_require('views/info_views/tags_info_view');
sc_require('views/info_views/medium_info_view');
sc_require('views/info_views/info_pane');
sc_require('views/info_views/categories_info_view');
sc_require('views/info_views/year_info_view');
sc_require('views/info_views/content_view');

sc_require('views/info_views/config_entity/project_info_view');

/***
 * The pane used to edit the settings of a new or existing PresentationMedium and the DbEntity to which it is associated (if any). The saving order of this will have to first save a created DbEntity and then the PresentationMedium if a DbEntity is being created here
 * @type {*}
 */
Footprint.ProjectInfoView = Footprint.InfoPane.extend({
    layout: { top: 0, left: 0, width: 400, height: 400 },
    classNames: 'footprint-project-info-view'.w(),

    recordType: Footprint.Project,

    controllers: Footprint.projectControllers,

    contentView: Footprint.ContentView.extend({
        childViews: ['nameView', 'yearView', 'keyView', 'descriptionView', 'geographyView', 'categoriesView'],

        refreshTarget: Footprint.ProjectToolbarView,
        controllers: Footprint.projectControllers,
        // Bind to the controller so children access the content items by delegation
        contentBinding: parentViewPath(1, '*editController'),

        nameView: Footprint.NameItemView.extend({
            useStaticLayout: YES,
            layout: {width: .9, height: .05}
        }),
        yearView: Footprint.YearItemView.extend({
            useStaticLayout: YES,
            layout: {width: .9, height: .05}
        }),
        keyView: Footprint.KeyInfoView.extend({
            useStaticLayout: YES,
            layout: {width: .9, height: .1}
        }),
        descriptionView: Footprint.DescriptionItemView.extend({
            useStaticLayout: YES,
            layout: {width: .9, height: .1}
        }),
        geographyView: Footprint.GeographyInfoView.extend({
            useStaticLayout: YES,
            layout: {width: .9, height: .1}
        }),
        categoriesView: Footprint.CategoriesInfoView.extend({
            useStaticLayout: YES,
            layout: {width: .9, height: .1}
        }),
        commitButtonsView: Footprint.InfoPaneButtonsView.extend({
            useStaticLayout: YES,
            layout: {width: .9, height: .1}
        })
    })
});
