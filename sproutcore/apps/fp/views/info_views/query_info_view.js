
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

sc_require('views/clear_button_view');

// TODO this will become more complicated to handle separate group bys
Footprint.QueryInfoView = Footprint.InfoView.extend({
    classNames:'footprint-query-info-view'.w(),
    recordType: null,
    layout: {left: 0.01, right: 0.01, top: 5, height: 24},

    layerName: null,
    layerNameBinding: SC.Binding.oneWay('Footprint.layerActiveController.name'),
    title: function() {
        return 'Select features from %@'.fmt(this.get('layerName'));
    }.property('layerName'),

    // Toggle off to hide the summary fields (e.g. group by)
    showSummaryFields: YES,

    titleView: SC.LabelView.extend({
        classNames: "footprint-infoview-title-view".w(),
        layout: {left: 0.01, height: 24},
        valueBinding: '.parentView.title'
    }),

    contentView: SC.View.extend({
        classNames:'footprint-query-info-content-view'.w(),
        layout: {left: 0.01, right: 0.01, top: 26},
        childViews:'boundsView filterView joinView joinColumnsView queryButtonView aggregatesView groupByView'.w(),
        contentBinding: '.parentView.content',
        showSummaryFieldsBinding: SC.Binding.oneWay('.parentView.showSummaryFields'),
        isEnabledBinding: SC.Binding.oneWay('.parentView.isEnabled'),

        // Read-only view of selected bounds
        boundsView: Footprint.InfoView.extend({
            childViews:'titleView contentView clearButtonView'.w(),
            classNames:'footprint-query-info-bounds-view'.w(),
            layout: {width:0.48, top:0, height: 24},
            title: 'Bounds:',
            contentBinding: '.parentView*content',
            isEnabledBinding: SC.Binding.oneWay('.parentView.isEnabled'),
            titleView: SC.LabelView.extend({
                classNames: "footprint-infoview-title-view".w(),
                layout: {left: 0.01, height: 24, width: 0.1},
                valueBinding: '.parentView.title',
                needsEllipsis: YES
            }),
            contentView: SC.LabelView.extend({
                layout: {left: 0.12, right: 0.1},
                contentBinding: '.parentView.content',
                contentValueKey: 'boundsAsString',
                hint: 'No bounds selected. Drag bounds on the map to filter by bounds'
            }),
            clearButtonView: Footprint.ClearButtonView.extend({
                layout: {left: 0.9, width: 24},
                isVisibleBinding: SC.Binding.oneWay('.parentView*content.bounds').transform(function(bounds) {
                    return bounds && bounds.getPath('coordinates');
                }).bool(),
                isEnabledBinding: SC.Binding.oneWay('.parentView.isEnabled'),
                action: 'doClearBounds'
            })
        }),

        filterView: Footprint.InfoView.extend({
            childViews:'titleView contentView clearButtonView'.w(),
            classNames:'footprint-query-info-content-view'.w(),
            layout: {width:0.48, top:26, height: 24},
            title: 'Where:',
            contentBinding: '.parentView*content.query_strings',
            isEnabledBinding: SC.Binding.oneWay('.parentView.isEnabled'),
            titleView: SC.LabelView.extend({
                classNames: "footprint-infoview-title-view".w(),
                layout: {left: 0.01, height: 24, width: 0.1},
                valueBinding: '.parentView.title'
            }),
            contentView: Footprint.EditableModelStringView.extend({
                classNames: ['footprint-editable-content-view'],
                layout: {left: 0.12, right: 0.1},
                contentBinding: '.parentView.content',
                isEnabledBinding: SC.Binding.oneWay('.parentView.isEnabled'),
                contentValueKey: 'filter_string'
            }),
            clearButtonView: Footprint.ClearButtonView.extend({
                layout: {left: 0.9, width: 24},
                isVisibleBinding: SC.Binding.oneWay('.parentView*content.filter_string').bool(),
                isEnabledBinding: SC.Binding.oneWay('.parentView.isEnabled'),
                action: 'doClearFilter'
            })
        }),
        joinView: Footprint.SelectInfoView.extend({
            classNames:'footprint-query-info-join-view'.w(),
            layout: {left: 0, width:0.44, top:53, height: 24},
            title: 'Join:',
            titleView: SC.LabelView.extend({
                classNames: "footprint-infoview-title-view".w(),
                layout: {left: 0, height: 24, width: 0.1},
                valueBinding: '.parentView.title'
            }),
            contentLayout: {left: 0.12},

            recordType:null,
            recordTypeBinding:SC.Binding.oneWay('.parentView.recordType'),
            contentBinding: SC.Binding.oneWay('Footprint.joinLayersController.arrangedObjects'),
            // The status is based on the controller tracking content items--content itself has no status
            statusBinding: SC.Binding.oneWay('Footprint.joinLayersController.status'),
            selectionBinding: 'Footprint.joinLayersController.selection',
            itemTitleKey:'db_entity_key',
            includeNullItem:YES,
            nullTitle: 'None',
            isEnabledBinding: SC.Binding.oneWay('.parentView.isEnabled')
        }),

        /***
         * Displays the join columns available from the selected join.
         * This will go away when better auto-complete is up and running (as will the join)
         */
        joinColumnsView: Footprint.SelectInfoView.extend({
            classNames:'footprint-query-info-join-columns-view'.w(),
            layout: {left: 0.46, width:0.5, top:53, height: 24},
            isEnabledBinding: SC.Binding.oneWay('.parentView.isEnabled'),
            titleView: SC.LabelView.extend({
                classNames: "footprint-infoview-title-view".w(),
                layout: {left: 0, width: 0},
                isVisible: NO,
            }),
            contentLayout: {left:0},
            nullTitle: 'View available fields',
            // Primitives get their title from the content
            recordType:null,
            recordTypeBinding:SC.Binding.oneWay('.parentView.recordType'),
            contentBinding: SC.Binding.oneWay('Footprint.availableFieldsController.content'),
            selectionBinding: 'Footprint.availableFieldsController.selection',
            maxHeight: 300,
            // Don't let the user select anything
            isSelectable: NO,
            itemTitleView: 'content'
        }),

        queryButtonView: SC.ButtonView.design({
            classNames: ['footprint-query-info-query-button-view', 'theme-button', 'theme-button-green'],
            layout: {left:0.49, width:0.1, top:13, height: 24},
            isEnabledBinding: SC.Binding.oneWay('.parentView.isEnabled'),
            title: 'Query',
            action: 'doExecuteQuery',
            // We pass the layerSelection content to the action
            contentBinding: '.parentView.content',
            isEnabledBinding: SC.Binding.oneWay('.parentView.isEnabled')
        }),

        aggregatesView: Footprint.InfoView.extend({
            childViews:'titleView contentView clearButtonView'.w(),
            classNames:'footprint-query-info-aggregates-view'.w(),
            layout: {left:0.62, top:0, height: 24},
            isEnabledBinding: SC.Binding.oneWay('.parentView.isEnabled'),
            title: 'Aggregates',
            hint: 'Enter aggregates (e.g. SUM(du), AVG(emp))',
            isVisibleBinding: SC.Binding.oneWay('.parentView.showSummaryFields'),
            contentBinding: '.parentView*content.query_strings',
            contentView: Footprint.EditableModelStringView.extend({
                classNames: ['footprint-editable-content-view'],
                layout: {left: 0.2, right:0.1},
                contentBinding: '.parentView.content',
                contentValueKey: 'aggregates_string'
            }),
            clearButtonView: Footprint.ClearButtonView.extend({
                layout: {left: 0.9, width: 24},
                isVisibleBinding: SC.Binding.oneWay('.parentView*content.aggregates_string').bool(),
                isEnabledBinding: SC.Binding.oneWay('.parentView.isEnabled'),
                action: 'doClearAggregates'
            })
        }),

        groupByView: Footprint.InfoView.extend({
            childViews:'titleView contentView clearButtonView'.w(),
            classNames:'footprint-query-info-group-by-view'.w(),
            layout: {left:0.62, top:26, height: 24},
            isEnabledBinding: SC.Binding.oneWay('.parentView.isEnabled'),
            title: 'Group By',
            hint: 'Enter group-by columns of main or join table (e.g. blockgroup)',
            contentBinding: '.parentView*content.query_strings',
            isVisibleBinding: SC.Binding.oneWay('.parentView.showSummaryFields'),
            contentView: Footprint.EditableModelStringView.extend({
                classNames: ['footprint-editable-content-view'],
                layout: {left: 0.2, right:0.1},
                isEnabledBinding: SC.Binding.oneWay('.parentView.isEnabled'),
                contentBinding: '.parentView.content',
                contentValueKey: 'group_by_string'
            }),
            clearButtonView: Footprint.ClearButtonView.extend({
                layout: {left: 0.9, width: 24},
                isVisibleBinding: SC.Binding.oneWay('.parentView*content.group_by_string').bool(),
                isEnabledBinding: SC.Binding.oneWay('.parentView.isEnabled'),
                action: 'doClearGroupBy'
            })
        })
    })
});
