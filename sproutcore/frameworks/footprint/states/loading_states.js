

Footprint.LoadingState = SC.State.extend({

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
        this._results.addObserver('status', this, 'loadingControllerStatusDidChange');
        // Call the observer immediately in case the content is already ready
        this.loadingControllerStatusDidChange();
    },

    readyState: SC.State,


    setLoadingControllerDirectly: NO,
    /***
     * Observe the loading controller and notify listeners on load or failure
     */
    loadingControllerStatusDidChange:function() {
        var results = this._results;
        if (results.get('status') & SC.Record.READY) {
            if (!this.get('setLoadingControllerDirectly')) {
                var loadingController = this.get('loadingController');
                if (loadingController)
                    loadingController.set('content', results.get('content'));
            }
            this.statechart.sendEvent(this.get('didLoadEvent'), results);
        }
        else if (results.get('status') & SC.Record.ERROR) {
            this.statechart.sendEvent(this.get('didFailEvent'), results)
        }
    },

    errorState: SC.State.extend({
        enterState: function() {
//            SC.AlertPane.error('Error in loading state: %@'.fmt(this.toString()));
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
