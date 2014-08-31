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
     * Required. The attributes of the recordsthat should be updated or undone upon invoking undo
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
    undoAttributes: [],
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

    // Queue of postSave handlers that queue up before CRUD finishes
    _eventHandlerQueue: [],
    // Track when the CRUD saving starts and finishes. We'll queue postSave events
    // until the CRUD is finished saving
    _crudFinished:  YES,
    // The record type to match from context passed to crudDidStart and crudDidFinish
    // If not overridden in the subclass this will never match and crudDidStart, crudDidFinish
    // will not be used
    baseRecordType: null,
    // Instructs postSave methods to use the baseRecordType to find the record in the
    // store. If NO, it will used the subclass recordType passed in as context.class_name
    // We use NO for BuiltForm subclasses and other records that are saved as their subclass
    // whereas something like Scenario is treated Scenario, so we keep this value NO
    findByBaseRecordType: YES,

    /**
     * The default success message. Override to customize
     * If customized to return null, the alert will be supressed
     * @param context. The postSave context plus record and recordType
     * @returns {*}
     */
    successMessage: function(context) {
        var recordType = context.get('recordType');
        return "Successfully saved %@ records".fmt(recordType.friendlyName() || recordType.toString().split('.')[1].titleize());
    },
    /**
     * The default failure message. Override to customize
     * @param context. The postSave context plus record and recordType
     * @returns {*}
     */
    failureMessage: function(context) {
        var recordType = context.get('recordType');
        return  '%@ Save Failed'.fmt(recordType.friendlyName() || recordType.toString().split('.')[1].titleize());
    },

    /***
     * Simply returns the content.firstObject. Override for custom behavior. For instance,
     * Layers resove to their DbEntityInterest
     * @param context
     * @returns {*}
     * @private
     */
    _resolveContextRecord: function(context) {
        return context.getPath('content.firstObject');
    },
    crudDidStart: function(context) {
        if ((this._resolveContextRecord(context) || SC.Object).kindOf(this.get('baseRecordType'))) {
            this._eventHandlerQueue.clear();
            this._crudFinished = NO;
            this._crudFailed = NO;
            // Reset any records that implement the no_post_save_publishing flag
            context.get('content').forEach(function(record) {
                if (typeof(record.get('no_post_save_publishing')) != 'undefined')
                    record.setIfChanged('no_post_save_publishing', NO);
            })
            return YES;
        }
        return NO;
    },
    crudDidFinish: function(context) {
        if ((this._resolveContextRecord(context) || SC.Object).kindOf(this.get('baseRecordType'))) {
            this._crudFinished = YES;
            // Pop out handlers that queued up and run them
            while (this._eventHandlerQueue.length > 0)
                this._eventHandlerQueue.popObject().apply(this);
            return YES;
        }
        return NO;
    },

    _resolveRecord: function(context, allowNull) {
        // Either find the record by the baseRecordType or
        var record = F.store.find(
            this.get('findByBaseRecordType') ?
                this.get('baseRecordType') :
                SC.objectForPropertyPath('Footprint.%@'.fmt(context.get('class_name'))),
            context.get('id'));
        if (!record && !allowNull)
            throw Error("Could not find record of class_name %@ and id %@ in the main store".fmt(context.get('class_name'), context.get('id')));
        return record;
    },

    /***
     * Responds to the start event of a postSave publisher. If the incoming class_name matches
     * this.baseRecordType, the handler will run or be queued up if _crudFinished=NO
     * @param context
     * @returns {*}
     */
    postSavePublisherStarted: function(context) {
        // Gate keep by recordType
        var recordType = SC.objectForPropertyPath('Footprint.%@'.fmt(context.get('class_name')))
        if (!recordType.kindOf(this.get('baseRecordType'))) {
            SC.Logger.debug("Not handled");
            return NO;
        }
        SC.Logger.debug("Handled");
        if (this._crudFailed)
            // Quit if we already failed
            return;

        var eventHandler = function() {
            var record = this._resolveRecord(context);

            // Reset the progress
            record.set('progress', 0);
            SC.Logger.debug("Starting progress for recordType %@ with id %@".fmt(recordType, record.get('id')));
        };
        if (this._crudFinished)
            // Run the handler immediately if CRUD is already finished
            eventHandler.apply(this);
        else
            // Queue it up
            this._eventHandlerQueue.unshiftObject(eventHandler);
        return YES;
    },

    /***
     * Listens for postSavePublisherProportionCompleted updates from Socket IO
     * Each update sends a 'proportion' value. When this proportion hits 100% the save is
     * completed. We use proportion both to show status and because concurrent publishers
     * on the server make it impossible to know otherwise when everything is complete.
     * @param context
     * @returns {window.NO|*}
     */
    postSavePublisherProportionCompleted: function(context) {
        // Gate keep by recordType
        var recordType = SC.objectForPropertyPath('Footprint.%@'.fmt(context.get('class_name')))
        if (!recordType.kindOf(this.get('baseRecordType'))) {
            SC.Logger.debug("Not handled");
            return NO;
        }
        SC.Logger.debug("Handled portion %@ with proportion %@".fmt(
            context.get('progress_description'), context.get('proportion')));
        if (this._crudFailed)
            // Quit if we already failed
            return YES;

        var eventHandler = function() {
            var record = this._resolveRecord(context);

            // Update the progress.
            record.set('progress', Math.min(1, record.get('progress')+context.get('proportion')));
            SC.Logger.debug("Updating progress for recordType %@ with id %@, portion %@ with total progress %@".fmt(
                recordType, record.get('id'), context.get('progress_description'), record.get('progress')));

            var fullContext = SC.ObjectController.create(context, {record:record, recordType:recordType});
            // Progress is complete
            if (record.get('progress') == 1) {
                var successMessage = this.successMessage(fullContext);
                if (successMessage)
                    SC.AlertPane.info({
                        message: successMessage
                    });
                this.postSavePublishingFinished(fullContext);
            }
        };
        if (this._crudFinished)
            // Run the handler immediately if CRUD is already finished
            eventHandler.apply(this);
        else
            // Queue it up
            this._eventHandlerQueue.unshiftObject(eventHandler);
        return YES
    },


    /***
     * Handles postSave publishing failure events
     * @param context
     * @returns {window.NO|*}
     */
    postSavePublisherFailed: function(context) {
        // Gate keep by recordType
        var recordType = SC.objectForPropertyPath('Footprint.%@'.fmt(context.get('class_name')))
        if (!recordType.kindOf(this.get('baseRecordType')))
            return NO;
        var record = this._resolveRecord(context, YES);
        // Reset the progress
        record.set('progress', 0);

        var fullContext = SC.ObjectController.create(context, {record:record, recordType:recordType});
        SC.AlertPane.warn({
            message: this.failureMessage(fullContext),
            description: 'There was an error processing "%@". Please try again, and if this continues, please report to your system administrator.'.loc(context.get('key') || 'unknown')
        });
        // Let subclasses handle. We pass the record if it is available
        Footprint.statechart.sendEvent('postSavePublishingDidFail', fullContext);
        this._postSavePublisherFailed(context);
        return YES;
    },
    _postSavePublisherFailed: function(context) {
        this._crudFailed = YES;
        this._crudFinished = YES;
        // If the crud state is still savingRecords, tell it to give up
        Footprint.statechart.sendEvent('saveRecordsDidFail');
    },

    commitConflictingNestedStores: function(records) {
        // Other nestedStore locks cause SC to crash. They shouldn't but I don't know to prevent it right now
        Footprint.store.get('nestedStores').forEach(function(nestedStore) {
            if (nestedStore.locks) {
                var locks = (records.map(function(record) {
                    var lockStatus = nestedStore.locks[record.get('storeKey')];
                    return lockStatus ? [record.get('storeKey'), getStatusString(nestedStore.peekStatus(lockStatus))] : null;
                }).compact());
                if (locks.get('length') > 0) {
                    logWarning(
                        "Refreshing locked records!. A nested store has locks of the following storeKeys with the given statuses: %@".fmt(
                        locks.map(function(keyAndStatus) {
                            return [keyAndStatus[0], getStatusString(keyAndStatus[1])].join(':');
                        }).join(', ')
                    ));
                    // Commit the changes to clear the locks
                    // TODO this is not a permanent solution
                    nestedStore.commitChanges();
                }
            }
        });
    },

    /***
     * Override to do something useful after postSavePublishing completes
     * context contains the context from postSaveCompleted plus the record that was resolved
     */
    postSavePublishingFinished: function(context) {

    },
    /***
     * Override to so something useful after a postSavePublisherFailed event
     * @param context
     */
    postSavePublishingFailed: function(context) {

    },

    /***
     * Event sent when a BuildingUsePercent property changes to inform dependent records of the change.
     * For example, when a child instance precent changes, the parent needs to resum the values accordingly
     */
    buildingUsePercentPropertyDidChange: function(context) {
        var buildingUsePercent = context.get('content');

        // Find the parent BuildingUseDefinition
        var parentBuildingUseDefinition = buildingUsePercent.getPath('building_use_definition.category');
        // Get the ChildArray container
        var buildingUsePercents = buildingUsePercent.get('buildingUsePercents');
        // Find or create the parent BuildingUsePercent
        var parentBuildingUsePercent = buildingUsePercent.getPath('parentBuildingUsePercent');
        if (!parentBuildingUsePercent) {
            // Create the parent if it doesn't exist
            parentBuildingUsePercent = buildingUsePercents.createNestedRecord(
                Footprint.BuildingUsePercent,
                {
                    building_use_definition: parentBuildingUseDefinition.get('id'),
                    building_attribute_set: buildingUsePercents.getPath('parentRecord.id'),
                    efficiency: 0,
                    square_feet_per_unit: 0
                });
        }
        // Set the parentBuildingUsePercent.percent to the sum of the children
        parentBuildingUsePercent.setIfChanged('percent',
            parseFloat(buildingUsePercent.get('buildingUsePercents').filter(function(buildingUsePercent) {
                // Filter for children
                return buildingUsePercent.getPath('building_use_definition.category')==parentBuildingUseDefinition;
            }).reduce(function(percentTotal, buildingUsePercent) {
                // Sum percents
                return buildingUsePercent.get('percent') + percentTotal;
            }, 0).toFixed(2))
        );

        // Set the parentBuildingUsePercent.total_far to the sum of each children's percent*totalFar
        var totalFar = buildingUsePercents.getPath('parentRecord.total_far');
        parentBuildingUsePercent.setIfChanged('floor_area_ratio',
            parseFloat(buildingUsePercent.get('buildingUsePercents').filter(function(buildingUsePercent) {
                // Filter for children
                return buildingUsePercent.getPath('building_use_definition.category')==parentBuildingUseDefinition;
            }).reduce(function(percentTotal, buildingUsePercent) {
                // Sum percents
                return buildingUsePercent.get('percent')*totalFar + percentTotal;
            }, 0).toFixed(2))
        );

    },


    initialSubstate: 'readyState',
    readyState: SC.State,

    enterState: function(context) {
        // Don't set _context here since some subclasses need to customize their context
        // Create the undoManager if it doesn't yet exist
//        if (!this._content)
//            throw Error("Subclass %@ enterState must set the this._content".fmt(this.get('fullPath')));
        if (!this.get('undoManager'))
            this.initializeUndoManager();
    },

    exitState: function() {
        this._content = null;
        this._context = null;
    },

    /***
     * For simpler record type saves that don't need CrudState.SavingRecords state.
     * TODO The two ways of saving should be coallesced
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

    /***
    * For simpler record type saves that don't need CrudState.SavingRecords state.
    * TODO The two ways of saving should be coallesced
    * Undo has a different context but is otherwise the same as update but it doesn't register an undo
    */
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
     * Creates a context for freezing a painting context of the current record or record set for undo/redo
     */
    undoContext: function(otherContext) {
        return SC.ObjectController.create({
            // The undoManager needs to be specified for setting redo (I think)
            undoManager: this.get('undoManager'),
            // The Feature recordType
            recordType: this._context.get('recordType'),
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
     * @param otherContext - context dict to apply to the outer context to pass non-record info. if this
     * contains 'content' that is assume to be the records or records that are modified. Otherwise
     * this._content is used
     */
    createModifyContext: function(recordsContext, otherContext) {
        var content = (otherContext && otherContext.content) ? arrayOrItemToArray(otherContext.content) : this._content;
        return SC.ObjectController.create({
            // The undoManager for records of the active layer selection
            undoManager: this.get('undoManager'),
            // The same structure as this object but used to undo the records back to their previous state
            undoContext: this.undoContext(otherContext),
            // The Feature recordType
            recordType: this._context.get('recordType'),
            // An array of each records to be updated along with the values to update (context)
            // The resulting object is {record:record, attributeToUpdate:value, attributeToUpdate:value, ...}
            recordContexts:arrayOrItemToArray(content).map(function(record) {
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