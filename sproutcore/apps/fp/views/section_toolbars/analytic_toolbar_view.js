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
sc_require('views/menu_button_view');
/***
 * Tests the binding and display of data in view Footprint.ProjectTitlebarView.
 */
Footprint.AnalyticToolbarViewView = Footprint.MenuButtonView.extend({
    classNames: 'footprint-policy-toolbar-view'.w(),
    anchorLocation: SC.ANCHOR_TOP,
    layout: { height: 32 },
    title: 'Analytic Modules',

    menuItems: function () {
        return this.get('defaultMenuItems');
    }.property('defaultMenuItems').cacheable(),

    defaultMenuItems: [
        // View and edit the selected item's attributes
        { title: 'Fiscal', action: 'showFiscalModule'},
        { title: 'VMT', action: 'showVMTModule'},
        { title: 'Energy', action: 'showEnergyModule'},
        { title: 'Water', action: 'showWaterModule'}
    ],
    itemsBinding: SC.Binding.oneWay('.menuItems')
});
