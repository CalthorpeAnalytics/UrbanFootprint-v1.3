// ==========================================================================
// Project:   Footprint.loginController Unit Test
// Copyright: @2012 My Company, Inc.
// ==========================================================================


module("Footprint.loginController", {
    setup: function() {
        setupApplicationForControllerTesting(
            {
                stateSetup: function() {
                    // NOTE: loginContent and the Login model no longer exist. - Dave P
                    login = Footprint.store.find(SC.Query.local(Footprint.Login)).toArray()[0];
                    Footprint.loginContent.set('username', login.get('username'))
                    Footprint.loginContent.set('password', login.get('password'))
                }
            }
        );
    },

    teardown: controllerTeardown
});


test("Testing userController", function() {

    // Set the loginContent to simulate the form entry
    // Wait for the server
    stop(3000);
    setTimeout(function() {
        SC.RunLoop.begin();
        SC.RunLoop.end();
        assertStatus(Footprint.userController.content, Footprint.Record.READY_CLEAN, 'Footprint.userController');
        assertCurrentState(Footprint.LoadingApp);
        start();
    }, 1000);
});
