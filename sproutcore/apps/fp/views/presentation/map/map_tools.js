
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

Footprint.MapTools = SC.Object.extend({

    /***
     * A reference to the mapView that these tools interact with
     */
    mapView:null,
    /***
     * Point brush
     */
    pointbrush:null,
    /***
     * A d3 polygon selection bush
     */
    polybrush:null,
    /**
     * A d3 rectangle selection brush
     */
    rectanglebrush:null,

    init: function() {
        this.set('polybrush', this.initPolygonBrush());
        this.set('rectanglebrush', this.initRectangleBrush());
        this.set('pointbrush', this.initPointBrush());
    },

    initPolygonBrush: function() {
        var self = this;
        return Footprint.BrushTool.create({
            mapView: this.get('mapView'),
            brush:this._initBrush(d3.svg.polybrush),
            selector:'.polybrush',
            /***
             * Returns the closed polygon geometry based on the current points selected by the tool
             * @returns {*}
             */
            geometry:function() {
                var coordinates = [];
                var polybrush = d3.select(".polybrush");
                var polybrushNodes = polybrush.data()[0];
                if (!polybrushNodes)
                    return;

                for (var i=0; i < polybrushNodes.length; i++ ) {
                    var coord = new jsts.geom.Coordinate(polybrushNodes[i][0], polybrushNodes[i][1]);
                    coordinates.push(coord);
                }

                // adds the first node as the last node, closing the polygon shell
                coordinates.push(new jsts.geom.Coordinate(polybrushNodes[0][0], polybrushNodes[0][1]));
                return self.polygonFromLinearRing(coordinates);
            },

            toString: function() {
                return 'Footprint.PolygonBrushTool';
            }
        });
    },

    initRectangleBrush: function() {
        var self = this;
        return Footprint.BrushTool.create({
            mapView: this.get('mapView'),
            brush:this._initBrush(d3.svg.brush),
            selector:null, // not needed currently
            /***
             * Creates the polygon geometry from the rectangle
             * @returns {*}
             */
            geometry: function() {
                var extent = this.get('brush').extent();
                var bbox0 = ([extent[0][0], extent[0][1]]);
                var bbox1 = ([extent[1][0], extent[1][1]]);
                var c1 = new jsts.geom.Coordinate(bbox0[0], bbox0[1]);
                var c2 = new jsts.geom.Coordinate(bbox1[0], bbox0[1]);
                var c3 = new jsts.geom.Coordinate(bbox1[0], bbox1[1]);
                var c4 = new jsts.geom.Coordinate(bbox0[0], bbox1[1]);
                return self.polygonFromLinearRing([c1,c2,c3,c4,c1]);
            },

            toString: function() {
                return 'Footprint.RectangleBrushTool';
            }
        });
    },
    initPointBrush: function() {
        var self = this;
        return Footprint.BrushTool.create({
            mapView: this.get('mapView'),
            brush:this._initBrush(d3.svg.brush),
            selector:null, // not needed currently
            /***
             * Creates the polygon geometry from the rectangle
             * @returns {*}
             */
            geometry: function() {
                var extent = this.get('brush').extent();
                var coordinate = new jsts.geom.Coordinate(extent[0][0], extent[0][1]);
                return self.projectedPointFromCoordinate(coordinate)
            },

            toString: function() {
                return 'Footprint.PointBrushTool';
            },
            startSelection: function() {
                Footprint.statechart.sendAction('doStartSelection');
                this.get('brush').dragStop();
            }
        });
    },

    /***
     * Converts any number of point coordinates to a polygon. The end coordinates must already be closed
     * @param coordinates
     * @returns {*}
     */
    polygonFromLinearRing: function(coordinates) {
        var shell = geometryFactory.createLinearRing(coordinates);
        return this.projectPolygon(geometryFactory.createPolygon(shell));
    },

    /***
     * Translates the polygon from screen coordinates to map coordinates and returns geojson of the coordinates
     * @param polygon
     * @returns {{type: string, coordinates: Array}}
     */
    projectPolygon: function(polygon) {
        var coordinates = polygon.getCoordinates();
        var map = this.getPath('mapView.map');

        return {
            type: "MultiPolygon",
            coordinates: [[coordinates.map(function(coordinate) {
                var projectedCoordinates = map.pointLocation(coordinate);
                return [projectedCoordinates.lon, projectedCoordinates.lat];
            }, this) ]]
        };
    },

    /***
     * Extract
     * @param multiPolygon
     * @returns {{type: string, coordinates: Array}}
     */
    extentsFromPolygons: function(multiPolygon) {
        // TODO
        var coordinates = multiPolygon.map(function(polygon) {
            polygon.getCoordinates();
        });
    },

    /***
     * Translates the x,y coordinate to the map projection
     * @param coordinate
     * @returns {{type: string, coordinates: Array}}
     */
    projectedPointFromCoordinate: function(coordinate) {

        var map = this.getPath('mapView.map');
        var projectedCoordinate = map.pointLocation(coordinate);

        return {
            type: "Point",
            "coordinates": [
                projectedCoordinate.lon, projectedCoordinate.lat
            ]
        }
    },

    _initBrush: function(brushMaker) {
        var w = window.innerWidth;
        var h = window.innerHeight;
        var self = this;
        return brushMaker()
            .x(d3.scale.identity().domain([0,w]))
            .y(d3.scale.identity().domain([0,h]));
    }
});

 /***
  * Represents a tool used for painting/selection
  * @type {*}
  */
Footprint.PaintTool = SC.Object.extend({

    mapView: null,
    /***
     * The d3.svg tool used for making selections and/or painting
     */
    brush:null,
    /***
     * The selector string to access the svg element holding the tool's path data()
     */
    selector:null,
    /***
     * Returns the path drawn by tool by accessing the data() of the element indicated by the selector
     */
    geometry:function() {

    }
});

 /***
  * Extends PaintTool to add actions based on the d3.svg.brush interface
  * @type {*}
  */
Footprint.BrushTool = Footprint.PaintTool.extend({
    /***
     * Overload init to set up the brush events
     * Brush start clears the activeLayerSelection
     */
    init:function() {
        sc_super();
        var self = this;
        this.get('brush')
            .on('brushstart', function() {
                // Clear the activeLayerSelection's geometry when we start.
                // TODO this could also be additive or a continuation of the previous polygon
                SC.run(self.startSelection, self);
            })
            .on('brush', function() {
                SC.run(self.addToSelection, self);
            })
            .on('brushend', function() {
                SC.run(self.endSelection, self);
            })
        Footprint.statechart.sendAction('doCancelLayerSelectionUpdate');
    },

    startSelection: function() {
        Footprint.statechart.sendAction('doStartSelection');
    },

    addToSelection: function() {
        Footprint.statechart.sendAction('doAddToSelection');
    },

    endSelection: function() {
        Footprint.statechart.sendAction('doEndSelection');
    }
});
