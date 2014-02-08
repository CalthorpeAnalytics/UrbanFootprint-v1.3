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

Footprint.BackupProperties = {
    /**
     * Return an object containing a backup of the properties
     * @returns SC.Object object containing properties to backup
     */
    backupProperties: function() {
        var backup = SC.Object.create();
        for (var i = 0; i < this.properties.length; i++) {
            var p = this.properties[i];
            backup.set(p, this.get(p));
        }
        return backup;
    },

    /**
     * Restores properties from a backup crated by backupProperties().
     */
    restoreProperties: function(backup) {
        for (var i = 0; i < this.properties.length; i++) {
            var p = this.properties[i];
            this.set(p, backup.get(p));
        }
        return;
    }
}
