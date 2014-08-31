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
    statusBinding: SC.Binding.oneWay('*record.status'),

    createNestedRecord: function(recordType, attributes) {
        this.pushObject(attributes);
        return this.get('lastObject');
    }

});
