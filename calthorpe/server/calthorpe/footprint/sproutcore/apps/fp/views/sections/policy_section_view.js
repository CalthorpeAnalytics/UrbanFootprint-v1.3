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

sc_require('views/section_titlebars/policy_toolbar_view');

Footprint.PolicySectionView = SC.View.extend({
    classNames: 'footprint-policy-section-view'.w(),
    childViews: 'policySetToolbarView listView'.w(),
    layout: { width: 200, right: 0 },

    /**
     * Titlebar used to changed the active PolicySet
     */
    policySetToolbarView: Footprint.PolicyToolbarView.extend({
        layout: { height: 24 }
    }),

    listView: SC.ScrollView.extend({
        layout: { top: 24, bottom: 0 },
        contentView: SC.SourceListView.extend({
            isEnabledBindng: SC.Binding.oneWay('content').bool(),
            rowHeight: 20,
            contentBinding: SC.Binding.oneWay('Footprint.policyCategoriesTreeController.arrangedObjects'),
            contentValueKey: 'name',
            selectionBinding: SC.Binding.from('Footprint.policyCategoriesTreeController.selection'),

            exampleView: SC.ListItemView.extend({
                childViews: 'valueView'.w(),

                valueView: SC.LabelView.extend({
                    layout: { left: .7, width: 40 },
                    valueBinding: SC.Binding.from('.parentView.content.value').transform(function (value, forward) {
                        return value && d3.format('.0%')(value);
                    })
                }),

                render: function (context, firstTime) {
                    // hack to keep child views from disappearing when ListItemView is selected
                    if (firstTime) {
                        sc_super();
                    }
                },
            }),
        }),
    }),
});

