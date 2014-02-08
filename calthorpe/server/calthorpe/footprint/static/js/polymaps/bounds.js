// Based upon polymaps example bounds.js

function load(e) {
  map.extent(bounds(e.features)).zoomBy(-.5);
}

function bounds(features) {
  var i = -1,
      n = features.length,
      geometry,
      bounds = [{lon: Infinity, lat: Infinity}, {lon: -Infinity, lat: -Infinity}];
  while (++i < n) {
    geometry = features[i].data.geometry;
    boundGeometry[geometry.type](bounds, geometry.coordinates);
  }
  return bounds;
}

function boundPoint(bounds, coordinate) {
  var x = coordinate[0], y = coordinate[1];
  if (x < bounds[0].lon) bounds[0].lon = x;
  if (x > bounds[1].lon) bounds[1].lon = x;
  if (y < bounds[0].lat) bounds[0].lat = y;
  if (y > bounds[1].lat) bounds[1].lat = y;
}

function boundPoints(bounds, coordinates) {
  var i = -1, n = coordinates.length;
  while (++i < n) boundPoint(bounds, coordinates[i]);
}

function boundMultiPoints(bounds, coordinates) {
  var i = -1, n = coordinates.length;
  while (++i < n) boundPoints(bounds, coordinates[i]);
}

var boundGeometry = {
  Point: boundPoint,
  MultiPoint: boundPoints,
  LineString: boundPoints,
  MultiLineString: boundMultiPoints,
  Polygon: function(bounds, coordinates) {
    boundPoints(bounds, coordinates[0]); // exterior ring
  },
  MultiPolygon: function(bounds, coordinates) {
    var i = -1, n = coordinates.length;
    while (++i < n) boundPoints(bounds, coordinates[i][0]);
  }
};
