/*
 * UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
 *
 * Copyright (C) 2013 Calthorpe Associates
 *
 * This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
 *
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
 */
Footprint.QueryingState = SC.State.extend({

    initialSubstate:'parsingState',

    parsingState: SC.State.extend({
        enterState: function(context) {
            var aggregatesString = context.get('aggregatesString');
            var aggregates = aggregatesString && aggregatesString.split(',');
            var joins = context.get('joins').toArray();
            var queryString = context.get('queryString');
            var queryFactory = SC.Query.create();
            var tokenList = queryFactory.tokenizeString(queryString, queryFactory.queryLanguage);
            if (tokenList.error)
                throw tokenList.error;
            var query = queryFactory.buildTokenTree(tokenList, queryFactory.queryLanguage);
            if (query.error) {
                SC.AlertPane.warn({
                    message: "Could not parse query",
                    description: "Only basic operators are currently available: '>, <, ='. You can refer to properties by name. Example: built_form.name = 'SACOG Agriculture'"
                });
                Footprint.statechart.sendEvent('selectionDidEnd',
                    SC.Object.create({content:Footprint.layerSelectionActiveController.content}));
            }

            var groupByString = context.get('groupByString');

            this.gotoState('savingQueryState', SC.Object.create({
                query:query,
                aggregates:aggregates,
                groupBy:groupByString,
                joins:joins
            }))
        }
    }),

    savingQueryState: SC.State.plugin('Footprint.SavingSelectionState'),


    // Tell the map controller whenever a new selection layer is ready
    selectionDidUpdate:function(context) {
        Footprint.mapController.refreshSelectionLayer();
        Footprint.statechart.sendEvent('selectionDidEnd', context)
    },
    selectionDidError: function(context) {
        SC.AlertPane.error({
            message: 'A query error occurred',
            description: 'There was an error processing your query. Sorry for the inconvenience. A log of the error has been created, and we\'re working on improving it!'
        });
        // slight hack... an errored selection behaves the same as an updated selection + error message... so
        // we keep it internal here rather than routing it through an action call.
        this.selectionDidUpdate(context);
    },

    selectionDidEnd: function(context) {
        if (!context.getPath('content.features.length'))
        // If there are no features selected
            this.gotoState('noSelectionState');
        else
        // Selection is ready to load the full Features
            this.gotoState('selectionIsReadyState');
    }
});
