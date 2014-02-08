/**
 * Created with PyCharm.
 * User: calthorpe
 * Date: 2/19/13
 * Time: 9:48 AM
 * To change this template use File | Settings | File Templates.
 */

sc_require('resources/polymaps');

$(function() {
    window.geometryFactory = new jsts.geom.GeometryFactory();
    window.rTree =new jsts.index.strtree.STRtree();
    window.reader = new jsts.io.GeoJSONReader();
});

Footprint.geometryController = SC.Object.create({



})