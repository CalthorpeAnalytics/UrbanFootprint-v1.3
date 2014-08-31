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

// NOTE that this is a temporary construct to allow the mapGroupsLayerController to do its thing
// based on future plans. Eventually, visible attributes will presumably be their own records. To
// maintain downstream compatibility, those records must expose the visible attribute's name on
// 'name' and its parent layer at 'layer'.

Footprint.visibleAttributesController = SC.ArrayController.create({
    layers: null,
    layersBinding: SC.Binding.oneWay('Footprint.layersVisibleForegroundController.arrangedObjects'),
    layersDidChange: function() { this.invokeOnce('doUpdateContent'); }.observes('*layers.@each.visible'),
    doUpdateContent: function() { this.notifyPropertyChange('content'); },
    content: function() {
        var ret = [];
        // For each layer,
        (this.get('layers') || SC.EMPTY_ARRAY).forEach(function(layer) {
            // for each of its visible attributes,
            (layer.get('visible_attributes') || SC.EMPTY_ARRAY).forEach(function(visibleAttribute) {
                // create an entry in ret.
                ret.push(SC.Object.create({
                    name: visibleAttribute,
                    layer: layer
                }))
            })
        });
        return ret;
    }.property()
});
