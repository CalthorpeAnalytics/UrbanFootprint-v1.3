// ==========================================================================
// Project:   Footprint Unit Test
// Copyright: @2013 My Company, Inc.
// ==========================================================================
/*globals Footprint module test ok equals same stop start */


module("Footprint.policiesControllers", {
    setup: function() {
        setupApplicationForControllerTesting(
            {
                stateSetup: bypassLoginState
            }
        );
    },

    teardown: controllerTeardown
});

test("Testing policyCategoriesTreeController", function() {

    // Give the test enough time to complete the asynchronous timeout handlers
    stop(10000);

    setTimeout(function() {
        // Verify that PolicySet instances at the first level of the tree
        var policyCategories = Footprint.policyCategoriesTreeController.get('treeItemChildren');
        assertNonZeroLength(policyCategories, 'Footprint.policyCategoriesTreeController.arrangedObjects');
        assertKindForList(Footprint.PolicyCategory, policyCategories, 'Footprint.policyCategoriesTreeController.arrangedObjects');
        // Verify that Policy instances at the second level of the tree
        assertNonZeroLength(policyCategories[0].get('treeItemChildren'),
            'Footprint.policyCategoriesTreeController.treeItemChildren[0].treeItemChildren');
        assertKindForList(Footprint.Policy, policyCategories[0].get('treeItemChildren'),
            'Footprint.policyCategoriesTreeController.treeItemChildren[0].treeItemChildren');
        // Restart the main thread
        start();
    }, 2400);
});
