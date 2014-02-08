
 /* 
* UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
* 
* Copyright (C) 2012 Calthorpe Associates
* 
* This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
* 
* This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
* 
* You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
* 
* Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
 */

SC.Controller.reopen({
    /***
     * Adds the ability to quickly dump fields and properties for debugging.
     * content isn't technically defined on SC.Controller but I assume callers will be extending SC.Object or SC.Array
     * @returns {*}
     */
    dump: function() {
        return "content: %@".fmt(this.get('content'));
    }
});

SC.ArrayController.reopen({
  status: function() {
    var content = this.get('content'),
        ret = content ? content.get('status') : null;
    return ret ? ret : SC.Record.EMPTY;
  }.property().cacheable()
});

SC.ManyArray.reopen({

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
          record.removeObserver('status', this, this.notifyStatusChange);
          observedRecords.removeObject(record);
        }
      }
      // If any item in content is not in observedRecords, observe them.
      len = this.get('length');
      for (i = 0; i < len; i++) {
        record = this.objectAt(i);
        if (!observedRecords.contains(record)) {
          record.addObserver('status', this, this.notifyStatusChange);
          this.invokeOnce(this.notifyStatusChange);
          observedRecords.pushObject(record);
        }
      }
    }.observes('[]'),

    notifyStatusChange: function() {
        this.notifyPropertyChange('status');
    },
    status: function() {
        var length = this.get('length');
        var maxStatus = 0;
        for (i = 0; i < length; i++) {
            var status = this.objectAt(i).get('status');
            maxStatus = status > maxStatus ? status : maxStatus;
        }
        return maxStatus || SC.Record.EMPTY;
    }.property().cacheable()
});

 SC.ChildArray.reopen({

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
                 record.removeObserver('status', this, this.notifyStatusChange);
                 observedRecords.removeObject(record);
             }
         }
         // If any item in content is not in observedRecords, observe them.
         len = this.get('length');
         for (i = 0; i < len; i++) {
             record = this.objectAt(i);
             if (!observedRecords.contains(record)) {
                 record.addObserver('status', this, this.notifyStatusChange);
                 this.invokeOnce(this.notifyStatusChange);
                 observedRecords.pushObject(record);
             }
         }
     }.observes('[]'),

     notifyStatusChange: function() {
         this.notifyPropertyChange('status');
     },
     status: function() {
         var length = this.get('length');
         var maxStatus = 0;
         for (i = 0; i < length; i++) {
             var status = this.objectAt(i).get('status');
             maxStatus = status > maxStatus ? status : maxStatus;
         }
         return maxStatus || SC.Record.EMPTY;
     }.property().cacheable()
 });
