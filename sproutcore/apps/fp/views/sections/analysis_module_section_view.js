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
sc_require('views/info_views/analytics/vmt_module_management_view');
sc_require('views/overlay_view');

Footprint.AnalysisModuleSectionView = SC.View.extend({
    classNames: ['footprint-analytic-section-view', 'footprint-map-overlay-section'],
    childViews: ['analysisModuleSelectView', 'contentView', 'overlayView', 'collapseButtonView'],

    collapseButtonView: SC.ButtonView.extend({
        // This button is rotated, making its layout a bit fiddly.
        layout: { top: 55, right: -30, height: 20, width: 80, rotateZ: -90 },
        classNames: ['theme-button-gray', 'theme-button', 'theme-button-shorter'],
        icon: sc_static('fp:images/section_toolbars/pulldown.png'),
        title: 'Collapse',
        action: function() {
            Footprint.analysisModulesController.set('analysisModuleSectionIsVisible', NO);
        }
    }),

    overlayView: Footprint.OverlayView.extend({
        contentBinding: SC.Binding.oneWay('Footprint.analysisModulesEditController.content'),
        statusBinding:SC.Binding.oneWay('*content.status')
    }),
    /**
     * Titlebar used to changed the active analytic module
     */

    analysisModuleSelectView:  Footprint.LabelSelectView.extend({
        layout: {height: 24 },
        contentBinding: SC.Binding.oneWay('Footprint.analysisModulesEditController.content'),
        isVisibleBinding: SC.Binding.oneWay('.content').notEmpty(false),
        itemTitleKey: 'name',

        // Conditionally give an empty list message
        scenarioNameBinding: SC.Binding.oneWay('Footprint.scenarioActiveController.name'),
        includeNullItemIfEmpty:YES,
        nullTitle: function() {
            return '%@ analysis modules for %@'.fmt(this.get('contentStatus') & SC.Record.READY ? 'No':'Loading', this.get('scenarioName'));
        }.property('scenarioName', 'contentStatus').cacheable(),

        selectionBinding: 'Footprint.analysisModulesEditController.selection',
        selectedItemBinding: '.selection.firstObject',
        nowShowingView:function() {
            if (this.getPath('selection.firstObject'))
                return 'Footprint.%@ModuleManagementView'.fmt(this.getPath('selection.firstObject.key').camelize().capitalize());
        }.property('selection').cacheable()
    }),

    contentView: SC.ContainerView.extend({
        classNames: 'footprint-analytic-section-content-view'.w(),
        layout: {top:24},
        nowShowingBinding: SC.Binding.oneWay('.parentView.analysisModuleSelectView.nowShowingView')
    })
});

