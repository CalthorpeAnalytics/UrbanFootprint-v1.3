/***
 * The state that manages the projects pane at the top of the application
 * @type {Class}
 */

Footprint.ShowingAnalysisToolsState = SC.State.design({

    initialSubstate: 'readyAnalysisModuleState',

    analysisModuleDidChange: function() {
        var analysisModule =  F.analysisModulesController.getPath('selection.firstObject');
        // Load tool controllers--0 or more
        var loadingControllers = analysisModule.get('analysis_tools').map(function(analysisTool) {
            // Look for a matching AnalysisTool controller
            return Footprint.analysisToolControllerLookup.get(analysisTool.get('key')) || null;
        }).compact();

        if (loadingControllers.get('length')==0) {
            // Nothing to do. Go restart ShowingAnalysisToolsState to get to recordsAreReadyState
            Footprint.statechart.gotoState(this.get('fullPath'));
            return
        }
        this.loadingAnalysisToolsState.set('loadingControllers', loadingControllers);
        Footprint.statechart.gotoState(this.loadingAnalysisToolsState);
        // Let others handle if needed
        return NO;
    },

    readyAnalysisModuleState: SC.State,

    loadingAnalysisToolsState: Footprint.ConcurrentLoadingState.extend({
        loadingSubstate: 'Footprint.LoadingAnalysisToolState',
        allControllersDidLoad: function() {
            Footprint.statechart.gotoState('analysisToolsAreReady', SC.Object.create({
                    content: F.analysisModulesController.getPath('selection.firstObject')
            }));
        }
    }),

    analysisToolsAreReady: Footprint.RecordsAreReadyState.extend({

        recordsDidUpdateEvent: 'analysisToolDidUpdate',
        recordsDidFailToUpdateEvent: 'analysisToolDidFailToUpdate',
        updateAction: 'doAnalysisToolUpdate',
        undoAction: 'doSupplementalAnalysisModuleUndo',

        doAnalysisToolUpdate: function(context) {
            // We need to explicitly make the active analysisModule dirty to get save to work
            var recordsEditController = this.getPath('recordsEditController');
            recordsEditController.set('recordsAreUpdating', YES);

            changeRecordStatus(
                this.getPath('recordsEditController.nestedStore'),
                this.getPath('recordsEditController.firstObject'),
                SC.Record.READY_CLEAN,
                SC.Record.READY_DIRTY);

            this.updateRecords({
                content:this.getPath('recordsEditController.firstObject'),
                recordsEditController: this.get('recordsEditController'),
                recordType: this.get('recordType')
            });
        },

        analysisToolDidUpdate: function(context) {

            var recordsEditController = this.getPath('recordsEditController');
            recordsEditController.set('recordsAreUpdating', NO);

            Footprint.mapLayerGroupsController.refreshLayers(['developable']);
            Footprint.statechart.gotoState('%@.readyState'.fmt(this.get('fullPath')), context);
        },
        // React to DbEntity saves by refreshing our records if the behavior matches
        dbEntityInterestDidUpdate: function(context) {
            var dbEntityInterest = context.get('record');
            var dbEntityBehavior = dbEntityInterest.getPath('db_entity.feature_behavior.behavior');
            Footprint.analysisModulesController.forEach(function(analysisModule) {
                (analysisModule.get('analysis_tools') || []).forEach(function(analysisTool) {
                    if (dbEntityBehavior == analysisTool.get('behavior')) {
                        analysisTool.refresh();
                    }
                }, this);
            }, this);
        },

        analysisToolDidFailToUpdate: function(context) {
            var recordsEditController = this.getPath('recordsEditController');
            recordsEditController.set('recordsAreUpdating', NO);
            Footprint.statechart.gotoState('%@.readyState'.fmt(this.get('fullPath')), context);
        },

        noAnalysisToolsState: SC.State,

        enterState: function(context) {
            var analysisTool = Footprint.analysisToolsController.getPath('selection.firstObject');
            if (!analysisTool) {
                Footprint.statechart.gotoState('noAnalysisToolsState');
                return;
            }
            var recordsEditController = Footprint.analysisToolEditControllerLookup.get(analysisTool.get('key'));
            this.set('recordsEditController', recordsEditController);
            this._recordsEditController = recordsEditController;

            this._context = context;
            this.set('content', this._content);
            this.set('recordType', this._context.get('recordType'));
            this.set('baseRecordType', this.get('recordType'));
            this._nestedStore = Footprint.store.chainAutonomousStore();
            this._recordsEditController.set('nestedStore', this._nestedStore);
            this._content = this._recordsEditController.get('content');

            sc_super();
        },
        exitState: function() {
            this._recordsEditController = null;
            if (this._nestedStore) {
                this._nestedStore.destroy();
                this._nestedStore = null;
            }
            this.set('content', null);
            this.set('recordType', null);
            this.set('baseRecordType', null);
            this.set('recordsEditController', null);
            sc_super()
        },

        undoManagerProperty: 'undoManager',

        updateContext: function(context) {
            var recordContext = SC.ObjectController.create();
            return this.createModifyContext(recordContext, context)
        }
    })
});


// Loads each controller to get the subclass version of the AnalysisTool instance
// We already have the nested base instances, but we need the specific of the subclass instances
// We rely on the configured AnalysisTool controllers to specify the correct recordType
Footprint.LoadingAnalysisToolState = Footprint.LoadingState.extend({
    recordArray: function() {
        var configEntity = Footprint.scenariosController.getPath('selection.firstObject');
        if (!configEntity)
            return;

        var localResults = Footprint.store.find(SC.Query.create({
            recordType: this.getPath('loadingController.recordType'),
            location: SC.Query.LOCAL,
            conditions: 'config_entity = {configEntity}',
            configEntity: configEntity
        }));
        if (localResults.get('length') > 0) {
            return localResults;
        }
        return Footprint.store.find(SC.Query.create({
            recordType: this.getPath('loadingController.recordType'),
            location: SC.Query.REMOTE,
            parameters: {
                config_entity: configEntity
            }
        }));
    },

    loadingAnalysisModuleControllerIsReady: function() {
        // Start over now that we have a analysis_moduleSelection
        // invokeLast to allow the active controller to bind
        this.invokeNext(function() {
            Fooptrint.statechart.gotoState(this.parentState.analysisToolsAreReady, this.get('loadingController'));
        });
    }
});

