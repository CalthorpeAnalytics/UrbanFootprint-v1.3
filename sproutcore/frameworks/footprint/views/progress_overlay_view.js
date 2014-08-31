/**
 * Created by calthorpe on 11/18/13.
 */

Footprint.ProgressOverlayView = SC.View.extend({
    childViews: ['loadingProgressOverlayView', 'errorProgressOverlayView'],
    classNames: ['overlay-view'],

    /***
     * The content whose status is being observed.
     */
    content:null,
    /***
     * The content status
     */
    status:null,
    statusBinding:SC.Binding.oneWay('*content.status'),
    /***
     * post-save progress of the content on the server
     * some records need to do post-save processing on the server, even after the save
     * returns and the record's status is ready. This property tracks that value from 0 to 1
     * and shows it in the progress bar.
     */
    saveInProgress:null,
    saveInProgressBinding:SC.Binding.oneWay('*content.saveInProgress'),
    // Show the progress bar if the record is not ready or the saveInProgress is true
    isVisible: function() {
        return (this.get('content') && (
            // Record is READY but post_save is in-progress
            this.get('saveInProgress')
        )) ? YES : NO;
    }.property('content', 'saveInProgress').cacheable(),

    loadingProgressOverlayView: SC.ProgressView.extend({
        classNames: ['loading-progress-overlay-view'],
        isVisible:NO,
        isVisibleBinding: SC.Binding.oneWay('.parentView.status').matchesStatus(SC.Record.ERROR).not(),
        valueBinding: SC.Binding.oneWay('.parentView*content.progress'),
        minimum: 0,
        maximum: 1
    }),

    errorProgressOverlayView: SC.ProgressView.extend({
        classNames: ['error-progress-overlay-view'],
        isVisible:NO,
        isVisibleBinding: SC.Binding.oneWay('.parentView.status').matchesStatus(SC.Record.ERROR),
        value: 0,
        minimum: 0,
        maximum: 1
    })
});

/***
 * This progress overlay is used when you need to display progress (managed on parent store
 * records) of a nested store record.
 */
Footprint.ProgressOverlayForNestedStoreView = Footprint.ProgressOverlayView.extend({
    nestedStoreContent: null,
    nestedStoreContentStatus: null,
    nestedStoreContentStatusBinding: SC.Binding.oneWay('*nestedStoreContent.status'),
    nestedStoreHasChanges: null,
    nestedStoreHasChangesBinding: SC.Binding.oneWay('*nestedStoreContent.store.hasChanges'),
    content: function() {
        // GATEKEEP: No nested content.
        var nestedStoreContent = this.get('nestedStoreContent');
        if (!nestedStoreContent)
            return null;
        // GATEKEEP: Doesn't exist in the master store yet.
        var storeKey = nestedStoreContent.get('storeKey');
        var store = nestedStoreContent.getPath('store.parentStore');
        // The check of < 0 is a bug work around for materializeRecord of nested records
        var id = store.idFor(storeKey);
        if (!id || id < 0)
            return null;
        // Return the master store's copy of the record.
        return store.find(nestedStoreContent.constructor, nestedStoreContent.get('id'));
    }.property('nestedStoreContent', 'nestedStoreContentStatus', 'nestedStoreHasChanges').cacheable()
});

