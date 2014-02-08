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

sc_require('models/scenarios_models');
sc_require('views/editable_model_string_view');
sc_require('views/info_views/geography_info_view');
sc_require('views/info_views/tags_info_view');
sc_require('views/info_views/medium_info_view');
sc_require('views/info_views/info_pane');
sc_require('views/info_views/content_view');

/***
 * The pane used to edit the settings of a new or existing PresentationMedium and the DbEntity to which it is associated (if any). The saving order of this will have to first save a created DbEntity and then the PresentationMedium if a DbEntity is being created here
 * @type {*} */
Footprint.ScenarioInfoView = Footprint.InfoPane.extend({
    layout: { top:0, left: 0, width:500, height:200 },
    classNames:'footprint-scenario-info-view'.w(),

    recordType:Footprint.Scenario,
    selectionListBinding: SC.Binding.oneWay('Footprint.scenariosController.content'),
    contentBinding: SC.Binding.oneWay('Footprint.recordEditController.content'),

    contentView: Footprint.ContentView.extend({
        childViews:['nameView', 'yearView', 'keyView', 'descriptionView', 'commitButtonsView'],

        contentBinding: SC.Binding.oneWay('.parentView.content'),

        nameView: Footprint.NameItemView.extend({
            valueBinding: '.parentView*content.name',
            layout: {width: .9, top: .1, height: .1},
            isEditable:YES
        }),
        yearView: Footprint.YearItemView.extend({
            valueBinding: '.parentView*content.year',
            layout: {width: .9, top: .2, height: .1},
        }),
        keyView: Footprint.NameItemView.extend({
            valueBinding: '.parentView*content.key',
            title:'Key',
            layout: {width: .9, top: .3, height: .1},
            isEditable:YES
        }),
        descriptionView: Footprint.DescriptionItemView.extend({
            layout: {width: .9, top: .4, height: .2}
        }),

        // TODO redo
        categoriesView: Footprint.CategoriesInfoView.extend({
            layout: {width: .9, top: .6, height: .12}
        }),

        commitButtonsView: Footprint.InfoPaneButtonsView.extend({
            layout: {width: .9, bottom: 0, height: .2},
            isEditable: YES,
            contentBinding: '.parentView*content'
        })
    })
});
