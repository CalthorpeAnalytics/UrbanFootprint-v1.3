sc_require('controllers/global_config_controllers');
sc_require('controllers/regions_controllers');
sc_require('controllers/projects_controllers');
sc_require('controllers/scenarios/scenario_controllers');

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

Footprint.LoadingConcurrentDependenciesState = SC.State.extend({
    substatesAreConcurrent: YES,
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
            this.statechart.sendEvent('didLoadConcurrentDependencies');
        }
    }
});

Footprint.LoadingScenarioDependenciesState = Footprint.LoadingConcurrentDependenciesState.extend({
    didLoadConcurrentDependencies: function() {
        this.statechart.sendEvent('didLoadScenarioDependencies');
    },
    loadingScenarioCategoriesState:SC.State.plugin('Footprint.LoadingScenarioCategoriesState'),
    loadingBuiltFormTagsState:SC.State.plugin('Footprint.LoadingBuiltFormTagsState'),
    loadingLayerTagsState:SC.State.plugin('Footprint.LoadingLayerTagsState'),
    loadingBuildingUseDefinitionsState:SC.State.plugin('Footprint.LoadingBuildingUseDefinitionsState'),
    loadingBehaviorsState:SC.State.plugin('Footprint.LoadingBehaviorsState'),
    loadingIntersectionsState:SC.State.plugin('Footprint.LoadingIntersectionsState')
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
Footprint.LoadingAppState = SC.State.design({

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
        var regionController = this.get('loadingController');
        this.getPath('loadingRegionsState.loadingController').forEach(function(region) {
            var delegate = Footprint.regionActiveController.get('configEntityDelegate');
            var loadingRegionStateClass = delegate.get('loadingRegionState')

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
    didLoadScenarioController: function(context) {
        // Goto without a sending the context. The receiver expect a single Scenario, not the list
        this.gotoState('showingAppState')
    },

    didFailLoadingController: function(context) {
        SC.AlertPane.error({
            message: 'Login Error',
            description: "There was an error logging you in. Please alert the system's administrator. Sorry for the inconvenience!",
            buttons: [{
                title: 'OK',
                action: 'doLogout'
            }]
        })
    },

    exitState:function() {
        Footprint.getPath('mainPage.loadingPane').remove();
    }
});
