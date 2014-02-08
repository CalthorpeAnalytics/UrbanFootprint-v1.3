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

Footprint.AnalyticBarView = SC.View.extend({
    childViews:'barView labelView'.w(),
    layout: { height:20 }, // Sensible default
    classNames: "footprint-analytic-bar-view".w(),

    /**
     * The specific Result to use for this bar. If not specified the first result with configuration.result_type=='analytic_bars' will be used
     */
    dbEntityKey:null,

    /**
     * The specific query attribute key of the Result to show
     */
    queryAttributeKey:null,


    /***
     * The configEntity from which we get the results
     */
    configEntity:null,
    configEntityStatus:null,
    configEntityStatusBinding: SC.Binding.oneWay('*configEntity.status'),
    presentations:null,
    presentationsBinding:SC.Binding.oneWay('*configEntity.presentations.results'),
    presentationsStatus:null,
    presentationsStatusBinding:SC.Binding.oneWay('*presentations.status'),
    /**
     * The Results of a LayerLibrary instance. This is bound to the resultsController content
     */
    content:function() {
        if (this.get('presentations') && (this.getPath('presentationsStatus') & SC.Record.READY)) {
            return this.get('presentations').filter(function(presentation, i) {
                return presentation.get('key') == 'result_library__default';
            }, this)[0].get('presentation_media');
        }
    }.property('presentations', 'presentationsStatus').cacheable(),

    /***
     * The result matching the dbEntityKey
     */
    result: function() {
        // Find the Result matching dbEntityKey or the first result of result_type 'analytic_bars'
        if (this.get('content'))
            return this.get('content').filter(function(result) {
                return this.get('dbEntityKey') ?
                    result.get('db_entity_key') == this.get('dbEntityKey') :
                    result.getPath('configuration.result_type') == 'analytic_bars';

            }, this)[0];
    }.property('content', 'dbEntityKey').cacheable(),
    resultStatus:null,
    resultStatusBinding:SC.Binding.oneWay('*result.status'),

    overallMinimum:null,
    overallMaximum:null,

    /***
     * The minimum value of the bar
     */
    minimum:function() {
        /*
        if (this.get('value')) {
            var digits = Number(this.get('value')).toString().length-1;
            return Number(this.get('value')).toNearest(Math.pow(10,(digits)));
        }
        */
        return this.getPath('result.configuration.extent_lookup.%@.min'.fmt(this.get('queryAttributeKey')));
    }.property('result', 'queryAttributeKey').cacheable(), //.property('value').cacheable(),

    /***
     * The maximum value of the bar
     */
    maximum:function() {
        /*
        if (this.get('value')) {
            var digits = Number(this.get('value')).toString().length-1;
            return Number(this.get('value')*10).toNearest(Math.pow(10,(digits)));
        }
        */
        return this.getPath('result.configuration.extent_lookup.%@.max'.fmt(this.get('queryAttributeKey')));
    }.property('result', 'queryAttributeKey').cacheable(), //,property('value').cacheable(),

    /***
     * Returns a dict that maps result query column names to generalized attributes. This allows the table columns
     * to have non-standard names, but our SC attributes/properties can be standardized
     * (e.g. dwelling_units:households__sum)
     * @returns {*}
     * @private
    */
    attributeToColumn: function() {
        return this.getPath('result.configuration.attribute_to_column');
    }.property('result').cacheable(),

    dbColumn:function() {
        if (this.get('attributeToColumn') && this.get('queryAttributeKey'))
            return this.get('attributeToColumn')[this.get('queryAttributeKey')]
    }.property('attributeToColumn', 'queryAttributeKey').cacheable(),

    queryLookup:function() {
        if (this.get('result'))
            return $.mapObjectToObject(
                this.getPath('result.query'),
                function(key, value) {
                    // Remove the __sum or part so we match our attribute
                    return [key.split('__')[0], value]
                });
    }.property('result').cacheable(),

    /***
     * The value of the query attribute based on the queryAttributeKey
     */
    value: function() {
        if (this.get('queryLookup') && this.get('dbColumn'))
           return this.get('queryLookup')[this.get('dbColumn')];
    }.property('queryLookup', 'dbColumn').cacheable(),

    barView: SC.ProgressView.extend({
        minimumBinding:SC.Binding.oneWay('.parentView.minimum'),
        maximumBinding:SC.Binding.oneWay('.parentView.maximum'),
        valueBinding: SC.Binding.oneWay('.parentView.value'),

        observeInitial:function() {
            if (!this.getPath('parentView.value'))
                this.set('value', this.get('minimum'));
        }.observes('.minimum')
    }),

    labelView: SC.LabelView.extend({
        parentValue:null,
        parentValueBinding:SC.Binding.oneWay('.parentView.value'),
        value: function() {
            var value = this.get('parentValue');
            return value ? d3.format(',f')(value) : 'N/A';
        }.property('result', '.parentValue').cacheable()
    }),

    toString: function() {
        return this.toStringAttributes('minimum maximum configEntity content dbEntityKey queryAttributeKey result value attributeToColumn'.w());
    }
});


