/**
 * Created by calthorpe on 11/18/13.
 */

Footprint.OverlayView = SC.View.extend({
    childViews: ['loadingOverlayView', 'errorOverlayView'],
    classNames: ['overlay-view'],

    /***
     * The content whose status is being observed.
     */
    content:null,
    /***
     * The content status
     */
    status:null,
    // If true test the status of all content items
    testItems: NO,
    showOnBusyOnly: NO,

    isVisible: function() {
        // If testItems then check all content items
        return this.get('testItems') ?
            (this.get('content') || []).toArray().concat(this.get('content')).filter(function(item) {
                return !item || this.statusMatches(item.get('status'));
            }, this) > 0:
            this.statusMatches(this.get(status));
    }.property('status', 'content', 'testItems').cacheable(),

    statusMatches: function(status) {
        return this.get('showOnBusyOnly') ?
            this.get('status') & SC.Record.BUSY :
            !(this.get('status') & SC.Record.READY);
    },

    loadingOverlayView: SC.View.extend({
        childViews:['imageView'],

        isVisibleBinding:SC.Binding.oneWay('.parentView.isVisible'),

        imageView: SC.ImageView.extend({
            layout: { centerX:0, centerY:0, width:40, height:40},
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
