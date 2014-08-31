/*
 * UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
 *
 * Copyright (C) 2014 Calthorpe Associates
 *
 * This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
 *
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
 */

sc_require('views/section_toolbars/toolbar_view');
sc_require('views/section_toolbars/title_view');
sc_require('views/section_toolbars/edit_title_view');

/**
 * Extends TitlebarView to add an edit button view
 * @type {*}
 */
Footprint.EditingToolbarView = Footprint.ToolbarView.extend({

    childViews: 'titleView'.w(),
    classNames: "footprint-editing-toolbar-view".w(),
    content: null,
    contentNameProperty: null,
    recordType: null,
    activeRecord: null,
    menuItems: null,
    controlSize: null,
    title: null,
    icon: sc_static('fp:images/section_toolbars/pulldown.png'),

    // This contains the title and the pull down
    titleView: Footprint.EditTitleView.extend({
        layoutBinding: SC.Binding.oneWay('.parentView.titleViewLayout'),
        titleBinding: SC.Binding.oneWay('.parentView.title'),
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        contentNamePropertyBinding:SC.Binding.oneWay('.parentView.contentNameProperty'),
        recordTypeBinding: SC.Binding.oneWay('.parentView.recordType'),
        activeRecordBinding: SC.Binding.oneWay('.parentView.activeRecord'),
        menuItemsBinding: SC.Binding.oneWay('.parentView.menuItems'),
        controlSizeBinding: SC.Binding.oneWay('.parentView.controlSize'),
        iconBinding: SC.Binding.oneWay('.parentView.icon')
    })
});
