/**
 *
 * Created with PyCharm.
 * User: calthorpe
 * Date: 9/9/13
 * Time: 11:53 AM
 * To change this template use File | Settings | File Templates.
 */

function isLightColor(color) {
    var rVal = color.substring(1,3);
    var gVal = color.substring(3,5);
    var bVal = color.substring(5,7);

    var grayscale = (parseInt(rVal,16) + parseInt(gVal,16) + parseInt(bVal,16))/3;
    return (grayscale < 150) ? false : true;
}
