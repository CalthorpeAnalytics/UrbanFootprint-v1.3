sc_require('controllers/global_config_controllers');
sc_require('controllers/regions_controllers');
sc_require('controllers/projects_controllers');
sc_require('controllers/scenarios/scenario_controllers');

Footprint.LoadingState = Footprint.State.extend({

    init: function() {
        sc_super();
        if (!this.get('loadingController'))
            this.set('loadingController', SC.ArrayController.create())
    },

    initialSubstate: 'readyState',

    /**
     * The recordType to query for
     */
    recordType:null,
    /**
     * The controller that is loaded by binding its content to the query
     */
    loadingController: null,

    /**
     * The state event sent when the controller loads
     * TODO rename to isReadyEvent
     */
    didLoadEvent:null,
    /**
     * The state event sent when the controller fails
     */
    didFailEvent:'didFailLoadingController',

    recordArray:function() {
        throw "Provide an Footprint.Store.find to load the content of loadingController";
    },

    loadingStatusValue:0.5,

    enterState: function() {
        Footprint.loadingStatusController.increment(this.get('loadingStatusValue'));

        var loadingController = this.get('loadingController');
        // Don't observe until we enter the state
        loadingController.addObserver('status', this, 'loadingControllerStatusDidChange');

        // Need to fetch the content
        loadingController.set('content', this.recordArray());
        // Call the observer immediately in case the content is already ready
        this.loadingControllerStatusDidChange();
    },

    readyState: SC.State,

    /***
     * Observe the loading controller and notify listeners on load or failure
     */
    loadingControllerStatusDidChange:function() {
        var loadingController = this.get('loadingController');
        if (loadingController.get('status') === SC.Record.READY_CLEAN) {
            this.statechart.sendEvent(this.get('didLoadEvent'), loadingController);
        }
        else if (loadingController.get('status') & SC.Record.ERROR) {
            this.statechart.sendEvent(this.get('didFailEvent'), loadingController);
        }
    },

    errorState: SC.State.extend({
        enterState: function() {
//            SC.AlertPane.error('Error in loading state: %@'.fmt(this.toString()));
        }
    }),

    exitState:function() {
        // Stop observing upon exiting the state
        this.get('loadingController').removeObserver('status', this, 'loadingControllerStatusDidChange');
    }
});

Footprint.LoadingConfigEntityState = Footprint.LoadingState.extend({

    parentController:null,
    /**
     * Queries for all the scenarios of the ConfigEntity
     * @returns {*}
     */
    recordArray:function() {
        return Footprint.store.find(
            SC.Query.create({
                recordType: this.get('recordType'),
                location:SC.Query.REMOTE,
                parameters:{
                    //parent_config_entity: this.getPath('parentController.selection.firstObject')
                }
        }));
    }
});

Footprint.LoadingGlobalConfigState = Footprint.LoadingState.extend({
    recordType:Footprint.GlobalConfig,
    loadingController:Footprint.globalConfigController,
    didLoadEvent:'didLoadGlobalConfigController',

    /**
     * Queries for the singleton Globalconfig
     */
    recordArray:function() {
        return Footprint.store.find(SC.Query.remote(
            this.get('recordType')
        ));
    }
});

Footprint.LoadingRegionsState = Footprint.LoadingConfigEntityState.design({
    recordType:Footprint.Region,
    loadingController: Footprint.regionsController,
    parentController:Footprint.globalConfigController,
    didLoadEvent:'didLoadRegionController'
});

Footprint.LoadingProjectsState = Footprint.LoadingConfigEntityState.design({
    recordType:Footprint.Project,
    substatesAreConcurrent: YES,
    initialSubstate: null,
    loadingController: SC.ArrayController.create(),
    parentController: Footprint.regionActiveController,
    didLoadEvent:'didLoadProjectController'
});

Footprint.LoadingScenarioDependenciesState = SC.State.design({
    substatesAreConcurrent: YES,
    loadingScenarioCategoriesState:SC.State.plugin('Footprint.LoadingScenarioCategoriesState'),
    loadingBuiltFormTagsState:SC.State.plugin('Footprint.LoadingBuiltFormTagsState'),
    loadingLayerTagsState:SC.State.plugin('Footprint.LoadingLayerTagsState'),
    loadingPresentationsState:SC.State.plugin('Footprint.LoadingPresentationsState'),
    loadingBuiltFormSetsState:SC.State.plugin('Footprint.LoadingBuiltFormSetsState'),
    loadingPolicySetsState:SC.State.plugin('Footprint.LoadingPolicySetsState'),

    enterState: function() {
        this._loadingControllerQueue = [];
        this.get('substates').forEach(function(substate) {
            substate.get('loadingController').addObserver('status', this, 'loadingControllerStatusDidChange')
            this._loadingControllerQueue.push(substate);
        }, this);
    },

    loadingControllerStatusDidChange:function(sender) {
        if (sender.get('status') & SC.Record.READY) {
            sender.removeObserver('status', this, 'loadingControllerStatusDidChange');
            this._loadingControllerQueue.pop(sender);
        }
        if (this._loadingControllerQueue.length == 0) {
            this.statechart.sendEvent('didLoadScenarioDependencies');
        }
    }
});

Footprint.LoadingScenariosState = Footprint.LoadingConfigEntityState.design({
    recordType:Footprint.Scenario,
    loadingController: SC.ArrayController.create(),
    parentController: Footprint.projectActiveController,
    didLoadEvent:'didLoadScenarioController'
});

/***
 * The default post-login state, whether for an authenticated session or an anonymous demo session
 * @type {Class}
 * TODO rename states to have State suffix
 */
Footprint.LoadingAppState = Footprint.State.design({

    // These states are loaded sequentially
    loadingGlobalConfigState: Footprint.LoadingGlobalConfigState,
    loadingRegionsState: Footprint.LoadingRegionsState,
    loadingProjectsState: Footprint.LoadingProjectsState,
    loadingScenariosState: Footprint.LoadingScenariosState,
    loadingScenarioDependenciesState: Footprint.LoadingScenarioDependenciesState,

    initialSubstate:'loadingGlobalConfigState',

    enterState: function() {
        Footprint.mainPage.get('loadingPane').append();
    },

    didLoadGlobalConfigController: function() {
        this.gotoState('loadingRegionsState');
    },
    didLoadRegionController: function() {
        this.getPath('loadingRegionsState.loadingController').forEach(function(region) {
            var loadingRegionStateClassName = 'Footprint.LoadingRegion%@State'.fmt(region.get('key').classify());
            // If it exists create a substate with which to load client data
            var loadingRegionStateClass = SC.objectForPropertyPath(loadingRegionStateClassName);
            // TODO for some reason loadingProjectsState doesn't run if this is null
            if (loadingRegionStateClass) {
                // By adding a substate to a concurrent state that supports concurrent classes, this will
                // run when we enter the state, along with the loadingProjectState itself
                this.get('loadingProjectsState').addSubstate('loading%@State'.fmt(region.get('key').classify()), loadingRegionStateClass);
            }
        }, this);

        this.gotoState('loadingProjectsState');
    },
    didLoadProjectController: function() {
        this.gotoState('loadingScenarioDependenciesState');
    },
    didLoadScenarioDependencies: function() {
        this.gotoState('loadingScenariosState');
    },
    didLoadScenarioController: function() {
        this.gotoState('showingAppState')
    },

    didFailLoadingController: function(context) {
        logError("Loading state did error for state: %@".fmt(context.toString()));
    },

    exitState:function() {
        Footprint.getPath('mainPage.loadingPane').remove();
    }
});
