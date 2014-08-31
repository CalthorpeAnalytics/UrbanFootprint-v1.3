 /*
* UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
*
* Copyright (C) 2014 Calthorpe Associates
*
* This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
*
* This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
*
* Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
*/

sc_require('system/array_status');

SC.ManyArray.reopen(SC.ArrayStatus, {

    refresh: function() {
      var length = this.get('length');
      for (i = 0; i < length; i++) {
          var record = this.objectAt(i);
          record.refresh();
      }
    },

    toString: function() {
      return sc_super() + "\n---->" +
          this.map(function(item) {
              return item.toString()
          }, this).join("\n---->");
    }
});
