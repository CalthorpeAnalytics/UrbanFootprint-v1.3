
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

sc_require('resources/jqueryExtensions');

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
    }.property('nodes')
});

/**
 * Objectifies the relationship between top level items and second level items (and possibly deeper)
 * The data structure is {key_string1: {key: top_level_instance, values: second_level_instances}, key_string2: ...} where key_string1 is a string version of the top_level_instance so that the values can be grouped under a single key.
 */
Footprint.TreeContent = SC.Object.extend({
    /***
     * Subclasses must set or bind the following properties, unless the derivitive properties are set, as described:
     */

    // The configEntity that is in scope. This will update all the controller properties whenever set or reset
    configEntity: null,
    // The configEntity property path to access the nodeSet that contains the nodes
    // Leave null if their is no set class and/or you set the nodes property directly
    keyProperty:null,
    // The property of the keyObject that access its name
    keyNameProperty:null,

    init: function() {
        sc_super();
        if (this.get('nodeSetProperty'))
            this.bind('nodeSet', '*configEntity.%@'.fmt(this.get('nodeSetProperty')));
        if (this.get('nodesProperty'))
            this.bind('nodes', '*nodeSet.%@'.fmt(this.get('nodesProperty')));
    },

    // Start the tree expanded
    treeItemIsExpanded: YES,
    // The name of the root element
    name: "root",
    // Set to the configEntity's nodeSetProperty whenever the confgEntity is updated, or can be set/bound directly instead
    nodeSet: null,

    // The nodes of the tree. Set the nodesProperty or bind nodes
    nodes:null,
    nodesStatus:null,
    nodesStatusBinding:SC.Binding.oneWay('*nodes.status'),

    /***
     * The unique key objects used by the the TreeController. These are model instances that have a string property that label the top-level tree nodes
     * These are only used to populate a select view that lets a user assign an existing key to a node.
     */
    keyObjects: null,
    keyObjectsStatus:null,
    keyObjectsStatusBinding: '*keyObjects.status',

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
     * Creates a object whose attributes are the top-level tree key names and values are the nodes with that key
     */
    tree:function() {
        var self = this;
        return $.mapToCollectionsObjectWithObjectKeys(
            (self.get('nodes') || []).toArray(),
            function(node) { // create 'keys' attributes
                var matching_keys =  $.grep(
                    arrayOrItemToArray(node.getPath(self.get('keyProperty'))),
                    function(key) {
                        // only accept the key objects that match keyObjects
                        // This allows us to filter out keyObjects of the nodes that we don't care about
                        // For instance, with Scenarios we only care about Category instances whose key property is
                        // 'category'
                        return self.get('keyObjects').contains(key);
                    });
                return (matching_keys.length > 0 ? matching_keys : [self.get('undefinedKeyObject')]).compact()
            },
            function(node) { // create 'values' attributes
                return node;
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

    toString: function() {
        return "%@:\n%@".fmt(sc_super(), this.toStringAttributes('nodeSetProperty nodeSet nodes keyProperty keyObjects keyNameProperty tree treeItemChildren'.w()));
    }
});
