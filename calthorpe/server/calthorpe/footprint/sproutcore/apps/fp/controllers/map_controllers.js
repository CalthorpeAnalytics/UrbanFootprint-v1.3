
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

 /***
  * A lightweight controller for basic map functionality.
  * @type {Class}
  */
Footprint.mapController = SC.ObjectController.create({

    selectionLayerNeedsRefresh: NO,
    refreshSelectionLayer: function() {
        this.set('selectionLayerNeedsRefresh', YES);
    },
    layerNeedsRefresh:NO,
    refreshLayer: function() {
        this.set('layerNeedsRefresh', YES);
    },

    mapNeedsRezoomToProject:NO,
    resetExtent: function(){
        this.set('mapNeedsRezoomToProject', YES);
    },

    mapLayersNeedZoomUpdate:NO,
    refreshMapLayerZoomVisibility: function() {
        this.set('mapLayersNeedZoomUpdate', YES);
    },

    // Hack set true when map is ready
    isReady:NO
});

 /***
  * A lightweight controller that manages the map tools properties
  * content is A Footprint.MapTools instance (singleton?) for painting, selection, etc. tools for the map
  * This is setup by the view so that the tools can access the map and send actions to the view
  * @type {Class}
  */
Footprint.mapToolsController = SC.ObjectController.create({

    activeMapToolKey:null,
    /**
     * The active paint tool according to activeMapToolKey
     */
    activePaintTool:null,
    activeMapToolKeyObserver: function() {
        var paintToolName = this.get('activeMapToolKey');
        var paintTool = paintToolName ? this.get(paintToolName) : null;
        if (this.get('activePaintTool') !== paintTool)
            this.set('activePaintTool', paintTool);
    }.observes('.activeMapToolKey')
});

