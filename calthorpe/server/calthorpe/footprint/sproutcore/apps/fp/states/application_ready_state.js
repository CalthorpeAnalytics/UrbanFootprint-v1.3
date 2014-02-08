Footprint.ApplicationReadyState = SC.State.extend({

    enterState: function() {
        // Check for authentication and respond accordingly
        this.gotoState('loggingInState');
    },

    exitState: function() {
        // Nothing to worry about here.
    }

});

