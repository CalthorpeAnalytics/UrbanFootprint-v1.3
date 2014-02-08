/**
 *
 * Created by calthorpe on 12/28/13.
 */

Footprint.CancelButtonView = SC.ButtonView.design({
    layout: { height: 24, width: 80 },

    calculatedStatus: null,
    title: function() {
        return this.get('calculatedStatus') === SC.Record.READY_DIRTY ||
            this.get('calculatedStatus') === SC.Record.READY_NEW ?
            'Cancel' : 'Done';
    }.property('calculatedStatus').cacheable(),
    action: 'doPromptCancel'
});
