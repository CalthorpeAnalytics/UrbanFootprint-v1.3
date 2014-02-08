
/*
* UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
* 
* Copyright (C) 2013 Calthorpe Associates
* 
* This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
* 
* This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
* 
* You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
* 
* Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
*/

sc_require('models/presentation_medium_model');

// Result is a subclass class that supports charts and grids
Footprint.Result = Footprint.PresentationMedium.extend({
});

// A grid (table) result based on a data table, view, or query
Footprint.Grid = Footprint.Result.extend();
// A chart result based on a data table, view, or query
Footprint.Chart = Footprint.Result.extend();
// A chart that is displayed on a map as one or more layers
Footprint.LayerChart = Footprint.Result.extend();

// ResultLibrary is configuration of various results
Footprint.ResultLibrary = Footprint.Presentation.extend({
    // We currently use the results attribute instead of presentation_media. In theory Sproutcore supports subclassing on nested records, so we should be able to use the presentation_media attribute instead of results. A Result is a subclass of PresentationMedium
    results: SC.Record.toMany("Footprint.Result", {
        nested:NO,
        isMaster:YES
    }),

    _copyProperties: function () {
        return sc_super().concat([]);
    },
    _cloneProperties: function () {
         return sc_super().concat(['results']);
    }
});

