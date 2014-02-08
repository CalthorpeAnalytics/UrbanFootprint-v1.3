// ==========================================================================
// Project:   Footprint Unit Test
// Copyright: @2013 My Company, Inc.
// ==========================================================================
/*globals Footprint module test ok equals same stop start */


module("Footprint.builtFormsControllers", {
    setup: function() {
        setupApplicationForControllerTesting(
            {
                stateSetup: bypassLoginState
            }
        );
    },
    teardown: controllerTeardown
});


test("Testing builtFormCategoriesTreeController", function() {
    // Give the test enough time to complete
    stop(30000);
    var params = {
        controllers: Footprint.builtFormControllers,
        controllersPath: 'Footprint.builtFormControllers',
        recordType: Footprint.BuiltForm
    };
    Footprint.TestForBuiltFormControllers = testTreeController(params);
});

