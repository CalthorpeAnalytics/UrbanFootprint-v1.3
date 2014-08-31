
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

/***
 * Displays the single value if a single value is shared among propKey property value of the 'content' items
 * If all resolved values are the same, the value is returned. Otherwise null is returned
 * If value is passed, the property value of all items is set to value
 * @type {Function}
 */
Footprint.pluralProperty = function(propKey, value) {
    var content = this.get('content');
    if (!content || !(this.getPath('contentStatus') & SC.Record.READY))
        return;

    if (value !== undefined) {
        // Setter
        content.forEach(function(item) {
            // Set all items' property to the value
            item.set(propKey, value)
        })
    }
    // Getter
    // For multiple items return null unless all have the same property value
    return content.mapProperty(propKey).uniq().length==1 ? content.firstObject().get(propKey) : null;
}.property('contentStatus', 'content');

/***
 * Displays the range shared among the propKey property values of the content items
 * Assumes the propKey is the name of the content's attribute that we are interested in display in the form attribute__range
 * TODO make the content and property properties function arguments
 * @type {Function}
 */
Footprint.pluralRangeProperty = function(propKey, value) {
    var property = propKey.split('__')[0];
    var content = this.get('content');
    if (!content || !(this.get('contentStatus') & SC.Record.READY))
        return;

    // Getter
    // For multiple items return the range unless only 1 value exists
    return content.mapProperty(property).uniq().length==1 ? null : 'range %@-%@'.fmt(content.mapProperty(property).min(), content.mapProperty(property).max());
}.property('contentStatus', 'content');
