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

sc_require('views/info_views/geography_info_view');
sc_require('views/info_views/tags_info_view');
sc_require('views/info_views/medium_info_view');
sc_require('views/sections/analytic_section_view');



/***
 * The pane used to edit the settings of a new or existing Policy and the DbEntity to which it is associated (if any). The saving order of this will have to first save a created DbEntity and then the Policy if a DbEntity is being created here
 * @type {*}
 */
Footprint.PolicyInfoView = Footprint.InfoPane.extend({
    classNames:'footprint-policy-info-view'.w(),
    layout: { top:0, left: 0, width:400, height:400 },

    recordType: Footprint.Policy,
    refreshTarget: Footprint.AnalyticSectionView,
    controllers: Footprint.policyControllers,

    contentView: SC.View.extend({
        childViews:['nameView', 'keyView', 'descriptionView', 'valueView', 'tagsView', 'commitButtonsView'],

        nameView: Footprint.NameInfoView.extend({
            useStaticLayout:YES,
            layout: {width: .9, height: .05}
        }),
        keyView: Footprint.KeyInfoView.extend({
            useStaticLayout:YES,
            layout: {width: .9, height: .1}
        }),
        descriptionView: Footprint.DescriptionItemView.extend({
            useStaticLayout:YES,
            layout: {width: .9, height: .1}
        }),
        valueView: Footprint.InfoView.extend({
            useStaticLayout:YES,
            layout: {width: .9, height: .08},

            title: 'Value',
            contentView: Footprint.EditableModelStringView.extend({
                layout: {left: .2, width: .8},
                valueBinding: parentViewPath(2,'*content.value')
            })
        }),
        tagsView: Footprint.TagsInfoView.extend({
            useStaticLayout:YES,
            layout: {width: .7, height: .1}
        }),
        commitButtonsView: Footprint.InfoPaneButtonsView.extend({
            useStaticLayout:YES,
            layout: {width: .9, height: .1}
        })
    })
});
