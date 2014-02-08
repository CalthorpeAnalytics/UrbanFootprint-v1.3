
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

 Footprint.ControllerMixins = {
    /**
     * Denotes if the data source is ready
     */
    isReady: function() {
        var status = this.get('status');
        return status & SC.Record.READY;
    }.property('status').cacheable(),

    /**
     * Provides a summary of the status of the controller.
     */
    summary: function() {
        var ret = '';

        var status = this.get('status');
        if (status & SC.Record.READY) {
            var len = this.get('length');
            if (len && len > 0) {
                ret = len === 1 ? "1 item" : "%@ items".fmt(len);
            } else {
                ret = "No items";
            }
        }
        if (status & SC.Record.BUSY) {
            ret = "Loading..."
        }
        if (status & SC.Record.ERROR) {
            ret = "Error"
        }
        return ret;
    }.property('length', 'status').cacheable()
};