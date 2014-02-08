/**
 *
 * Created by calthorpe on 11/18/13.
 */

SC.ChildArray.reopen({

    refresh: function() {
        var record = this.get('record');
        if (record) record.refresh();
    },

    status: null,
    statusBinding: SC.Binding.oneWay('*record.status')

    // // Set up observers.
    // contentDidChange: function() {
    //     var observedRecords = this._observedRecords;
    //     if (!observedRecords) observedRecords = this._observedRecords = [];
    //     var record, i, len;
    //     // If any items in observedRecords are not in content, stop observing them.
    //     len = observedRecords.length;
    //     for (i = len - 1; i >= 0; i--) {
    //         record = observedRecords.objectAt(i);
    //         if (!this.contains(record)) {
    //             record.removeObserver('status', this, this.notifyStatusChange);
    //             observedRecords.removeObject(record);
    //         }
    //     }
    //     // If any item in content is not in observedRecords, observe them.
    //     len = this.get('length');
    //     for (i = 0; i < len; i++) {
    //         record = this.objectAt(i);
    //         if (!observedRecords.contains(record)) {
    //             record.addObserver('status', this, this.notifyStatusChange);
    //             this.invokeOnce(this.notifyStatusChange);
    //             observedRecords.pushObject(record);
    //         }
    //     }
    // }.observes('[]'),

    // refresh: function() {
    //     var length = this.get('length');
    //     for (i = 0; i < length; i++) {
    //         var record = this.objectAt(i);
    //         record.refresh();
    //     }
    // },

    // notifyStatusChange: function() {
    //     this.notifyPropertyChange('status');
    // },
    // status: function() {
    //     var length = this.get('length');
    //     var maxStatus = 0;
    //     for (i = 0; i < length; i++) {
    //         var status = this.objectAt(i).get('status');
    //         maxStatus = status > maxStatus ? status : maxStatus;
    //     }
    //     return maxStatus || SC.Record.EMPTY;
    // }.property().cacheable()
});
