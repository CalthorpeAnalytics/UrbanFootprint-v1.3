sc_require('views/info_views/visualize_pane');
sc_require('states/loading_states');

/***
 * The state that manages the projects pane at the top of the application
 * @type {Class}
 */
Footprint.ShowingBuiltFormsState = Footprint.State.design({

    substatesAreConcurrent: YES,


    showingOrNotShowingState: SC.State.extend({
        initialSubstate: 'notShowingState',

        notShowingState: SC.State.extend({
            doVisualize: function() {
                this.gotoState('showingState')
            }
        }),
        showingState: SC.State.extend({
            doClose: function() {
                this.gotoState('notShowingState');
            },

            _infoPane:null,
            enterState: function(context) {
                this._infoPane = this._infoPane || Footprint.VisualizePane.create();
//                Footprint.mainPage.get('mainPane').remove();
                this._infoPane.append();

            },
            exitState: function(context) {
                this._infoPane.remove();
//                Footprint.mainPage.get('mainPane').append();
            }
        })

    }),


    loadManagementState: SC.State.extend({
        initialSubstate: 'initialLoadState',

        initialLoadState: SC.State.extend({
           enterState: function(context){
               Footprint.statechart.sendEvent('selectedBuiltFormDidChange', SC.Object.create({content : Footprint.builtFormCategoriesTreeController.getPath('selection.firstObject')}))
           }
        }),

        // LoadingState when the Footprint.builtFormActiveController is not ready
        loadingFlatBuiltFormState: Footprint.LoadingState.extend({
            enterState: function(context) {
                this._context = context;
                sc_super();
            },

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

        selectedBuiltFormDidChange: function(context) {
            this.gotoState('loadingFlatBuiltFormState', context);
        }

    })







});

