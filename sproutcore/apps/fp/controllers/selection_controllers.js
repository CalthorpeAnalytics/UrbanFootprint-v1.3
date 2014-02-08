
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

sc_require('controllers/controllers');

Footprint.ActiveController = SC.ObjectController.extend({

    init: function() {
        sc_super();
        // We require from to be set right-off-the bat to avoid problems. We'd have to get rid of this if from were ever bound
        if (!this.get('listController'))
            throw "'listController' property is null or undefined. Perhaps it wasn't sc_required or was declared below this definition";
    },
    /***
     * Bind to the singleSelection property of the the listController. When the selection changes we update
     * our content
     */
    contentBinding: SC.Binding.from('.listController*selection.firstObject'),

    observeControllerProperty:null,

    /***
     * An ArrayController or TreeController that has a selection to which we should two-way bind
     */
    listController:null,

    /***
     * Determines when the initialContentObserver should fire
     * For listControllers, like TreeControllers that can't delegate their status to anything,
     * optionally a custom status that determines when to trigger the initialContentObserver
     */
    listStatus:function() {
        return this.getPath('listController.status');
    }.property('listController'),

    /***
     * This sets it to the first item of listController.selection or failing that the
     * first item of listController or list. If content is bound this setting will quickly be undone
     *
     */
    initialContentObserver:function() {
        if (this.get('listStatus') & SC.Record.READY)
            this.set('content', this.firstItemOfSelectionSetOrFirstItemOfList());
    }.observes('*listController.status'),


    /***
     * Since our controllers currently only support one active item, take the first item of the selection set, or
     * the first item of the list if nothing is selected
     * @returns {*|Object|Object|Object|Object}
     */
    firstItemOfSelectionSetOrFirstItemOfList: function() {
        return this.getPath('listController.selection').length() > 0 ?
            this.getPath('listController.selection.firstObject') :
            this.firstItem()
    },
    /***
     * The first item of the listController if nothing is selected. Override this for TreeControllers, etc
     * @returns {*|Object|Object|Object|Object}
     */
    firstItem: function() {
        return this.getPath('listController.firstObject');
    },


    toString: function() {
        return this.toStringAttributes('content listController listStatus'.w());
    }

});

Footprint.TreeSelectionController = Footprint.ActiveController.extend({
    /***
     * Specifies how to fetch the first node of the TreeController items
     * @returns {*}
     */
    firstItem: function() {
        return this.getPath('listController.nodes.firstObject');
    }
});

