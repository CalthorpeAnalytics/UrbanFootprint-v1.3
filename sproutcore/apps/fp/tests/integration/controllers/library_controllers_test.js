// ==========================================================================
// Project:   Footprint Unit Test
// Copyright: @2013 My Company, Inc.
// ==========================================================================

/**
 * Test the controllers manage the library of DbEntityInterests of the active ConfigEntity, and possibly other libraries, such as lists of charts, etc.
 */
module("Footprint.layLibraryControllers", {
    setup: function() {
        setupApplicationForControllerTesting(
            {
                stateSetup:bypassLoginState
            }
        );
    },

    teardown: controllerTeardown
});

test("Testing layersController", function() {

    // Give the test enough time to complete
    stop(30000);
    var params = {
        controllers: Footprint.layerControllers,
        controllersPath: 'Footprint.layersControllers',
        recordType: Footprint.PresentationMedium
    };
    Footprint.TestForLaryLibraryControllers = testListController(params);

    setTimeout(function() {
        // We exepct one PresentationMedium per db_entity
        var expectedLength = Footprint.scenarioActiveController.getPath('content.db_entities').length;
        ok(expectedLength > 0, "No DbEntities found for the active ConfigEntity");
        assertLength(
            expectedLength,
            Footprint.layersController.get('content'),
            'Footprint.layersController.content');
        assertKindForList(
            Footprint.PresentationMedium,
            Footprint.layersController.get('content'),
            'Footprint.layersController.content');
        // Restart the main thread
        start();
    }, 8000);
});


