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

sc_require('models/presentation_models');

/***
 * The API delivers presentations by type so that we don't have to deal with mixed inheritance in a flat list
 * TODO We should make the map presentations of type Map and abstract Presentation (both here and on the server)
 * @type {{maps: (SC.ManyAttribute|SC.ChildrenAttribute), results: (SC.ManyAttribute|SC.ChildrenAttribute)}}
 */

Footprint.PresentationTypes = Footprint.Record.extend({
    _internal:YES,
    layers: SC.Record.toMany('Footprint.LayerLibrary', {
        isMaster:YES,
        nested: YES
    }),
    results: SC.Record.toMany('Footprint.ResultLibrary', {
        isMaster:YES,
        nested: YES
    }),
    _cloneProperties: function() { return 'layers results'.w(); }
});
