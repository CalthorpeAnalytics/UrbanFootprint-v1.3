/**
 * Created by calthorpe on 11/18/13.
 */

sc_require('system/array_status');

Footprint.OverlayView = SC.View.extend({
    childViews: ['loadingOverlayView', 'errorOverlayView'],
    classNames: ['overlay-view'],

    /***
     * The content whose status is being observed.
     */
    content:null,
    status:null,

    arrayController: SC.ArrayController.create(SC.ArrayStatus),
    contentObserver: function() {
        if (this.get('testItems') && this.get('content'))
            this.setPathIfChanged('arrayController.content', this.get('content'));
    }.observes('.content'),
    arrayControllerStatus: null,
    arrayControllerStatusBinding: SC.Binding.oneWay('*arrayController.status'),

    /***
     * The content status. If set explicitly it is sent to statusMatches to determine if the overlay should be shown.
     * If set and testItems is also YES, The items will be tested if statusMatches returns false for status. If not
     * set and testItems is YES, the items will be checked. If status is null and testItems is NO, then content.status will
     * be checked
     */
    computedStatuses: function() {
        if (this.get('status')) {
            // Check status or both status and arrayController.status
            return [this.get('status')].concat(this.get('testItems') ? [this.getPath('arrayController.status')]: []);
        }
        if (this.get('testItems')) {
            // Check just arrayController status
            return [this.getPath('arrayController.status')];
        }
        // Check content.status
        return [this.getPath('content.status')];
    }.property('status', 'testItems', 'arrayControllerStatus').cacheable(),

    // If true test the status of all content items
    testItems: NO,
    showOnBusyOnly: NO,

    /***
     * We show the overlay if any status we check returns BUSY (if showOnBusyOnly=YES) or any status returns anything other than READY
     * We either check just status, all content items' statuses, or both
     */
    isVisible: function() {
        // If any computedStatus matches return true
        return this.get('computedStatuses').some(function(computedStatus) {
            return this.statusMatches(this.get('computedStatus'));
        }, this);
    }.property('computedStatuses').cacheable(),

    statusMatches: function(status) {
        return this.get('showOnBusyOnly') ?
            this.get('status') & SC.Record.BUSY :
            !(this.get('status') & SC.Record.READY);
    },

    loadingOverlayView: SC.View.extend({
        childViews:['imageView'],

        isVisibleBinding:SC.Binding.oneWay('.parentView.isVisible'),

        imageView: SC.ImageView.extend({
            layout: { centerX:0, centerY:0, width:27, height:27},
            useCanvas: NO,
            value: sc_static('footprint:images/spinner.gif')
        })
    }),

    errorOverlayView: SC.View.extend({
        childViews:['labelView'],
        isVisible:NO,
        isVisibleBinding: SC.Binding.oneWay('.parentView.status').matchesStatus(SC.Record.ERROR),
        labelView: SC.LabelView.extend({
            layout: { centerX:0, centerY:0, width:100, height:20},
            value: 'An Error Occurred...'
        })
    })
});
