// ==========================================================================
// Project:   Footprint Unit Test
// Copyright: @2013 My Company, Inc.
// ==========================================================================

module("Footprint.scenarioController", {
    setup: function() {
        setupApplicationForControllerTesting(
            {
                stateSetup:bypassLoginState
            }
        );
    },

    teardown: function() {
        controllerTeardown();
    }
});

test("Testing scenarioController", function() {

    ok('test');
    // Give the test enough time to complete the asynchronous timeout handlers
    stop(20000);

    var timeout=0;
    setTimeout(function() {
        logStatus(Footprint.globalConfigController, 'Footprint.globalConfigController');
        assertStatus(Footprint.globalConfigController, Footprint.Record.READY_CLEAN, 'Footprint.globalConfigController');
    }, timeout+=2000);

    setTimeout(function() {
        logStatus(Footprint.regionsController, 'Footprint.regionsController');
        assertStatus(Footprint.regionsController, Footprint.Record.READY_CLEAN, 'Footprint.regionsController');
    }, timeout+=2000);

    setTimeout(function() {
        logStatus(Footprint.projectsController, 'Footprint.projectsController');
        assertStatus(Footprint.projectsController, Footprint.Record.READY_CLEAN, 'Footprint.projectsController');
    }, timeout+=2000);

    setTimeout(function() {
        logStatus(Footprint.scenariosController, 'Footprint.scenariosController');
        assertStatus(Footprint.scenariosController, Footprint.Record.READY_CLEAN, 'Footprint.scenariosController');
        start();
    }, timeout+=5000);

});
