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

sc_require('states/loading_records_state');

Footprint.CrudState = SC.State.extend({

    // -----------------------
    // Always-available actions.
    //

    /***
     * @param context. Context contains:
     *  recordType: Required. The kind of record to view/edit
     *  activeRecord: Optional. The record to edit or clone. Set null to create a record from scratch
     *  content: Optional. Used for the activeRecord if activeRecord undefined. If activeRecord is simply null
     *  then null will be used, assuming a creation case
     *  nowShowing: Optional. Default 'Footprint.FeatureSummaryInfoView'. The view to show of the tabbed
     *  views in the modal window
     *  Note that showing the modal has nothing to do with whether or not the content is ready.
     *  There are times when we want to show the modal while the content loads.
     *  // TODO rename activeRecord to content throughout
     */
    doShowModal: function(context) {
        // Resolve the infoView to use with the following three alternatives
        var infoPaneStringOrView = context && context.get('infoPane');
        if (infoPaneStringOrView) {
            var recordType = context.get('recordType');
            var infoPaneViewClass = typeof(infoPaneStringOrView) == 'string' ? SC.objectForPropertyPath(infoPaneStringOrView) : infoPaneStringOrView;
            if (!infoPaneViewClass) {
                throw Error("infoPane was not set or configured for recordType %@".fmt(recordType));
            }
            var createdInfoPane;
            var infoPaneGuid = SC.guidFor(infoPaneViewClass);
            if (this._infoPane && this._infoPane.constructor == infoPaneViewClass) {
                // infoPane is already set to the same type, just update the context
                this._infoPane.set('context', context);
                this._infoPane.append();
            }
            else if (this._infoPaneCache && this._infoPaneCache[infoPaneGuid]) {
                // infoPane is a different record type but that type has been cached
                if (this._infoPane.get('isPaneAttached')) {
                    // It should already be removed
                    logWarning("Previous infoPane %@ was not removed properly".fmt(this._infoPane.constructor));
                    this._infoPane.remove();
                }
                this._infoPane = this._infoPaneCache[infoPaneGuid];
                this._infoPane.set('context', context);
                createdInfoPane = this._infoPane;
                if (!createdInfoPane.get('isPaneAttached'))
                    createdInfoPane.append();
            }
            else {
                // infoPane is a different record type and that type has not been cached
                createdInfoPane = infoPaneViewClass.create({
                    recordType:recordType,
                    context:context
                });
                // Display it
                createdInfoPane.append();
                // Remember it for reenter and exit
                this._infoPane = createdInfoPane;
                // Cache the creation
                this._infoPaneCache = this._infoPaneCache || {};
                this._infoPaneCache[infoPaneGuid] = this._infoPane;
            }
        }
    },
    doHideModal: function(context) {
        if (this._infoPane) {
            this._infoPane.remove();
        }
    },

    /***
     * A bit of a hack to clear the filter property when selecting unless the modal is updating
     */
    doClearFilterUnlessModal: function() {
        Footprint.statechart.sendAction('doClearFilter');
        Footprint.statechart.sendAction('doClearJoins');
        Footprint.statechart.sendAction('doClearAggregates');
        Footprint.statechart.sendAction('doClearGroupBy');
    },

    /***
     * Handles a selection being made from a selection panel
     */
    doPickSelection: function(context) {
        // this.invokeLater(function() {
        //     context.getPath('parentView.parentView.parentView').remove()
        // })
    },

    /***
     * Exports modal table content as CSV
     * @param context
     */
    doExport: function(context) {
        if (context.get('isLocalExport')) {
            var csv = context.get('content').map(function (row) {
                return row.join(',')
            }).join('\r\n');
            window.open("data:text/csv;charset=utf-8," +
                '<meta name="content-type" content="text/csv">' +
                '<meta name="content-disposition" content="attachment;  filename=data.csv">' +
                escape(csv))
        }
        else {
            // TODO
        }
    },

    /***
     * Converts modal table content to CSV and presents it in a window for copying
     * @param context
     */
    doCopy: function(context) {
        var csv = context.get('content').map(function (row) {
            return row.join(',')
        }).join('\n');
        Footprint.clip.setText(csv);
    },

    /*********************************************
     *
     * The CRUD actions.
     * These are triggered whether the modal is open or not. They route through the
     * generic doProcessRecord action, which opens the modal if needed.
     *
     */

    /***
     * Create a brand spankin' new record with minimum attributes copied from the context.
     * @param context - context.activeRecord is the is the context that is minimally copied
     */
    doCreateRecord:function(context) {
        // view objects don't like to get passed to the ArrayController, so filter for the key we want
        var safeContext = filter_keys(context, ['infoPane', 'recordsEditController', 'recordType', 'content']);
        var pluralContext = toArrayController(this._context || {}, safeContext, {crudType:'create'});
        this.statechart.sendAction('doProcessRecord', pluralContext);
    },

    /***
     * Create a new record by cloning the record in the context
     * @param context - context.activeRecord is cloned
     */
    doCloneRecord:function(context) {
        // We always deal with adding records one at a time, but the context.content
        // will either be singular or a single-item array, since some of the saving_crud_state
        // stuff always turns content into an array for simplicity.

        // view objects don't like to get passed to the ArrayController, so filter for the key we want
        var safeContext = filter_keys(context, ['infoPane', 'recordsEditController', 'recordType', 'content']);
        var pluralizeContext = toArrayController(this._context || {}, safeContext, {crudType:'clone'});
        this.statechart.sendAction('doProcessRecord', pluralizeContext);
    },

    /***
     * Update the record in the context.
     * @param context - context.activeRecord is used for the editing states
     */
    doUpdateRecord:function(context) {
        var pluralizeContext = toArrayController(this._context || {}, context, {crudType:'update'});
        this.statechart.sendAction('doProcessRecord', pluralizeContext);
    },

    /***
     * View the record in the context
     * TODO use the regular edit state unless we need a different state for read-only
     * @param context - context.activeRecord is the selected record
     */
    doViewRecord:function(context) {
        var pluralizeContext = toArrayController(this._context || {}, context, {crudType:'view'});
        this.statechart.sendAction('doProcessRecord', pluralizeContext);
    },

    /***
     * Query based on the recordType in the context
     * @param context - context.recordType is the type of record used for the querying states
     */
    doQueryRecords: function(context) {
        var singularContext = toArrayController(context);
        this.statechart.sendAction('doProcessRecord', singularContext);
    },

    /***
     * This action is sent by the doFooRecord(s) actions above. If this method handles the
     * action, it goes to the modal state and pops open the modal. If we're already in the
     * modal state, it will handle it instead.
     */
    doProcessRecord: function(context) {
        this.gotoState('modalState', context);
    },

    // -----------------------------------
    // Substates
    // 

    initialSubstate: 'noModalState',

    noModalState: SC.State,

    modalState: SC.State.extend({

        // ---------------------
        // Actions & Events
        //

        /***
         * Called by one of the CRUD actions. This handler will be called when we are already in the modal.
         * It might respond to a clone, create or create action, so it sends us to the prepareContentState
         * so that we are ready to perform those actions.
         * @param context
         */
        doProcessRecord: function(context) {
            var recordType = this.getPath('_context.recordType');
            // For modal info panes we don't have to worry about a new recordType coming through. That will only
            // happen if it changes from an action on that modal (e.g. BuiltForm subclasses). For non-modals,
            // we simply exit the state and re-enter with the new recordType, assuming that the non-modal will
            // preserve its state upon reopening.
            if (recordType && recordType !== context.get('recordType')) {
                if (this.parentState._infoPane.getPath('closeForNewModalPane')) {
                    this.gotoState('modalState', context);
                    return;
                }
                else {
                    // Switching recordTypes within a modal. Reset the _recordsEditController
                    this.initializeController(context);
                }
            }
            // Respond to the passed in content and crudType by preparing a clone, new record, etc.
            Footprint.statechart.gotoState('prepareContentState', context);
        },

        /***
         * Responds to an edit controller changing selection.
         * If that controller, the context, matches this _recordsEditController
         * change to the new selection
         * @param context
         */
        selectedRecordChangeObserved: function(context) {
            // Make sure this is our recordEditController changing
            if (SC.Set.create(context.getPath('selection')).isEqual(SC.Set.create(this._context.get('content'))))
                return;

            var content = this._recordsEditController.getPath('selection').toArray();
            Footprint.statechart.sendEvent('selectedRecordDidChange', toArrayController(this._context, {content:content}));
        },
        /***
         * Separate the event out in-case we need to disable calling prepareContenxtState during a save.
         * This problem is acute when deleting a record. Going to parepareContentState disrupts the save (delete) process.
         * @param context
         */
        selectedRecordDidChange: function(context) {
            Footprint.statechart.gotoState('prepareContentState', context);
        },

        /***
         * Close the modal, clearing any changes without saving them.
         * This is here and not in showingModalState in case the user has to close during a saingRecordState
         */
        doPromptCancel: function(context) {
            var postConfirmAction = (context && context.get('postConfirmAction')) || 'doCancel';

            // If all records in the controller are new or clean, just delete without a prompt
            var nestedStore = this._recordsEditController.get('nestedStore');
            var unclean_statuses = [SC.Record.READY_NEW, SC.Record.READY_DIRTY];
            var newOrDirtyRecords = this._recordsEditController.map(function(record) {
                var storeKey = record.get('storeKey');
                var status = nestedStore.peekStatus(storeKey);
                return unclean_statuses.contains(status) ? nestedStore.materializeRecord(storeKey) : null;
            }, this).compact();
            // No changes, proceed
            if (newOrDirtyRecords.get('length') == 0) {
                Footprint.statechart.sendAction(postConfirmAction, toArrayController(context, {confirm:YES}));
                return;
            }

            SC.AlertPane.warn({
                message: "You are about cancel with the following item%@ edited but not saved: %@. Changes will be discarded.".fmt(
                    newOrDirtyRecords.get('length') > 1 ? 's' : '', // TODO auto-pluralize
                    newOrDirtyRecords.mapProperty('name').join(', ')
                ),
                description: "",
                caption: "",
                confirm:YES, // Used by the action
                buttons: [
                    { title: "Keep Open" },
                    { title: "Don't Save", action:postConfirmAction }
                ]
            });
        },
        doCancel: function() {
            this.gotoState('noModalState');
        },

        // ---------------------
        // Substates
        //

        initialSubstate: 'initialState',
        initialState: SC.State,

        enterState: function(context) {
            this._nestedStore = Footprint.store.chainAutonomousStore();
            // Setup the recordsEditController. This is called whenever the recordType/recordsEditController changes,
            // not just on enterState
            this.initializeController(context);
            Footprint.statechart.sendAction('doShowModal', context);
            // Process the content. This will send us to the prepareContentState
            this.doProcessRecord(context);
        },

        exitState: function() {

            if (this._recordsEditController) {
                // Stop observing the selection
                this._recordsEditController.removeObserver('selection', this, 'selectedRecordChangeObserved');

                // Deselect all objects in case we are selected records that will be removed
                // The controller should be wired up to reselect the selection of the source controller.
                this._recordsEditController.deselectObjects(this._recordsEditController.get('selection'));

                // Clear the nested store.
                this._recordsEditController.set('nestedStore', null);
            }

            // Remove the nestedStore reference from the dependencyRecordsEditController if it exists
            var dependencyRecordsEditController = this._context.getPath('dependencyContext.recordsEditController');
            if (dependencyRecordsEditController)
                dependencyRecordsEditController.set('nestedStore', null);

            // Discard changes
            if (this._nestedStore && !this._nestedStore.get('isDestroyed'))
                this._nestedStore.destroy();
            this._nestedStore = null;

            // Cleanup
            this._recordsEditController = null;
            this._context = null;
            Footprint.statechart.sendAction('doHideModal');
        },

        initializeController: function(context) {

            // If a different recordsEditController was previously used for a different recordType,
            // stop observing its selection
            if (this._recordsEditController)
                this._recordsEditController.removeObserver('selection', this, 'selectedRecordChangeObserved');

            this._recordsEditController = context.get('recordsEditController');
            // Set the nestedStore of the controller. This updates its content query
            // to a new query with this nestedStore
            this._recordsEditController.set('nestedStore', this._nestedStore);
            // For recordTypes that have a dependencyContext, initialize the dependency recordsEditController too
            var dependencyRecordsEditController = context.getPath('dependencyContext.recordsEditController');
            if (dependencyRecordsEditController)
                dependencyRecordsEditController.set('nestedStore', this._nestedStore)

            // Observe changes to the selection so we can reset the content
            this._recordsEditController.addObserver('selection', this, 'selectedRecordChangeObserved');
        },


        /***
         * In the case of cloning a record, we need to prepare for cloning
         * by making sure that all toOne and toMany attributes are fully loaded.
         * TODO. This isn't recursive yet but needs to be. I needs to load all
         * toOne and toMany records, then upon loading to call itself to load
         * all the toOne/toMany records of those loaded records. That
         * functionality should probably be encapuslated in LoadingRecordsState,
         * which can prevent infinite loops.
         */
        prepareContentState: SC.State.extend({

            initialSubstate: 'initialState',
            initialState: SC.State,

            enterState: function(context) {
                this._context = context;
                this._nestedStore = this.getPath('parentState._nestedStore');
                this.prepareContent(context);
            },

            exitState: function() {
                this._context = null;
                this._nestedStore = null;
            },

            /***
             * Loads all child records that need to be fully loaded prior to cloning. Once complete
             * the top-level record is cloned.
             */
            cloningRecordsState: Footprint.LoadingRecordsState.extend({

                enterState: function(context) {
                    this._nestedStore = this.getPath('parentState._nestedStore');
                    sc_super();
                },

                didLoadRecords: function(context) {
                    // Get the nested version of the content even if its already nested
                    // Non-nested would be adding from the main interface, nested would be
                    // adding from the modal interface that has a list of nested store records
                    // The list is likely using a separate nestedStore
                    if (context.getPath('length') != 1)
                    // TODO we can support cloning multiple items if useful
                        throw Error("Trying to clone from non singular context");
                    var nestedSourceContent = this._nestedStore.materializeRecord(context.getPath('firstObject.storeKey'));
                    // Do the clone
                    var content = nestedSourceContent.cloneRecord(context.get('firstObject'));
                    Footprint.statechart.gotoState('modalReadyState', toArrayController(context, {content:content}));
                }
            }),

            /***
             * Handles local create or clone of a record and returns edit or the record target for update/view
             * @param context
             * @returns the content as an array
             */
            prepareContent: function(context) {

                // If we are not re-entering this state after a successful save or failure, set up the nested store
                // and clone the record
                var content;

                // The passed in or selected item. This might be the source record of a clone
                // or the record to be updated or deleted.
                // It might also be a cloned/created item when we're returning here by clicking
                // on a new item in the list
                var recordsEditController = context.get('recordsEditController');
                var sourceContextController = toArrayController(context, {content:
                // Set to passed in content if defined
                    context.get('content') ||
                        // Otherwise to the full selection or full content list
                        (recordsEditController.getPath('selection.length') > 0 ?
                            recordsEditController.get('selection').toArray() : // toArray to force ordering
                            // Default to all for stuff like features
                            recordsEditController.get('content'))
                });

                // Get the content array status or individual record status
                if (!sourceContextController.get('status') || sourceContextController.get('status') !== SC.Record.READY_NEW) {
                    if (context.get('crudType') === 'create') {
                        // Create a record from scratch, not clone
                        content = [this._nestedStore.createRecord(context.get('recordType'), {}, Footprint.Record.generateId())];
                        // Use the record type's _createSetup function to copy over
                        // minimum values, like a config_entity's parent_config_entity
                        // The seed record must be a complete record, not a new one
                        var seedRecord;
                        for(var i=0; i<recordsEditController.length(); i++) {
                            var record = recordsEditController.objectAt(i)
                            if (record.get('id') > 0) {
                                seedRecord = record;
                                break;
                            }
                        }
                        if (!seedRecord) {
                            throw Error("Cannot create a new record without any existing record as a template")
                        }
                        content.forEach(function(record) {
                            record._createSetup(seedRecord);
                        }, this);
                        Footprint.statechart.gotoState('modalReadyState', toArrayController(sourceContextController, {content:content}));
                    }
                    else if (context.get('crudType') === 'clone') {
                        Footprint.statechart.gotoState('cloningRecordsState', sourceContextController);
                    }
                    else {
                        // For all other cases of non-new sourceContent
                        // This can be one or more items in an array
                        Footprint.statechart.gotoState('modalReadyState', sourceContextController);
                    }
                }
                else {
                    // If we have content that is a new record then being here means
                    // that we are reentering this state.
                    // This is also the update/view/delete case of existing records
                    Footprint.statechart.gotoState('modalReadyState', sourceContextController);
                }
            }
        }),

        /***
         * Called as a method by enterState, and triggered as an action by CrudState's
         * CRUD actions (see above).
         */
        // All modal actions (e.g. closing the modal) can only be taken from the
        // ready state. Once in the saving state, the user is blocked from taking
        // actions until the save action completes or fails.
        modalReadyState: SC.State.extend({
            /***
             * Delete the selected record
             * @param context
             */
            doPromptDeleteRecord:function(context) {
                var pluralizedContext = toArrayController(
                    this.parentState._context,
                    {content:context.get('content'), crudType:'delete'});

                if (pluralizedContext.filter(function(record) {
                    return record.get('status') !== SC.Record.READY_NEW;
                }, this).get('length') == 0) {
                    this.doDeleteRecord(context);
                    return;
                }

                SC.AlertPane.warn({
                    message: "You are about to remove the following item%@: %@. All data will remain intact on the server.".fmt(
                        pluralizedContext.get('length') > 1 ? 's' : '', // TODO auto-pluralize
                        pluralizedContext.mapProperty('name').join(', ')
                    ),
                    description: "",
                    caption: "",
                    content: pluralizedContext.get('content'),
                    buttons: [
                        { title: "Cancel" },
                        { title: "Proceed", action:'doDeleteRecord' }
                    ]
                });
            },
            doDeleteRecord: function(context) {
                var pluralizedContext = toArrayController(
                    this.parentState._context || {},
                    {content:context.get('content'), crudType:'delete'});
                // Set the deleted property on the record.
                pluralizedContext.forEach(function(record) {
                    record._deleteSetup();
                });
                // If these are all new records just return. They are delete from view
                // and will be discarded when the state exits.
                if (pluralizedContext.filter(function(record) {
                    return record.get('status') !== SC.Record.READY_NEW;
                }, this).get('length') == 0) {
                    // Tell the recordsEditController to update its content
                    // For some reason its local query can't pick up the record.delete flag being set
                    this.parentState._recordsEditController.propertyDidChange('content');
                    return;
                }

                // Deselect all objects in case we are selected records that will be removed
                // The controller should be wired up to reselect the selection of the source controller
                // Remove created records (that weren't saved)
                // Find the minimum selection index to reselect the adjacent object after
                var selection = this.parentState._recordsEditController.get('selection');
                if (selection) {
                    var selIndexes = selection.indexSetForSource(context.get('content'));
                    this._index = selIndexes ? selIndexes.min : 0;
                }
                Footprint.statechart.sendAction('doSave', pluralizedContext);
            },
            /***
             * Pack up our things and go to the save state.
             **/
            doSave: function(context) {
                // Use the content already in the _context unless context passes a new on in. This would
                // only be the case for an inline delete button or similar that operates on a single record
                // and saves immediately. Normally a save all button will be hit, which meens no content passed in.
                var pluralizedContext = toArrayController(
                    this.parentState._context,
                    context.get('content') ? {content:context.get('content')} : {});
                this.gotoState(this.parentState.savingRecordState, pluralizedContext);
            },
            enterState: function(context) {

                // Create the complete context. This will get passed around with the content overridden sometimes
                // when different content is the target of an action
                this._context = SC.ArrayController.create({
                    content: context.get('content'),
                    nestedStore: this.getPath('parentState._nestedStore'),
                    recordType:context.get('recordType'),
                    recordsEditController:context.get('recordsEditController')
                });
                // Set the complete context up the line
                this.setPath('parentState._context', this._context);
                this.setPath('parentState.parentState._context', this._context);

                // Select content on the next run loop
                if (context.get('content'))
                    this.invokeNext(this.selectContent);
            },
            selectContent: function() {
                this._context.get('recordsEditController').selectObjects(this._context.get('content'));
            }
        }),

        savingRecordState: SC.State.plugin('Footprint.SavingRecordState', {
            // -------------------------
            // Save Events
            //

            /***
             * Override the parent's event handler to ignore selection changes.
             * @param context
             */
            selectedRecordDidChange: function(context) {

            },

            // Override to send an events for RecordsAreReady state
            startingCrudState: function(context) {
                // Announce to RecordsAreReady states that the CRUD started.
                // This will be handled and ignored for recursive calls
                Footprint.statechart.sendEvent('crudDidStart', context);
            },

            /***
             * Called when all records, including children, have completed CRUD.
             * @param context
             */
            didFinishRecords: function(context) {
                if (context.getPath('content.firstObject.constructor') !== this._context.getPath('content.firstObject.constructor')) {
                    logWarning("Context recordType: %@ does not match our recordType: %@. ChildRecordCrudState should have handled this event!".fmt(
                        context.getPath('content.firstObject.constructor'),
                        this._context.getPath('content.firstObject.constructor'))
                    );
                    return NO;
                }
                // All good, send the updated records to the main store
                this.parentState._nestedStore.commitChanges(YES);

                // Announce to RecordsAreReady states that the CRUD finished
                Footprint.statechart.sendEvent('crudDidFinish', this._context);
                // Slight hack: If we have an info pane open, go back to the ready state so
                // the user can continue editing. If we're doing editing-in-the-blind, go
                // all the way back to noModalState.
                if (this.parentState.parentState._infoPane)
                    this.gotoState(this.parentState.modalReadyState, this._context);
                else
                    this.gotoState('noModalState');
                return YES;
            },

            /***
             * Handle failure messages from the child record crud states
             * @param context
             * @returns {window.YES|*}
             */
            saveChildRecordsDidFail: function(context) {
                this.saveRecordsDidFail(context);
                return YES
            },
            /***
             * Called when saving fails at one of several spots along the way.
             */
            saveRecordsDidFail: function(context) {
                // Cancel any updates in progress
                Footprint.statechart.sendAction('cancelUpdate');

                var pluralizedContext = toArrayController(this.parentState._context);
                SC.AlertPane.warn({
                    message: "Failed to %@ records. Report this error if it recurs.".fmt(this.get('crudType')),
                    description: "Record Types: %@".fmt(uniqueRecordTypes(pluralizedContext.get('nestedStore'), pluralizedContext.get('content')).join(', '))
                });
                // Announce that the records failed to update so that a state can reset their record status
                Footprint.statechart.sendEvent('recordsDidFailToUpdate', pluralizedContext);
            },

            saveBeforeRecordsDidFail: function(context) {
                var pluralizedContext = toArrayController(
                    this.parentState._context,
                    {content:context.get('content')});
                SC.AlertPane.warn({
                    message: "Failed to create/update prerequisite records. Report this error if it recurs.",
                    description: "Record Types: %@".fmt(uniqueRecordTypes(pluralizedContext.get('nestedStore'), pluralizedContext.get('content')).join(', '))
                });
                // Goto our readyState so that the user can attempt to update again.
                this.gotoState(this.parentState.modalReadyState, pluralizedContext);
            },

            saveAfterRecordsDidFail: function(context) {
                var pluralizedContext = toArrayController(
                    this.parentState._context,
                    {content:context.get('content')});
                SC.AlertPane.warn({
                    message: "Failed to %@ dependent records. Report this error if it recurs.".fmt(context.get('crudType')),
                    description: "Record Types: %@".fmt(uniqueRecordTypes(pluralizedContext.get('nestedStore'), pluralizedContext.get('content')).join(', '))
                });
                // Goto our readyState so that the user can attempt to update again.
                this.gotoState(this.parentState.modalReadyState, pluralizedContext);
            },
            /***
             * Called by the above actions whenever saving fails at any step.
             */
            recordsDidFailToUpdate: function(context) {
                var pluralizedContext = toArrayController(
                    this.parentState._context,
                    {content:context.get('content')});
                pluralizedContext.get('content').forEach(function(record) {
                    record.set('progress', 0);
                    changeRecordStatus(this._nestedStore, record,
                        SC.Record.ERROR,
                        record.get('id') < 0 ?
                            SC.Record.READY_NEW :
                            SC.Record.READY_DIRTY);
                }, this);
                // Slight hack: If we have an info pane open, go back to the ready state so
                // the user can continue editing. If we're doing editing-in-the-blind, go
                // all the way back to noModalState.
                if (this.parentState.parentState._infoPane)
                    this.gotoState(this.parentState.modalReadyState, context);
                else
                    this.gotoState('noModalState');
            },

            // -------------------------
            // Internal support
            //
            enterState: function(context) {
                // Crud Saving indicator on
                context.setPath('recordsEditController.isSaving', YES);
                this._active = YES;
                // Reset the status indicator on the main store records.
                context.forEach(function(record) {
                    F.store.materializeRecord(record.get('storeKey')).set('progress', 0);
                });
                return sc_super();
            },
            exitState: function(context) {
                // Crud Saving indicator off
                context.setPath('recordsEditController.isSaving', NO);
                return sc_super();
            }
        })
    })
});
