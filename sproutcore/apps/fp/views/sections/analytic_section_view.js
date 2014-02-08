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

sc_require('views/section_toolbars/analytic_toolbar_view');
sc_require('views/info_views/analytics/fiscal_module_management_view');

Footprint.AnalyticSectionView = SC.View.extend({
    classNames: 'footprint-analytic-section-view'.w(),
    childViews: 'analyticModuleToolbarView contentView'.w(),

    nowShowingBinding: SC.Binding.oneWay('Footprint.showingAnalyticModuleController.nowShowing'),

    nowShowingView:function() {
        return this.getPath('nowShowing') || 'Footprint.FiscalModuleManagementView';
    }.property('nowShowing').cacheable(),

    /**
     * Titlebar used to changed the active PolicySet
     */

    analyticModuleToolbarView: Footprint.AnalyticToolbarViewView.extend({
        layout: { height: 24 }
    }),

    contentView: SC.ContainerView.extend({
        classNames: 'footprint-analytic-section-content-view'.w(),
        layout: {top:24},
        nowShowingBinding: SC.Binding.oneWay('.parentView.nowShowingView')
    })
});

