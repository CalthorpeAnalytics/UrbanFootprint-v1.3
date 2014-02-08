/**
 * Created by calthorpe on 12/16/13.
 */

// TODO these should be mixed into SC.Observable
/***
 * short-cut to getPath
 * @param obj
 * @param path
 * @returns {*}
 */
function g(obj, path) {
    return obj.getPath(path);
}
/***
 * short-cut to status
 * @param obj
 * @param path
 * @returns {*}
 */
function s(obj, path) {
    return path ? obj.getPath(path + '.status') : obj.get('status');
}
/***
 * short-cut to constructor
 * @param obj
 * @param path
 * @returns {*}
 */
function c(obj, path) {
    return path ? obj.getPath(path + '.constructor') : obj.get('constructor');
}
/***
 * short-cut to firstObject.toString()
 * @param obj
 * @param path
 * @returns {*}
 */
function f(obj, path) {
    return (path ? obj.getPath(path + '.firstObject') : obj.get('firstObject')).toString();
}
/***
 * short-cut to firstObject.constructor
 * @param obj
 * @param path
 * @returns {*}
 */
function fc(obj, path) {
    return (path ? obj.getPath(path + '.firstObject.constuctor') : obj.getPath('firstObject.constructor'));
}
/***
 * short-cut to length
 * @param obj
 * @param path
 * @returns {*}
 */
function l(obj, path) {
    return path ? obj.getPath(path + '.length') : obj.get('length');
}

function ts(obj, path) {
    return path ? obj.getPath(path).toString() : obj.toString();
}

function a(record, path) {
    return path ? record.getPath(path + '.attributes') : record.get('attributes')
}

