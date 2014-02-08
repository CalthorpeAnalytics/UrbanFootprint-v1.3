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

sc_require('models/footprint_record');
sc_require('models/key_mixin');
sc_require('models/name_mixin');

Footprint.Medium = Footprint.Record.extend(Footprint.Key, Footprint.Name, {
    name: SC.Record.attr(String),
    description: SC.Record.attr(String),
    key: SC.Record.attr(String),
    url: SC.Record.attr(String),
    content_type: SC.Record.attr(String),
    content: SC.Record.attr(Object),
    /**
     * Since keys need to be unique when cloning, we generate unique key
     */
    _mapAttributes: {
        key:function(key) { return '%@__%@'.fmt(key, Math.random()*10e6);}
    }
});
