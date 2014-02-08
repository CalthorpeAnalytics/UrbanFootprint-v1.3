/**
 * Created by calthorpe on 12/15/13.
 */

Footprint.RecordsAreReadyState = SC.State.extend({

    /***
     * Required. The event to invoke when the record(s) successfully update
     */
    recordsDidUpdateEvent: null,

    /***
     * Required. The event to invoke when the records(s) fail to update
     */
    recordsDidFailToUpdateEvent: null,

    /***
     * Required. The action to invoke upon undo to distinguish this state from others
     */
    undoAction: null,
    /***
     * Required. The attributes of the features that should be updated or undone upon invoking undo
     * TODO This could default to all attributes for simple record types
     */
    updateAttributes: null,

    /***
    * The undoManager for the instance(s) being updated. Use the Container and Property
    * or the undo
    */
    undoManagerProperty: null,
    /***
     * Use the controller with undoManagerProperty for collection undo (like for Features)
     */
    undoManagerController: null,
    /***
     * Get the initialized undoManager for the current item or collection
     * @returns {*}
     */
    undoManager: function() {
        var property = this.get('undoManagerProperty');
        var controller = this.get('undoManagerController');
        if (controller && property) {
            return controller.getPath(property);
        }
        else if (property) {
            // TODO stupidly assuming single _content for now
            return this._content.getPath(property);
        }
    }.property(),

    /***
     *
     * Initialize the undoManager for Scenario collection and individuals
     */
    initializeUndoManager: function() {
        var property = this.get('undoManagerProperty');
        var controller = this.get('undoManagerController');

        // For collection-scoped undo use the (e.g. a controller) and the undoManagerProperty (e.g. 'undoManager')
        if (controller && property) {
            if (!controller.getPath(property)) {
                controller.setPath(this.get('undoManagerProperty'), SC.UndoManager.create());
                //controller.get('content')[this.get('undoManagerProperty')] = SC.UndoManager.create();
            }
        }
        // For item scoped undo iterate through the items
        else if (property) {
            arrayOrItemToArray(this._content).forEach(function(content) {
                if (!content.getPath(property)) {
                    content.setPath(property, SC.UndoManager.create());
                    //content[property] = SC.UndoManager.create();
                }
            });
        }
    },

    /***
     * Returns the context to update the records(s). This is a list of SC.ObjectController that points
     * to the record along with a key/values of attributes and their target update value. The context
     * is the incoming context of the state, which can be used to create the updateContext
     */
    updateContext: function(context) {
        throw Error("No updateContext override for substate %@".fmt(this.get('fullPath')))
    },
    /***
     * The attributes to undo during and undo action. This determines what current attributes to store when
     * building and undoContext
     */
    undoAttributes: null,
    /***
     *
     * Like updateContext but clears the attributes, if available
     */
    clearContext: function(context) {
        throw Error("No clearContext override for substate %@".fmt(this.get('fullPath')))
    },

    /***
     * The attribute to cancel any update in progress, used when new updates come in during saving
     */
    cancelAction: null,

    /***
     * Method to submit the record(s) with updated values
     */
    updateRecords: function(context) {
        this.gotoState('%@.updatingState'.fmt(this.get('fullPath')), this.updateContext(context));
    },

    /***
     * Method to submit the record(s) with cleared values
     */
    clearRecords: function() {
        var context = this._context || SC.ObjectController.create({content:this._content});
        this.gotoState('%@.updatingState'.fmt(this.get('fullPath')), this.clearContext(context));
    },

    doRecordUndo: function(context) {
        this.get('undoManager').undo();
    },
    doRecordRedo: function(context) {
        this.get('undoManager').redo();
    },

    /***
     * If a record update fails this handles the event.
     * @param context. This could be used to report what records failed
     */
    updateDidFail: function(context) {
        // Simply return to the start of this state
        this.gotoState(this.get('fullPath'), this._context);
    },

    initialSubstate: 'readyState',
    readyState: SC.State,

    enterState: function(context) {
        // Don't set _context here since some subclasses need to customize their context
        // Create the undoManager if it doesn't yet exist
        if (!this._content)
            throw Error("Subclass %@ enterState must set the this._content".fmt(this.get('fullPath')));
        if (!this.get('undoManager'))
            this.initializeUndoManager();
    },

    exitState: function() {
        this._context = null;
    },

    /***
     * Updates the records. recordsDidUpdate is currently overridden to do doClearSelection upon completion
     */
    updatingState: Footprint.RecordUpdatingState.extend({
        undoActionBinding: SC.Binding.oneWay('.parentState.undoAction'),
        updateActionBinding: SC.Binding.oneWay('.parentState.updateAction'),
        recordsDidUpdateEventBinding: SC.Binding.oneWay('.parentState.recordsDidUpdateEvent'),
        recordsDidFailToUpdateEventBinding: SC.Binding.oneWay('.parentState.recordsDidFailToUpdateEvent'),
        recordsDidUpdate:function() {
            // Do the default stuff
            sc_super();
        }
    }),

    // Undo has a different context but is otherwise the same as update but it doesn't register an undo
    undoingState:Footprint.RecordUpdatingState.extend({
        init: function() {
            sc_super()
            // Add update actions handlers to this state instance so we can cancel updating if an action comes in.
            if (this.getPath('parentState.updateActions')) {
                this.getPath('parentState.updateActions').forEach(function(updateAction) {
                    this[updateAction] = function(context) {
                        this.cancelUpdate();
                        return NO;
                    }
                });
            }
        },
        undoActionBinding: SC.Binding.oneWay('.parentState.undoAction'),
        updateActionBinding: SC.Binding.oneWay('.parentState.updateAction'),
        recordsDidUpdateEventBinding: SC.Binding.oneWay('.parentState.recordsDidUpdateEvent'),
        recordsDidFailToUpdateEventBinding: SC.Binding.oneWay('.parentState.recordsDidFailToUpdateEvent'),
        recordsDidUpdate:function() {
            // Skip sc_super() so we don't register an undo
        }
    }),

    /***
     * Creates a context for freezing a painting context of the current feature set for undo/redo
     */
    undoContext: function(otherContext) {
        return SC.ObjectController.create({
            // The undoManager needs to be specified for setting redo (I think)
            undoManager: this.get('undoManager'),
            // The Feature recordType
            recordType: this.get('recordType'),
            // An array of each record to be undone along with the values to undo to (context)
            // The resulting objects are {record:record, attributeToUpdate:value, attributeToUpdate:value, ...}
            recordContexts: arrayOrItemToArray(this._content).map(function(record) {
                return SC.ObjectController.create(
                    {record:record},
                    // extract the primitive attributes from the record to be target attribute values for undoing
                    $.mapToDictionary(this.get('undoAttributes'), function(attr) {
                        return [attr, record.get(attr)];
                    })
                )
            }, this)
        },
        otherContext || {});
    },

    /***
     * Creates forward modification contexts (not undoing contexts)
     * @param recordsContext - context dict to apply to all records for blanket updates
     * @param otherContext - context dict to apply to the outer context to pass non-record info
     */
    createModifyContext: function(recordsContext, otherContext) {
        return SC.ObjectController.create({
            // The undoManager for features of the active layer selection
            undoManager: this.get('undoManager'),
            // The same structure as this object but used to undo the features back to their previous state
            undoContext: this.undoContext(otherContext),
            // The Feature recordType
            recordType: this._context.get('recordType'),
            // An array of each feature to be updated along with the values to update (context)
            // The resulting object is {feature:feature, attributeToUpdate:value, attributeToUpdate:value, ...}
            recordContexts:arrayOrItemToArray(this._content).map(function(record) {
                return SC.ObjectController.create({
                        record:record
                    },
                    recordsContext
                )
            })
        },
        otherContext || {});
    }
});