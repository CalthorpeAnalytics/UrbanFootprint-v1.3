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

sc_require('models/footprint_record');
sc_require('models/key_mixin');
sc_require('models/name_mixin');
sc_require('models/tags_mixin');

/**
 * A Mixin to identify the child items of each Policy, PolicySet or PolicyCategory for tree display
 * @type {Object}
 */
Footprint.PolicyTreeItemChildren = {
    treeItemIsExpanded: YES,
    treeItemChildren: function(){
        return this.get("policies");
    }.property()
};

Footprint.Policy = Footprint.Record.extend(
    Footprint.Key,
    Footprint.Name,
    Footprint.Tags,
    Footprint.PolicyTreeItemChildren, {

    value:SC.Record.attr(Number),
    // Sub policies
    policies: SC.Record.toMany("Footprint.Policy", {
        nested: true,
        inverse: "policies",
        isMaster:YES
    }),
    _copyProperties: function() { return 'policies'.w(); },
});



Footprint.PolicySet = Footprint.Record.extend(
    Footprint.Key,
    Footprint.Name,
    Footprint.PolicyTreeItemChildren, {

    policies: SC.Record.toMany("Footprint.Policy", {
        nested: true,
        inverse: "policy_set",
        isMaster:YES
    }),
    _copyProperties: function() { return 'policies'.w(); },
});
