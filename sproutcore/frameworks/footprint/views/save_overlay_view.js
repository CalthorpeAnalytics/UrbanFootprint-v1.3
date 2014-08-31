/***
 * Displays a saving overlay if visible.
 * You can key the message based using savingMessage property
 * @type {*|RangeObserver|Class|void}
 */
Footprint.SaveOverlayView = SC.View.extend({
    classNames: ['form-info-overlay'],
    childViews: ['labelView'],
    /***
     * Set to display a message according to what is happening. Defaults to 'Saving...'
     */
    savingMessage: 'Saving...',
    labelView: SC.LabelView.extend({
        layout: { height: 20, width: 250, centerX: 0, centerY: 0 },
        savingMessage: null,
        savingMessageBinding: SC.Binding.oneWay('.parentView.savingMessage'),
        value: function() {
            return this.getPath('parentView.savingMessage');
        }.property('savingMessage').cacheable()
    })
});
