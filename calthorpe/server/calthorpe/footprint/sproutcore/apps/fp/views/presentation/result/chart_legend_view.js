
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


Footprint.ChartLegendView = SC.View.extend({

    layout: { left:0, top:0.8, height: 30 },
    classNames: ['result-legend-view'],

    keys: null,
    columnToLabel: null,

    didCreateLayer: function () {
        this.notifyPropertyChange('data');
    },

    displayProperties:['data','keys','columnToLabel'],
    /***
     * Create a legend for the graph
     */
    update: function (context) {
        if (!this.get('keys') || !this.get('columnToLabel'))
          return;

        // sets legend margins
        var legendMargins = {left: 32, top: 4, right: 4, bottom: 4},
            legendWidth = 300, // - (legendMargins.left + legendMargins.right),
            legendSquare = 11,
            legendHeight = 15;

        // draws legend box
        var legendSvg = d3.selectAll(context).append("svg")
            .attr("width", legendWidth)
            .attr("height", legendHeight)
            .append("g");

        var numKeys = this.get('keys').length;

        var legend = legendSvg.selectAll("legend")
            .data(this.get('keys').map(function(key) {
                return this.get('columnToLabel')[key];
            }, this).slice())
            .enter().append("g")
            .attr("class", "legend")
            .attr("transform", function(d,i) {

                // Shift every other legend item over so that there are two columns of legend items
                var extraHorizontalShift = (i%2 == 0) ? legendWidth/2 : 0;
                // Shift down each row of two legend items
                var verticalShift = Math.floor(i/2)*legendHeight;

                return "translate(" + (legendMargins.left + extraHorizontalShift) + ", " + verticalShift + ")";
            });

        // draws swatches
        var colorScale = this.getPath('parentView.colorScale');
        legend.append("rect")
            .data(this.getPath('parentView.data'))
            .attr("x", (legendHeight - legendSquare)/2)
            .attr("y", (legendHeight - legendSquare)/2)
            .attr("width", legendSquare)
            .attr("height", legendSquare)
            .style("fill", function(d, i) { return colorScale(i); })
            .style("stroke","#d0dae3")
            .style("stroke-width", "1");

        // writes key names
        legend.append("text")
            .attr("x", legendSquare + 2 + (legendHeight - legendSquare)/2)
            .attr("y", (legendHeight - legendSquare/2))
            .style("text-anchor", "start")
            .text(function(d) { return d; });

        var isStackable = this.getPath('content.configuration.stackable');

    }
});
