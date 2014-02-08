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

sc_require('states/loading_records_state');

Footprint.CrudState = SC.State.extend({
    initialSubstate: 'resetState',

    resetState: SC.State.extend({
        enterState: function() {
            if (this._nestedStore) {
                // Make sure no changes remain outstanding
                this._nestedStore.discardChanges();
            }
            this.gotoState('%@.readyState'.fmt(this.getPath('parentState.fullPath')));
        }
    }),

    readyState: SC.State.extend({
        /***
         * The current info pane for the modal.
         * This can be set by the subclass to something permanent or passed in via context.infoPane
         * Alternatively if a RecordType has an infoPane() function it will be called to get the infoPane
         */
        _infoPane: null,

        /***
         * A bit of a hack to clear the filter property when selecting unless the modal is updating
         */
        doClearFilterUnlessModal: function() {
            Footprint.statechart.sendAction('doClearFilter');
            Footprint.statechart.sendAction('doClearJoins');
            Footprint.statechart.sendAction('doClearAggregates');
            Footprint.statechart.sendAction('doClearGroupBy');
        },

        doClearQueryAttributes: function() {
            Footprint.statechart.sendAction('doClearFilter');
            Footprint.statechart.sendAction('doClearJoins');
            Footprint.statechart.sendAction('doClearAggregates');
            Footprint.statechart.sendAction('doClearGroupBy');
        },

        /***
         * Handles a selection being made from a selection panel
         */
        doPickSelection: function(context) {
            this.invokeLater(function() {
                //context.getPath('parentView.parentView.parentView').remove()
            })
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
         * Converts modal table content to CSV and copies presents it in a window for copying
         * @param context
         */
        doCopy: function(context) {
            var csv = context.get('content').map(function (row) {
                return row.join(',')
            }).join('\n');
            Footprint.clip.setText(csv);
        },

        /***
         * Create a brand spankin' new record with minimum attributes copied from the context.
         * @param context - context.activeRecord is the is the context that is minimally copied
         */
        doCreateRecord:function(context) {
            // view objects don't like to get passed to the ArrayController, so filter for the key we want
            var safeContext = filter_keys(context, ['infoPane', 'recordsEditController', 'recordType', 'content']);
            var pluralContext = toArrayController(this._context || {}, safeContext, {crudType:'create'});
            this.gotoState('editingState', pluralContext);
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
            this.gotoState('editingState', pluralizeContext);
        },

        /***
         * Update the record in the context.
         * @param context - context.activeRecord is used for the editing states
         */
        doUpdateRecord:function(context) {
            var pluralizeContext = toArrayController(this._context || {}, context, {crudType:'update'});
            this.gotoState('editingState', pluralizeContext);
        },

        /***
         * View the record in the context
         * TODO use the updateRecordsState unless we need a different state for read-only
         * @param context - context.activeRecord is the selected record
         */
        doViewRecord:function(context) {
            var pluralizeContext = toArrayController(this._context || {}, context, {crudType:'view'});
            this.gotoState('editingState', pluralizeContext);
        },

        /***
         * Delete the selected record
         * @param context
         */
        doPromptDeleteRecord:function(context) {
            var pluralizedContext = toArrayController(
                this._context,
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


        /***
         * Query based on the recordType in the context
         * @param context - context.recordType is the type of record used for the querying states
         */
        doQueryRecords: function(context) {
            var singularContext = toArrayController(context);
            this.gotoState('editingState', singularContext);
        },

        doDeleteRecord: function(context) {
            var pluralizedContext = toArrayController(
                this._context || {},
                {content:context.get('content'), crudType:'delete'});
            // Set the deleted property on the record.
            pluralizedContext.forEach(function(record) {
                record._deleteSetup();
            });
            // If these are all new records just return. They are delete from view
            // and will be discarded when the state exits.
            if (pluralizedContext.filter(function(record) {
                return record.get('status') !== SC.Record.READY_NEW;
            }, this).get('length') == 0)
                return;

            // Deselect all objects in case we are selected records that will be removed
            // The controller should be wired up to reselect the selection of the source controller
            // Remove created records (that weren't saved)
            // Find the minimum selection index to reselect the adjacent object after
            var selection = this._recordsEditController.get('selection');
            if (selection) {
                var selIndexes = selection.indexSetForSource(context.get('content'));
                this._index = selIndexes ? selIndexes.min : 0;
            }
            Footprint.statechart.sendAction('doSave', pluralizedContext);
        },
        doSave: function(context) {
            var pluralizedContext = toArrayController(
                this._context,
                context.get('content') ? {content:context.get('content')} : {});
            pluralizedContext.forEach(function(record) {
                // Set progress to 0 for each record being created/updated in order to show post processing progress
                if ([SC.Record.READY_NEW, SC.Record.READY_DIRTY].contains(record.get('status')))
                    record.set('progress', 0);
            }, this);
            this.gotoState('%@.savingRecordState'.fmt(this.getPath('fullPath')),
                           toArrayController(pluralizedContext));
        },

        /***
         * Called when all records, including children have completed CRUD
         * @param context
         */
        didFinishRecords: function(context) {
            // All good, send the updated records to the main store
            try {;
                this._nestedStore.commitChanges(YES);
            }
            catch (error) {
                logWarning("Update/Delete succeeded, but commitChanges failed");
                this._nestedStore.discardChanges()
            }
            // Goto editingState so the user can continue editing
            this.gotoState(
                '%@.editingState'.fmt(this.get('fullPath')),
                context);
        },

        /***
         * An action sent by the record specific subclasses to indicate save progress during a create,
         * update, or delete.  The context contains a proportion property which is a non-cumulative
         * percent of progress toward complete the save. These are added to the saving record's
         * progress property. Because it's possible to have multiple records in our recordsEditController
         * updating at once, we examine the context key to see which of our records the id matches.
         * We have to use a key and not an id because new records have no useful id
         * @param context
         */
        doUpdateSaveProgress: function(context) {
            logProperty(context.get('key'), 'doUpdateSaveProgress context key');
            var keyPath = context.get('keyPath') || 'key';
            this._recordsEditController.forEach(function(record) {
                if (record.getPath(keyPath) !== context.get('key'))
                    return;

                logProperty(context.get('proportion'), 'Proportion of save progress');
                // Update the progress value on both versions of the recrod
                [record, record.getPath('store.parentStore').materializeRecord(record.get('storeKey'))].forEach(function(r) {
                    r.set('progress', record.get('progress') + context.get('proportion'));
                });
                logProperty(record.get('progress'), 'Total Progress');
                // All done? Then refresh the complete record from the server
                if (record.get('progress') == 1) {
                    // Refresh the record from the server.
                    // Even though the new record was retrived upon the initial save, post processing will usually
                    // create additional components of the record that we need to load here
                    // Alert the calling substate that the postprocessing ended. (TODO: this should be an event.)
                    if (context.postProcessingDidEnd) {
                        context.postProcessingDidEnd(SC.Object.create({content:record}));
                    }
                }
            }, this);
        },

        /***
         * Called when the main records being saved fail (as opposed to child records).
         */
        saveRecordsDidFail: function(context) {
            // Cancel any updates in progress
            Footprint.statechart.sendAction('cancelUpdate');

            var pluralizedContext = toArrayController(this._context);
            SC.AlertPane.warn({
                message: "Failed to %@ records. Report this error if it recurs.".fmt(this.get('crudType')),
                description: "Record Types: %@".fmt(uniqueRecordTypes(pluralizedContext.get('nestedStore'), pluralizedContext.get('content')).join(', '))
            });
            // Announce that the records failed to update so that a state can reset their record status
            Footprint.statechart.sendEvent('recordsDidFailToUpdate', pluralizedContext);
        },

        // TODO clean up
        postProcessRecordsDidFail: function(context) {
            var pluralizedContext = toArrayController(this._context);
            SC.AlertPane.warn({
                message: "Failed Post Process %@ records. Records will not be usuable".fmt(this.get('crudType')),
                description: "Record Types: %@".fmt(uniqueRecordTypes(pluralizedContext.get('nestedStore'), pluralizedContext.get('content')).join(', '))
            });
        },

        /***

        /***
         * Failure during post-processing. This means we likely have a bad record that is READY_CLEAN but not usable.
         * We mark the record as Error
         * @param context
         */
        postSaveDbEntityPublisherFailed: function(context) {
            // It appears that when the parent store's records are
            // destroyed, the change is propagated correctly to the
            // nested store. If there is any additional cleanup that
            // needs to be accomplished, accomplish it here.
            return NO;
        },

        saveBeforeRecordsDidFail: function(context) {
            var pluralizedContext = toArrayController(
                this._context,
                {content:context.get('content')});
            SC.AlertPane.warn({
                message: "Failed to %@ prerequisite records. Report this error if it recurs.".fmt(context.get('crudType')),
                description: "Record Types: %@".fmt(uniqueRecordTypes(pluralizedContext.get('nestedStore'), pluralizedContext.get('content')).join(', '))
            });
            // Goto our editingState so that the user can attempt to update again.
            this.gotoState('editingState', pluralizedContext);
        },

        saveAfterRecordsDidFail: function(context) {
            var pluralizedContext = toArrayController(
                this._context,
                {content:context.get('content')});
            SC.AlertPane.warn({
                message: "Failed to %@ dependent records. Report this error if it recurs.".fmt(context.get('crudType')),
                description: "Record Types: %@".fmt(uniqueRecordTypes(pluralizedContext.get('nestedStore'), pluralizedContext.get('content')).join(', '))
            });
            // Goto our editingState so that the user can attempt to update again.
            this.gotoState('editingState', pluralizedContext);
        },

        recordsDidFailToUpdate: function(context) {
            var pluralizedContext = toArrayController(
                this._context,
                {content:context.get('content')});
            pluralizedContext.get('content').forEach(function(record) {
                record.set('progress', 0);
                changeRecordStatus(this._nestedStore, record,
                    SC.Record.ERROR,
                    record.get('id') < 0 ?
                        SC.Record.READY_NEW :
                        SC.Record.READY_DIRTY);

            }, this);
            // Goto our editingState so that the user can attempt to update again.
            this.gotoState('editingState', pluralizedContext);
        },

        doResetCrudState: function() {
            // Restart the state
            this.gotoState(this.get('fullPath'));
        },

        doShowModal: function(context) {
            this.initializeModal(context);
        },
        doHideModal: function(context) {
            this.closeModal();
        },

        _recordsEditController: null,
        _context: null,
        _nestedStore: null,
        _infoPaneCache: null,
        enterState:function(context) {
            // This is the ArrayController or ObjectController that holds the nested store records
            // When cloning, we'll add records to the former.
            this._nestedStore = Footprint.store.chainAutonomousStore();
        },
        exitState: function() {
            this.closeModal();
            this._context = null;

            // Deselect all objects in case we are selected records that will be removed
            // The controller should be wired up to reselect the selection of the source controller
            if (this._recordsEditController)
                this._recordsEditController.deselectObjects(this._recordsEditController.get('selection'));

            // Discard changes
            if (this._nestedStore && !this._nestedStore.get('isDestroyed'))
                this._nestedStore.destroy();

            // Cleanup
            this._recordsEditController = null;
        },

        closeModal:function() {
            if (this._infoPane) {
                this._infoPane.remove();
            }
            // TODO Sometimes our _infoPane doesn't match the current infoPane
            findViewsByKind(Footprint.InfoPane).forEach(function(infoPane) {
                infoPane.remove();
            }, this)
        },

            /***
         *
         * @param context. Context contains:
         *  recordType: Required. The kind of record to view/edit
         *  activeRecord: Optional. The record to edit or clone. Set null to create a record from scratch
         *  content: Optional. Used for the activeRecord if activeRecord undefined. If activeRecord is simply null
         *  then null will be used, assuming a creation case
         *  nowShowing: Optional. Default 'Footprint.FeatureSummaryInfoView'. The view to show of the tabbed
         *  views in the modal window
         *  // TODO rename activeRecord to content throughout
         *
         */
        initializeModal:function(context) {

            // Resolve the infoView to use with the following three alternatives
            var infoPaneStringOrView = context && context.get('infoPane');
            if (infoPaneStringOrView) {
                var recordType = context.get('recordType');
                var infoPane = typeof(infoPaneStringOrView) == 'string' ? SC.objectForPropertyPath(infoPaneStringOrView) : infoPane;
                if (!infoPane) {
                    throw Error("infoPane was not set or configured for recordType %@".fmt(recordType));
                }
                var createdInfoPane;
                if (this._infoPane && this._infoPane.get('recordType') == recordType) {
                    // infoPane is already set to the same recordType
                    this._infoPane.set('context', context);
                    this._infoPane.append();
                }
                else if (this._infoPaneCache && this._infoPaneCache[SC.guidFor(recordType)]) {
                    // infoPane is a different record type but that type has been cached
                    this._infoPane = this._infoPaneCache[SC.guidFor(recordType)];
                    this._infoPane.set('context', context);
                    createdInfoPane = this._infoPane;
                    createdInfoPane.append();
                }
                else {
                    // infoPane is a different record type and that type has not been cached
                    createdInfoPane = infoPane.create({
                        recordType:recordType,
                        context:context
                    });
                    // Display it
                    createdInfoPane.append();
                    // Remember it for reenter and exit
                    this._infoPane = createdInfoPane;
                    // Cache the creation
                    this._infoPaneCache = this._infoPaneCache || {};
                    this._infoPaneCache[SC.guidFor(recordType)] = this._infoPane;
                }
            }
        },

        initialSubstate: 'noContentState',
        /***
         * A state for when we enter with no content
         */
        noContentState: SC.State.extend({
            doUpdateSaveProgress: function(context) {
                // Disregard stray messages from socketIO
            }
        }),

        doPromptCancel: function(context) {
            // If all records in the controller are new or clean, just delete without a prompt
            var newOrDirtyRecords = this._recordsEditController.filter(function(record) {
                return (record.get('status') === SC.Record.READY_NEW ||
                    record.get('status') === SC.Record.READY_DIRTY);
            }, this);
            // No changes, proceed
            if (newOrDirtyRecords.get('length') == 0) {
                this.doCancel(context);
                return;
            }

            SC.AlertPane.warn({
                message: "You are about cancel with the following item%@ edited but not saved: %@. Changes will be discarded.".fmt(
                    newOrDirtyRecords.get('length') > 1 ? 's' : '', // TODO auto-pluralize
                    newOrDirtyRecords.mapProperty('name').join(', ')
                ),
                description: "",
                caption: "",
                delegate: this,
                buttons: [
                    { title: "Keep Open" },
                    { title: "Don't Save", action:'doCancel' }
                ]
            });
        },
        doCancel: function() {
            this.gotoState('%@.resetState'.fmt(this.getPath('parentState.fullPath')));
        },


        /***
         * Override this to set up the record(s) for editing, either adding or updating
         */
        editingState:SC.State.extend({

            doResetCrudState: function() {
                // Cycle the store
                this.getPath('parentState._nestedStore').destroy();
                this.setPath('parentState._nestedStore', Footprint.store.chainAutonomousStore());
                // Restart the state
                this.gotoState(this.get('fullPath'), this._context);
            },

            enterState:function(context) {

                // Set up the modal if an infoPane is specified
                this.get('parentState').initializeModal(context);
                // Get the nestedStore created by the parent
                this._nestedStore = this.getPath('parentState._nestedStore');
                // Get and share the recordsEditController
                this._recordsEditController = context.get('recordsEditController');
                this.setPath('parentState._recordsEditController', this._recordsEditController);
                // Set the nestedStore of the controller. This updates its content query
                // to a new query with this nestedStore
                this._recordsEditController.set('nestedStore', this._nestedStore);
                this._nestedStore.reset();

                // Get the clone, create, or update/view content
                var content = this.prepareContent(context);
                // Create the complete context. This will get passed around with the content overridden sometimes
                // when different content is the target of an action
                this._context = SC.ArrayController.create({
                    content: content,
                    nestedStore: this._nestedStore,
                    recordType:context.get('recordType'),
                    recordsEditController:this._recordsEditController
                });
                this.setPath('parentState._context', this._context);
                // Select content
                if (content)
                    this.invokeNext(this.selectContent)
                // Observe changes to the selection so we can reset the content
                this._recordsEditController.addObserver('selection', this, 'selectedRecordDidChange');
            },
            selectContent: function() {
                this._recordsEditController.selectObjects(this._context.get('content'));
            },
            exitState: function() {
                // Stop observing the selection
                this._recordsEditController.removeObserver('selection', this, 'selectedRecordDidChange');
                // Cleanup
                this._nestedStore = null;
                this._recordsEditController = null;
                this._context = null;
            },

            /***
             * Responds to an edit controller changing selection.
             * If that controller, the context, matches this _recordsEditController
             * change to the new selection
             * @param context
             */
            selectedRecordDidChange: function(context) {
                // Make sure this is our recordEditController changing
                if (SC.Set.create(context.getPath('selection').isEqual(SC.Set.create(this._context.get('content')))))
                    return;

                var selection = this._recordsEditController.getPath('selection');
                this._context.set('content', this.prepareContent(toArrayController(this._context, {content:selection})));
            },

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
                var sourceContextController = toArrayController({content:
                    // Set to passed in content if defined
                    context.get('content') ||
                    // Otherwise to the full selection or full content list
                    (this._recordsEditController.getPath('selection.length') > 0 ?
                        this._recordsEditController.get('selection').toArray() : // toArray to force ordering
                        // Default to all for stuff like features
                        this._recordsEditController.get('content'))
                });
                // No content, no problem. Go to the noContentState and wait for an update
                if (!sourceContextController) {
                    this.gotoState('noContentState', context);
                    return;
                }

                // Get the content array status or individual record status
                if (!sourceContextController.get('status') || sourceContextController.get('status') !== SC.Record.READY_NEW) {
                    if (context.get('crudType') === 'create') {
                        // Create a record from scratch, not clone
                        content = [this._nestedStore.createRecord(context.get('recordType'), {}, Footprint.Record.generateId())];
                        // Use the record type's _createSetup function to copy over
                        // minimum values, like a config_entity's parent_config_entity
                        // The seed record must be a complete record, not a new one
                        var seedRecord;
                        for(var i=0; i<this._recordsEditController.length(); i++) {
                            var record = this._recordsEditController.objectAt(i)
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
                    }
                    else if (context.get('crudType') === 'clone') {
                        // Get the nested version of the content even if its already nested
                        // Non-nested would be adding from the main interface, nested would be
                        // adding from the modal interface that has a list of nested store records
                        // The list is likely using a separate nestedStore
                        if (sourceContextController.get('length') != 1)
                        // TODO we can support cloning multiple items if useful
                            throw Error("Trying to clone from non singular context");
                        var nestedSourceContent = this._nestedStore.materializeRecord(sourceContextController.getPath('firstObject.storeKey'));
                        // Do the clone
                        content = [nestedSourceContent.cloneRecord(sourceContextController.get('firstObject'))];
                    }
                    else {
                        // For all other cases of non-new sourceContent
                        // This can be one or more items in an array
                        content = sourceContextController.get('content')
                    }
                }
                else {
                    // If we have content that is a new record then being here means
                    // that we are reentering this state.
                    // This is also the update/view/delete case of existing records
                    content = sourceContextController.get('content')
                }
                return content;
            }
        }),
        savingRecordState: SC.State.plugin('Footprint.SavingRecordState')
    })
});
