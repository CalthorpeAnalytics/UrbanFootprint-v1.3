/***
 * The state that manages the projects pane at the top of the application
 * @type {Class}
 */
Footprint.ShowingBuiltFormsState = SC.State.design({
    buildingDidChange: function(context) {
        // Let this propagate through to other listeners
        return NO;
    },
    buildingsDidChange: function(context) {
        this.gotoState('buildingsAreReadyState', context)
    },
    buildingTypeDidChange: function(context) {
        // Let this propagate through to other listeners
        return NO;
    },
    buildingTypesDidChange: function(context) {
        this.gotoState('buildingTypesAreReadyState', context)
    },
    placetypeDidChange: function(context) {
        // Let this propagate through to other listeners
        return NO;
    },
    placetypesDidChange: function(context) {
        this.gotoState('placetypesAreReadyState', context)
    },

    doManageBuiltForms: function(context) {
        // Default behavior is to view/manage buildings
        var pluralContext = toArrayController(context, {crudType:'view'});
        this.doManageBuildings(pluralContext);
    },

    doManageBuildings: function(context) {
        // Tell the modal_state to show the BuiltForm panes,
        // even though our data might not be ready yet.
        var localContext = {
            infoPane: 'Footprint.BuiltFormInfoPane',
            nowShowing:'Footprint.ManageBuildingView',
            recordType: Footprint.PrimaryComponent,
            recordsEditController: Footprint.buildingsEditController,
            loadingController:Footprint.buildingsController
        };
        var pluralContext = toArrayController(filter_keys(context, ['crudType', 'content']), localContext)
        this.gotoState('builtFormEditState', pluralContext);
    },

    doManageBuildingTypes: function(context) {
        var localContext = {
            infoPane: 'Footprint.BuiltFormInfoPane',
            nowShowing:'Footprint.ManageBuildingTypeView',
            recordType: Footprint.PlacetypeComponent,
            recordsEditController: Footprint.buildingTypesEditController,
            loadingController:Footprint.buildingTypesController
        };
        var pluralContext = toArrayController(filter_keys(context, ['crudType', 'content']), localContext)
        this.gotoState('builtFormEditState', pluralContext);
    },

    doManagePlaceTypes: function(context) {
        var localContext = {
            infoPane: 'Footprint.BuiltFormInfoPane',
            nowShowing:'Footprint.ManagePlacetypeView',
            recordType: Footprint.Placetype,
            recordsEditController: Footprint.placetypesEditController,
            loadingController:Footprint.placetypesController
        };
        var pluralContext = toArrayController(filter_keys(context, ['crudType', 'content']), localContext)
        this.gotoState('builtFormEditState', pluralContext);
    },

    initialSubstate: 'readyState',
    readyState: SC.State,
    builtFormEditState: SC.State.extend({

        initialSubstate: 'loadingState',
        loadingState: Footprint.LoadingState.extend({
            didLoadEvent: 'didLoadBuiltForms',
            didFailEvent: 'didFailToLoadBuiltForms',

            enterState: function(context) {
                // Show the modal while the records are loading so that the user knows something is happening.
                Footprint.statechart.sendAction('doHideModal', context);
                Footprint.statechart.sendAction('doShowModal', context);

                this.set('loadingController', context.get('loadingController')) ;
                sc_super();
            },

            recordArray: function() {
                if (this.getPath('loadingController.status') === SC.Record.READY_CLEAN)
                    return this.getPath('loadingController.content');
                return Footprint.store.find(SC.Query.create({
                    recordType: this._context.get('recordType'),
                    location: SC.Query.REMOTE
                }));
            },

            didLoadBuiltForms: function(context) {
                this.gotoState('builtFormsAreReadyState', this._context);
            },
            didFailToLoadBuiltForms: function() {
                this.gotoState(this.getPath('parentState.parentState.fullName'));
            }
        }),

        builtFormsAreReadyState: Footprint.RecordsAreReadyState.extend({
            recordsDidUpdateEvent: 'builtFormsDidChange',
            recordsDidFailToUpdateEvent: 'builtFormsDidFailToUpdate',
            updateAction: 'doBuiltFormUpdate',
            undoAction: 'doBuiltFormUndo',

            enterState: function(context) {

                this._nestedStore = Footprint.store.chainAutonomousStore();
                this._content = this._nestedStore.find(SC.Query.local(
                    context.get('recordType'), {
                        conditions: '{storeKeys} CONTAINS storeKey',
                        storeKeys:context.get('loadingController').mapProperty('storeKey')
                    }));
                this._context = SC.ArrayController.create({content: this._content, recordType:context.get('recordType')});
                sc_super();

                var crudContext = toArrayController(context, {content:context.getPath('recordsEditController.selection.firstObject')})

                // Call doCloneRecord, doCreateRecord
                Footprint.statechart.sendAction('do%@Record'.fmt(context.get('crudType').capitalize()), crudContext)
            }
        })
    }),

    loadManagementState: SC.State.extend({

//        doVisualize: function() {
//            Footprint.statechart.sendAction('doViewRecord', {
//                infoPane: 'Footprint.VisualizePane'
//            })
//        },

        initialSubstate: 'initialLoadState',

        initialLoadState: SC.State.extend({
            enterState: function(context){
                Footprint.statechart.sendEvent('builtFormDidChange', SC.Object.create({content : Footprint.builtFormCategoriesTreeController.getPath('selection.firstObject')}))
            }
        }),
        // LoadingState when the Footprint.builtFormActiveController is not ready
        loadingFlatBuiltFormState: Footprint.LoadingState.extend({

            recordType:Footprint.FlatBuiltForm,
            didLoadEvent: 'didLoadFlatBuiltForm',
            loadingController: Footprint.flatBuiltFormsController,
            recordArray:function() {
                return Footprint.store.find(
                    SC.Query.create({
                        recordType: this.get('recordType'),
                        location:SC.Query.REMOTE,
                        parameters:{
                            built_form_id: this._context.getPath('content.id')
                        }
                    })
                );
            },
            didLoadFlatBuiltForm:function() {
                // Get out of this state
                this.gotoState('loadedState');
            }
        }),
        loadedState: SC.State,

        builtFormDidChange: function(context) {
            this.gotoState('loadingFlatBuiltFormState', context);
        }

    })
});

