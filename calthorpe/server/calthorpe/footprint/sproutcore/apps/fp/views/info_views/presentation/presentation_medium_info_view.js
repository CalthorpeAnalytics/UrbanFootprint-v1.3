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

sc_require('views/editable_model_string_view');
sc_require('views/info_views/geography_info_view');
sc_require('views/info_views/tags_info_view');
sc_require('views/info_views/medium_info_view');
sc_require('views/info_views/query_info_view');
sc_require('views/info_views/table_info_view');
sc_require('views/info_views/key_info_view');
sc_require('views/info_views/presentation/style_info_view');
sc_require('views/info_views/content_view');


/***
 * The pane used to edit the settings of a new or existing PresentationMedium and the DbEntity to which it is associated (if any). The saving order of this will have to first save a created DbEntity and then the PresentationMedium if a DbEntity is being created here
 * @type {*}
 */
Footprint.PresentationMediumInfoView = Footprint.InfoPane.extend({
    classNames:'footprint-presentation-medium-info-view'.w(),
    layout: { top:0, left: 0, width:400, height:400 },

    recordType: Footprint.PresentationMedium,
    refreshTarget: Footprint.LayerSectionView,
    controllers: Footprint.layerControllers,

    contentView: SC.ScrollView.extend({ // Creates an intermediate view as well

        contentView: Footprint.ContentView.extend({
            childViews:['nameView', 'tableView', 'queryView', 'keyView', 'descriptionView', 'geographyView', 'tagsView', 'styleView', 'commitButtonsView'],

            // The content of the view is the PresentationMedium
            contentBinding: parentViewPath(3, '.editController'),
            // Various collections not specific to the content needed by child views
            contextBinding: parentViewPath(3, '.recordSetController'),

            nameView: Footprint.NameItemView.extend({
                layout: {width: .9, height: .05, top: 0},
                contentBinding: parentViewPath(1, '*content.db_entity_interest.db_entity')
            }),

            tableView: Footprint.TableInfoView.extend({
                layout: {width: .9, height: .05, top: .05},
                contentBinding: parentViewPath(1, '*content.db_entity_interest.db_entity')
            }),

            // The query for the DbEntity if relevant (if the DbEntity represents a query or a database view)
            queryView: Footprint.QueryInfoView.extend({
                layout: {width: .9, height: .2, top: .1},
                contentBinding: parentViewPath(1, '*content.db_entity_interest.db_entity')
            }),

            keyView: Footprint.KeyInfoView.extend({
                layout: {width: .9, height: .05, top: .3},
                keyItemPath:'key',
                contentBinding: parentViewPath(1, '*content.db_entity_interest.db_entity')
            }),

            descriptionView: Footprint.DescriptionItemView.extend({
                layout: {width: .9, height: .1, top: .35},
                contentBinding: parentViewPath(1, '*content.db_entity_interest.db_entity')
            }),

            geographyView: Footprint.GeographyInfoView.extend({
                layout: {width: .9, height: .05, top: .45},
                contentBinding: parentViewPath(1, '*content.db_entity_interest.db_entity')
            }),

            tagsView: Footprint.TagsInfoView.extend({
                layout: {width: .9, height: .05, top: .5},
                contentBinding: parentViewPath(1, '*content.db_entity_interest.db_entity')
            }),

            styleView: Footprint.StyleInfoView.extend({
                layout: {width: .9, height: .4, top: .55},
                // Present other PresentationMedium instances of the Presentation in a select box so that
                // their style information might be copied.
                // TODO this actually needs to be other instances of the same table and thus the same attributes
                // or a way to copy over individual attribute styles
                itemsBinding: SC.Binding.oneWay(parentViewPath(1, '*context.items')),
                // With the PresentationMedium instance as the content, we want to be able to copy the medium_context
                // attributes from the selected value in the select box to the content.
                objectPath: '.medium_context'
            }),

            commitButtonsView: Footprint.InfoPaneButtonsView.extend({
                layout: {width: .9, height: .05, top: .95}
            })
        })
    })
});

Footprint.LayerInfoView = Footprint.PresentationMediumInfoView.extend({
    refreshTarget: Footprint.PresentationMediumInfoView,
    controllers: Footprint.layerControllers
});

Footprint.ResultInfoView = Footprint.PresentationMediumInfoView.extend({
    refreshTarget: Footprint.ResultInfoView,
    controllers: Footprint.resultControllers
});
