/*
 * UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
 *
 * Copyright (C) 2014 Calthorpe Associates
 *
 * This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
 *
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>. *
 * Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
 */
sc_require('mixins/selected_item');
sc_require('views/section_toolbars/title_view');

Footprint.ToolbarView = SC.View.extend(Footprint.SelectedItem, {
    layout: {height: 17},

    childViews: 'titleView'.w(),
    classNames: "footprint-toolbar-view".w(),
    contentNameProperty:null,

    title: null,
    /**
     * An observable object keyed by view name and valued by the title to display for each configured view.
     * The given value of the labelView will be formatted to specify the controller.name property
     */
    titles: null,

    /**
     * The view which actually shows the main title of the whatever section of the app the TitlebarView is describing
     * The title is formed by combining titles.labelView with the controller.name or "Loading controller.name"
     * if the latter isn't READY
     */
    titleView: Footprint.TitleView.extend({
        contentNamePropertyBinding:SC.Binding.oneWay('.parentView.contentNameProperty'),
        titleBinding: SC.Binding.oneWay('.parentView.title'),
        contentBinding: SC.Binding.oneWay('.parentView.content')
    })
});

