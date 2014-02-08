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

/**
 * Source: http://yesudeep.wordpress.com/2009/07/25/implementing-a-pythonic-range-function-in-javascript-2/
 * Behaves just like the python range() built-in function.
 * Arguments:   [start,] stop[, step]
 *
 * @start   Number  start value
 * @stop    Number  stop value (excluded from result)
 * @step    Number  skip values by this step size
 *
 * Number.range() -> error: needs more arguments
 * Number.range(4) -> [0, 1, 2, 3]
 * Number.range(0) -> []
 * Number.range(0, 4) -> [0, 1, 2, 3]
 * Number.range(0, 4, 1) -> [0, 1, 2, 3]
 * Number.range(0, 4, -1) -> []
 * Number.range(4, 0, -1) -> [4, 3, 2, 1]
 * Number.range(0, 4, 5) -> [0]
 * Number.range(5, 0, 5) -> []
 *   Number.range(5, 4, 1) -> []
 * Number.range(0, 1, 0) -> error: step cannot be zero
 * Number.range(0.2, 4.0) -> [0, 1, 2, 3]
 */
Number.range = function() {
    var start, end, step;
    var array = [];

    switch(arguments.length){
        case 0:
            throw new Error('range() expected at least 1 argument, got 0 - must be specified as [start,] stop[, step]');
            return array;
        case 1:
            start = 0;
            end = Math.floor(arguments[0]) - 1;
            step = 1;
            break;
        case 2:
        case 3:
        default:
            start = Math.floor(arguments[0]);
            end = Math.floor(arguments[1]) - 1;
            var s = arguments[2];
            if (typeof s === 'undefined'){
                s = 1;
            }
            step = Math.floor(s) || (function(){ throw new Error('range() step argument must not be zero'); })();
            break;
    }

    if (step > 0){
        for (var i = start; i <= end; i += step){
            array.push(i);
        }
    } else if (step < 0) {
        step = -step;
        if (start > end){
            for (var i = start; i > end + 1; i -= step){ array.push(i);
            }
        }
    }
    return array;
};

/***
 *  A basic sequence class with which to construct intervals.
 * @param start
 * @param end
 * @param options
 */
function Sequence(values, options) {
    this.values = values;
    this.start = this.values[0];
    this.end = this.values.last();
    this.options = options || {};

    /***
     * Returns intervalCount Range objects evenly space between start and end
     * @param intervalCount
     */
    this.getIntervalRanges = function(intervalCount) {
        var calculateRange = d3.scale.linear()
            .domain([0,self.options.data.intervalCount-1])
            .range([sequenceData.min,sequenceData.max]);
        dd
        var self = this,
            fullRange = this.max-this.min,
            increment = fullRange/intervalCount;
        return $.map(Number.range(intervalCount), function(index) {
            new Sequence(self.min+increment*index, self.min+increment*(index+1))
        });
    };
    /***
     * Returns all the intervals, including min and max, by split the distance between min and max into interval count ranges. Thus intervalCount+1 values are returned
     * @param intervalCount
     */
    this.getIntervals = function(intervalCount) {
        var self = this;
        return $.map(this.getIntervalRanges(intervalCount), function(range) {return range.min;})+[this.max];
    };
}

