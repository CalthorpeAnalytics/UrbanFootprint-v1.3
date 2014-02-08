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

    initialSubstate:'readyState',

    readyState: SC.State.extend({
        enterState: function(context) {
            if (this.parseQuery(Footprint.layerSelectionEditController)) {
                Footprint.statechart.sendAction('queryDidValidate', Footprint.layerSelectionEditController);
            }
            else {
                Footprint.statechart.sendAction('queryDidFail', Footprint.layerSelectionEditController);
            }
        },

        parseQuery: function(context) {

            // Parse the filter string using our enhanced SCQL
            // TODO prevent empty string weirdness
            if (!context.getPath('query_strings.filter_string'))
                context.setPath('query_strings.filter_string', null);
            var filterString = context.getPath('query_strings.filter_string');
            var filter = null;
            if (filterString) {
                var filter = processQuery(filterString);
                if (filter.error) {
                    SC.AlertPane.warn({
                        message: "Could not parse query",
                        description: "Only basic operators are currently available: '>, <, ='. You can refer to properties by name. Example: built_form.name = 'Agriculture'"
                    });
                    Footprint.statechart.gotoState(this.get('fullPath'), context);
                    return NO;
                }
            }
            Footprint.layerSelectionEditController.set('filter', filter);

            // Parse each comma-separated aggregate in the aggregatesString using our enhanced SCQL
            // TODO prevent empty string weirdness
            if (!context.getPath('query_strings.aggregates_string'))
                context.setPath('query_strings.aggregates_string', null);
            var aggregatesString = context.getPath('query_strings.aggregates_string');
            try {
                Footprint.layerSelectionEditController.set('aggregates', aggregatesString ? aggregatesString.split(',').map(function(aggregate) {
                    // Parse each separate for now, since SCQL can't handle selection strings
                    var aggregateQuery = processQuery(aggregate);
                    if (aggregateQuery.error) {
                        SC.AlertPane.warn({
                            message: "Could not parse aggregate field",
                            description: "Only SUM(field) AVG(field) and COUNT(field) are currently supported. Multiples may be separated by commas, such as SUM(du), AVG(emp)"
                        });
                        Footprint.statechart.gotoState(this.get('fullPath'), context);
                        throw "give up";
                    }
                    return aggregateQuery;
                }) : null);
            }
            catch(e) {
                return NO;
            }

            // Parse the single groupBy string in groupByString using our enhanced SCQL
            if (!context.getPath('query_strings.group_by_string'))
                context.setPath('query_strings.group_by_string', null);
            var groupByString = context.getPath('content.query_strings.group_by_string');
            try {
                Footprint.layerSelectionEditController.set('group_bys', groupByString ? groupByString.split(',').map(function(groupBy) {
                    var groupByQuery = processQuery(groupBy);
                    if (groupByQuery.error ) {
                        SC.AlertPane.warn({
                            message: "Could not parse group by text",
                            description: "This should be comma-separated properties of the main feature table or that specified by join. Example, land_use_code or built_form.id"
                        });
                        Footprint.statechart.gotoState(this.get('fullPath'), context);
                        throw "give up";
                    }
                    return groupByQuery;
                }): null);
            }
            catch(e) {
                return NO;
            }
            return YES;
        }
    })
});
