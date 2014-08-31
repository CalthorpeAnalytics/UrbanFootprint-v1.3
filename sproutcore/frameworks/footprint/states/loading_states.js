

Footprint.LoadingState = SC.State.extend({

    init: function() {
        sc_super();
        if (!this.get('loadingController'))
            this.set('loadingController', SC.ArrayController.create())
    },

    initialSubstate: 'readyState',

    /**
     * Optional. The recordType to query for
     */
    recordType:null,

    /**
     * Optional. The controller that is loaded by binding its content to the query
     */
    loadingController: null,

    /***
     * Optional. Check the status of each record returned by recordArray(). Normally
     * just the status of the query or ManyArray that is returned by recordArray() is checked
     */
    checkRecordStatuses: NO,

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
        throw Error("Provide an Footprint.Store.find to load the content of loadingController. If just loading related records, this can simply return" +
            "the ManyArray records in question. Then the state will wait for the ManyArray status to become READY_CLEAN");
    },

    loadingStatusValue:0.5,

    _recordsQueue: null,

    enterState: function(context) {
        this._context = context;
        //TODO remove
        Footprint.loadingStatusController.increment(this.get('loadingStatusValue'));
        // Need to fetch the content
        var loadingController = this.get('loadingController');
        if (this.get('setLoadingControllerDirectly') && loadingController) {
            loadingController.set('content', this.recordArray(context));
            this._results = loadingController;
        }
        else {
            this._results = SC.ArrayController.create({content: this.recordArray(context)});
        }
        if (this.get('checkRecordStatuses')) {
            this._recordsQueue = SC.Set.create(this._results);
            this._recordsQueue.forEach(function(record) {
                record.addObserver('status', this, 'recordStatusDidChange');
            }, this);
            // Call in case they are already all READY_CLEAN
            this.recordStatusDidChange();
        }
        else {
            this._results.addObserver('status', this, 'loadingControllerStatusDidChange');
            // Call in case the status already READY_CLEAN
            this.loadingControllerStatusDidChange();
        }
    },

    readyState: SC.State,

    setLoadingControllerDirectly: NO,

    /***
     * Observe the status change of each record. This is only used
     * when checkRecordStatuses==YES
     */
    recordStatusDidChange: function() {
        var recordsDequeue = this._recordsQueue.filter(function(record) {
            if (record && record.get('status') & SC.Record.ERROR) {
                this.statechart.sendEvent(this.get('didFailEvent'), this._results)
                return NO;
            }
            return record && record.get('status') === SC.Record.READY_CLEAN;
        }, this);
        recordsDequeue.forEach(function(record) {
            record.removeObserver('status', this, 'recordStatusDidChange');
            this._recordsQueue.removeObject(record);
        }, this);
        if (this._recordsQueue.length == 0) {
            this.statechart.sendEvent(this.get('didLoadEvent'), this._results);
        }
    },

    /***
     * Observe the results status and notify listeners on load or failure
     * This is not used when checkRecordStatuses==YES
     */
    loadingControllerStatusDidChange:function() {
        var results = this._results;
        if (results.get('status') & SC.Record.READY) {
            if (!this.get('setLoadingControllerDirectly')) {
                var loadingController = this.get('loadingController');
                if (loadingController)
                    loadingController.set('content', results.get('content'));
            }
            if (this.get('didLoadEvent'))
                this.statechart.sendEvent(this.get('didLoadEvent'), results);
            if (loadingController)
                // This event is only used by ConcurrentLoadingState
                this.statechart.sendEvent('didLoadController', loadingController);
        }
        else if (results.get('status') & SC.Record.ERROR) {
            this.statechart.sendEvent(this.get('didFailEvent'), results)
        }
    },

    errorState: SC.State.extend({
        enterState: function() {
            logError('Error in loading state: %@'.fmt(this.toString()));
        }
    }),

    exitState:function() {
        // Stop observing upon exiting the state
        if (this._results)
            this._results.removeObserver('status', this, 'loadingControllerStatusDidChange');
        this._results = null;
        this._context = null;
    }
});


Footprint.ConcurrentLoadingState = SC.State.extend({
    // Required. The controllers to load concurrently
    loadingControllers: null,
    // Required The substate of LoadingState with a customized recordArray function
    // One will be generated for each loadingController
    loadingSubstate:null,

    enterState: function() {
        var substates = this.get('loadingControllers').map(function(loadingController) {
            // We assume loadingControllers have unique recordTypes, thus use it for the substate name
            var substateName = 'loading%@State'.fmt(loadingController.get('recordType').toString().split('.')[1]);
            var substate;
            substate = this.loadingChildrenState.getState(substateName);
            if (!substate) {
                substate = this.loadingChildrenState.addSubstate(
                    substateName,
                    SC.requiredObjectForPropertyPath(this.get('loadingSubstate'))
                );
            }
            substate.set('loadingController', loadingController);
            return substate;
        }, this);
        this.loadingChildrenState.set('activeSubstates', substates);
        Footprint.statechart.gotoState('loadingChildrenState');
    },

    // Holds all the LoadingState subclasses. Sends events allControllersDidLoad when they all finish loading
    loadingChildrenState: SC.State.extend({
        substatesAreConcurrent: YES,
        // The substates active for this run (until we learn how to destroy child states)
        activeSubstates: [],

        // This is sent by each substate as it finishes
        // The event is defined on LoadingState so make sure the subclass of LoadingState
        // doesn't consume it
        didLoadController: function(context) {
            var matchingSubstate = this.get('activeSubstates').find(function(substate) {
                return substate.get('loadingController') == context;
            }, this);
            if (!matchingSubstate) {
                // Probably the user switched Scenarios or similar while we awaited this event
                logWarning("No substate loadingController matched the context given to didLoadController. Context: %@".fmt(context));
                return;
            }
            this.get('activeSubstates').removeObject(matchingSubstate);
            if (this.getPath('activeSubstates.length') == 0) {
                Footprint.statechart.sendEvent('allControllersDidLoad');
            }
        }
    }),
    exitState: function() {
        // TODO should destroy children
    }
});
