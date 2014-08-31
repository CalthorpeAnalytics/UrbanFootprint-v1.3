
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

/***
 * Used by the tree controller to create a hierarchy
 * @type {*}
 */
Footprint.TreeItem = SC.Object.extend({
    keyObject:null,
    nodes:null,
    // The property o the keyObject that is its viewable name
    keyNameProperty:null,
    nodeSet:null,

    name:function() {
        return this.get('keyObject').getPath(this.get('keyNameProperty'));
    }.property('keyNameProperty'),

    treeItemIsExpanded: YES,
    treeItemChildren: function(){
        return this.get('nodes');
    }.property('nodes'),

    toString: function() {
        return "%@:\n%@".fmt(sc_super(), this.toStringAttributes('keyObject keyNameProperty name'.w()));
    }
});

/**
 * Objectifies the relationship between top level items and second level items (and possibly deeper)
 * The data structure is {key_string1: {key: top_level_instance, values: second_level_instances}, key_string2: ...} where key_string1 is a string version of the top_level_instance so that the values can be grouped under a single key.
 */
Footprint.TreeContent = SC.Object.extend({
    /***
     * Subclasses must set or bind the following properties, unless the derivitive properties are set, as described:
    */

    /***
     * The unique key objects used by the the TreeController. These are model instances that have a string property that label the top-level tree nodes
     */
    keyObjects: null,
    keyObjectsStatus:null,
    keyObjectsStatusBinding: '*keyObjects.status',

    // The container object holding the nodes. Used with keyProperty to get the nodes
    nodeSet: null,
    // The property of node that resolves keyObject that matches one of keyObjects
    keyProperty:null,
    // The property of the nodes that access their name for display
    keyNameProperty:null,
    // Override to a return a function that resolves the node to a value for the tree
    // Normally the value of the tree will be the node itself
    nodeValueLookup: null,

    // The nodes of the tree.
    nodes:null,
    nodesStatus:null,
    nodesStatusBinding:SC.Binding.oneWay('*nodes.status'),

    // Start the tree expanded
    treeItemIsExpanded: YES,
    // The name of the root element
    name: "root",

    /***
     * Default sorting properties for the nodeSet level of tree controllers
     */
    nodeSetSortProperties: ['name'],
    /***
     * Dict with key: YES for any sorting key that should be reversed
     */
    reverseNodeSetSortDict: null,

    /***
     * Default sorting properties for the node level of tree controllers
     */
    sortProperties:['name'],
    /***
     * Dict with key: YES for any sorting key that should be reversed
     */
    reverseSortDict: null,

    /***
     * A Default key object to use if no keys are found for a node.
     * If not specified unmatched nodes will not appear in the tree
     */
    undefinedKeyObject: null,

    /***
     * Creates a object whose attributes are the top-level tree key names and values are the nodes with that key
     */
    tree:function() {
        var self = this;
        var keyObjects = this.get('keyObjects');
        return $.mapToCollectionsObjectWithObjectKeys(
            self.get('nodes') || [],
            function(node) { // create 'keys' attributes
                var list = arrayOrItemToArray(node.getPath(self.get('keyProperty'))).filter(
                    function(keyObject) {
                        // only accept the key objects that match keyObjects
                        // This allows us to filter out keyObjects of the nodes that we don't care about
                        // For instance, with Scenarios we only care about Category instances whose key property is
                        // 'category'
                        // Use id comparison since we traditionally load the full set as non-nested and the attribute
                        // version as nested. Comparing nested to non-nested records no longer works
                        return keyObjects.mapProperty('id').contains(keyObject.get('id'));
                    },
                    self
                );
                return list.length > 0 ? list : arrayOrItemToArray(self.get('undefinedKeyObject'));
            },
            function(node) {
                // create 'values' attributes. These are the node themselves, unless a nodeValueLookup function is defined,
                // in which case we pass the node to the function it returns
                return self.nodeValueLookup ? self.nodeValueLookup(node) : node;
            },
            function(keyObject) { // stringify keys
                return keyObject.getPath(self.get('keyNameProperty'));
            });
    }.property('nodesStatus', 'nodes', 'keyProperty', 'keyObjects', 'keyObjectsStatus').cacheable(),

    observeNodes: function() {
        this.invokeNext(function() {
            this.notifyPropertyChange('tree');
        });
    }.observes('.nodes.[]'),

    /***
     * This is the flattened version of tree which is actually used by the View. It contains a list of TreeItem instances
     * that each hold the top-level instance in the keyObject. These might be Categories, Tags, etc. The nodes are the
     * second-tier instances, such as Scenarios or BuiltForms
     */
    treeItemChildren: function() {
        var self = this;
        if (this.get('tree')) {
             var items = $.map(this.get('tree'), function(entry, keyString) {
                 var values = entry.values;
                 values.sortPropertyPath(self.get('sortProperties'), self.get('reverseSortDict'));
                return Footprint.TreeItem.create({
                    nodeSet: self.get('nodeSet'),
                    keyObject: entry.key,
                    nodes: values,
                    keyNameProperty: self.get('keyNameProperty')
                });
            })
            return items.sortPropertyPath(this.get('nodeSetSortProperties'), self.get('reverseNodeSetSortDict'));
        }
        return null;
    }.property('tree').cacheable(),

    sortedNodes: function() {
        var treeItemChildren = this.get('treeItemChildren');
        if (treeItemChildren) {
            return $.shallowFlatten(treeItemChildren.map(function(treeItem) { return treeItem.get('nodes') }));
        }
        //if (this.get('arrangedObjects'))
        //    return this.get('arrangedObjects').filter(function(obj) { return !obj.instanceOf(Footprint.TreeItem)});
    }.property('treeItemChildren').cacheable(),

    toString: function() {
        return "%@:\n%@".fmt(sc_super(), this.toStringAttributes('nodeSet nodes keyProperty keyObjects keyNameProperty tree treeItemChildren'.w()));
    }
});
