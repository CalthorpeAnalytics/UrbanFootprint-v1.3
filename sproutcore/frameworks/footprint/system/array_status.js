/**
 * Created by calthorpe on 4/7/14.
 */

/***
 * Adds a status to an Array by observing its content
 */
SC.ArrayStatus = {
    status: null,
    // Set up observers.
    contentDidChange: function() {
        var observedRecords = this._observedRecords;
        if (!observedRecords) observedRecords = this._observedRecords = [];
        var record, i, len;
        // If any items in observedRecords are not in content, stop observing them.
        len = observedRecords.length;
        for (i = len - 1; i >= 0; i--) {
            record = observedRecords.objectAt(i);
            if (!this.contains(record)) {
                record.removeObserver('status', this, this.calculateStatus);
                observedRecords.removeObject(record);
            }
        }
        // If any item in content is not in observedRecords, observe them.
        len = this.get('length');
        for (i = 0; i < len; i++) {
            record = this.objectAt(i);
            if (!observedRecords.contains(record)) {
                record.addObserver('status', this, this.calculateStatus);
                this.invokeOnce(this.calculateStatus);
                observedRecords.pushObject(record);
            }
        }
    }.observes('[]'),

    calculateStatus: function() {
        this.invokeOnce(this._calcluateStatus);
    },
    _calcluateStatus: function() {
        var length = this.get('length');
        var maxStatus = 0;
        for (i = 0; i < length; i++) {
            var status = this.objectAt(i).get('status');
            maxStatus = status > maxStatus ? status : maxStatus;
        }
        var status = maxStatus || SC.Record.EMPTY;
        this.setIfChanged('status', status);
    }
};