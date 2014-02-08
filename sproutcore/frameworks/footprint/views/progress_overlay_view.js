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
            // Record is BUSY
            !(this.get('status') & SC.Record.READY) ||
            // Record is READY but post_save is in-progress
            this.get('saveInProgress')
        )) ? YES : NO;
    }.property('content', 'status', 'saveInProgress').cacheable(),

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
 * This progress overlay is used where a main store record needs to show progress
 * based on a nested store records clone/create/update progress.
 */
Footprint.ProgressOverlayForMainStoreView = Footprint.ProgressOverlayView.extend({
    layout: { left:.5, right: 270, width:.5, centerY: 0, height: 16},
    classNames: ['overlay-view-for-main-store'],
    // The main store content item
    mainStoreContent: null,
    // The nested store content array
    nestedStoreContentArray: null,
    content: function() {
        // Find the corresponding nestedStore content
        return this.get('nestedStoreContentArray') ?
            this.get('nestedStoreContentArray').filter(function(item) {
                return item.get('storeKey') == this.getPath('mainStoreContent.storeKey');
            }, this)[0] :
            null;
    }.property('nestedStoreContentArray', 'mainStoreContent').cacheable(),
    statusBinding: SC.Binding.oneWay('*content.status')
});
