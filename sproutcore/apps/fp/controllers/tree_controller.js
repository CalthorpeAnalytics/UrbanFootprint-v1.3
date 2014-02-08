
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

sc_require('controllers/controllers');

 /***
  * Specialized TreeController that takes a Footprint.TreeContent for its ontent
  * @type {Class}
  */
Footprint.TreeController = SC.TreeController.extend(Footprint.SingleSelectionSupport, SC.CollectionViewDelegate, {
    treeItemIsGrouped: YES,
    allowsMultipleSelection: NO,
    allowsEmptySelection: NO,

    // Delegate the status to the nodes property of the content to get a status
    // The status is used by Footprint.SelectController to know they can assign their content to the selected item
    // or else first item of the nodes list
    statusBinding:SC.Binding.oneWay('*nodes.status'),

    /***
     * Returns the record type
     */
    recordType: function() {
        return this.getPath('nodes.firstObject.constructor');
    }.property('.nodes'),

	// ..........................................................
	// DRAG SOURCE SUPPORT
	//

	/**
		When dragging, add Task data type to the drag.
	*/
	/*collectionViewDragDataTypes: function(view) {
		return [this.get('recordType'), Footprint.TreeItem];
	},*/

	/**
		If the requested dataType is a Task, provide the currently selected tasks.	Otherwise return null.
	*/
/*	collectionViewDragDataForType: function(view, drag, dataType) {
		var ret=null, sel;
        *//*
		if (dataType === CoreTasks.Task) {
			sel = view.get('selection');
			ret = [];
			if (sel) sel.forEach(function(x) { ret.push(x); }, this);
		}
		*//*
		return ret;
	},*/

	// ..........................................................
	// DROP TARGET SUPPORT
	//
	/*collectionViewComputeDragOperations: function(view, drag, proposedDragOperations) {
        // TODO implement drag support fully
        return SC.DRAG_NONE;
		if (drag.hasDataType(this.get('recordType'))) {
			return SC.DRAG_MOVE;
		}
        if (drag.hasDataType(Footprint.TreeItem)) {
            return SC.DRAG_MOVE;
        }
		else {
			return SC.DRAG_NONE;
		}
	},*/

	/**
		Called if the user actually drops on the view.	Since we are dragging to and from
		the same view, let the CollectionView handle the actual reorder by returning SC.DRAG_NONE.
		If the drop target is the first index (before the unassign branch) do nothing by returning
		SC.DRAG_MOVE.
	*/
	/*collectionViewPerformDragOperation: function(view, drag, dragOp, idx, dropOp) {

		var ret = SC.DRAG_MOVE;

		// tells the CollectionView to do nothing
		if (idx < 0)
            return ret;

		// Extract tasks to drag
		var records = drag.dataForType(this.get('recordType'));
		if(!records)
            return ret;

		// Get assignee of item before drop location
		var content = view.get('content');
		var targetAssignee = content.objectAt(idx).get('assignee');

		// Set dragged records' assignee to new assignee
		records.forEach(function(record) {
			if (record.get('assignee') !== targetAssignee) {
				var targetAssigneeId = targetAssignee === null ?
                    null :
                    targetAssignee.get('id');
				console.log('Reassigning record "' + record.get('name') + '" to: ' + (targetAssignee? targetAssignee.get('name') : 'Unassigned'));
				record.set('assigneeId', targetAssigneeId);
				ret = SC.DRAG_NONE;
			}
		}, this);

		if (ret === SC.DRAG_NONE) {
            // Save changes here. Saving ordering will probably be related to the user's database data
		}

		return ret;
	},*/

	/**
		Called by the collection view to delete the selected items.

		@param {SC.CollectionView} view collection view
		@param {SC.IndexSet} indexes the items to delete
		@returns {Boolean} YES if the deletion was a success.
	*/
/*	collectionViewDeleteContent: function(view, content, indexes) {
		if (content && (SC.typeOf(content.destroyAt) === SC.T_FUNCTION || SC.typeOf(content.removeAt) === SC.T_FUNCTION)) {
            // Do the remove
			return YES;
		}
		return NO;
	},*/

	toString: function() {
	    return this.toStringAttributes('content'.w());
	}
});
