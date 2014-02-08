
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

/***
 * Adds stacking ability to charts
 * @type {{_transitionGrouped: Function, _transitionStacked: Function}}
 */
Footprint.ChartStackingToggleView = SC.CheckboxView.extend({

    layout: { left:10, width:70, height: 18, top: -15},
    classNames: ['result-toggle-view'],
    displayProperties: ['isStacked'],

    isStackable: null,
    isVisibleBinding: SC.Binding.oneWay('.isStackable'),

    action: function() {
        if (this.get('isStacked')) {
            this.getPath('parentView.content.configuration').is_stacked = NO;
            // this.getPath('parentView.content.configuration').notifyPropertyChange('is_stacked', NO);
            this._transitionToGrouped();
        } else {
            this.getPath('parentView.content.configuration').is_stacked = YES;
            // this.getPath('parentView.content.configuration').notifyPropertyChange('is_stacked', YES);
            this._transitionToStacked();
        }},
    title: 'Stack',


    /**
     * Enable the checkbox only when the chartView is initialized
     */
    //isEnabled: SC.Binding.oneWay('parentView.chartView.initialized'),


//    // Settable property that updates the configuration is_stacked property when the CheckboxView changes
//    isStacked: function(key, isStacked) {
//        if (isStacked !== undefined) {
//            this.setPath('parentView*content.configuration.is_stacked', isStacked);
//        }
//        return this.getPath('parentView*content.configuration.is_stacked') || NO;
//    }.property(),

   /**
    * Transitions from grouped bars to stacked bars
    * @private
    */
   _transitionToStacked: function() {

//       alert('Scroll this chart off the screen and back to refresh as stacked chart');

//       var millisecondsPerIndex = 10;
//       var xScale = this.getPath('chartView.xScale');
//       var yScale = this.getPath('chartView.yScale');
//       var data = this.get('data');
//       var height = this.getPath('chartView.height');
//       this.getPath('chartView.barSet').transition()
//           .duration(500)
//           .delay(function(d, i) { return i * millisecondsPerIndex; })
//           .attr("y", function(d) { return yScale(d.y0 + d.y); })
//           .attr("height", function(d) { return yScale(d.y0) - yScale(d.y0 + d.y); })
//           .transition()
//           .attr("x", function(d) { return xScale(d.x); })
//           .attr("width", xScale.rangeBand())
//           .style("stroke","#d0dae3")
//           .style("stroke-width", "0");
//
//       // Transition the y-axis to the new maximum height
//       this.getPath('chartView.graph').select(".y-axis")
//           .transition()
//           .duration(500)
//           .call(this.getPath('chartView.yAxis'));

   },

   /***
    * Transitions from stacked bars to grouped bars
    * @private
    */
   _transitionToGrouped:function() {

//       alert('Scroll this chart off the screen and back to refresh as grouped chart');
//       this.get('chartView').openingTransition();
//       return;
//
//       var millisecondsPerIndex = 10;
//       var xScale = this.getPath('chartView.xScale');
//       var yScale = this.getPath('chartView.yScale');
//       var data = this.get('data');
//       var height = this.getPath('chartView.height')
//       // Transition the bars
//       // Get all the bars
//       this.getPath('chartView.barSet').transition()
//           .duration(500)
//           // Delay by a function of the index so the transition is sequential
//           .delay(function(d, i) {
//               return i * millisecondsPerIndex; })
//           // Set the x attribute of each bar
//           .attr("x", function(d, i, j) {
//               return xScale(d.x) +
//                   xScale.rangeBand() / data.length * j; })// TODO data.length should be series.length I think
//           .attr("width", xScale.rangeBand() / data.length)
//           .transition()
//           .attr("y", function(d) { return yScale(d.y); })
//           .attr("height", function(d) { return height - yScale(d.y); })
//           .style("stroke","#d0dae3")
//           .style("stroke-width", "3");
//
//       // Transition the y-axis to support the new maximum height
//       this.getPath('chartView.graph').select(".y-axis")
//           .transition()
//           .duration(500)
//           .call(this.getPath('chartView.yAxis'));
   }

});