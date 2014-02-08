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

function remove_keys_matching_object(obj, other_obj) {
    var keys = $.map(other_obj, function(v,k) {return k;});
    return remove_keys(obj, keys);
}
function remove_keys(obj, keys) {
    var results = {}
    $.each(obj, function(k,v) {
        if (!keys.contains(k))
            results[k] = v;
    });
    return results;
}
function filter_keys(obj, keys) {
    if (obj.kindOf)
        return mapToSCObject(keys, function(key) {
            return obj.get(key) != undefined ? [key, obj.get(key)] : null;
        });
    else {
        var results = {}
        $.each(obj, function(k,v) {
            if (keys.contains(k))
                results[k] = v;
        });
        return results;
    }
}

var statusLookup = null;
function getStatusString(status) {
    statusLookup = statusLookup || $.mapToDictionary($.grep(
        $.map(SC.Record, function(key,value) {
            return [[key, value]]; }),
        function(a) { return a[1].match(/^[A-Z_]+$/) != null; }
    ));
    return statusLookup[status] || "Unmatched status: %@".fmt(status);
}

function logProperty(property, propertyName, dependentPropertyName) {
    if (dependentPropertyName) {
        SC.Logger.debug("%@: %@ observing %@ with value %@ and status %@",
            new Date(),
            dependentPropertyName,
            propertyName,
            property,
            property ? (property.status ? getStatusString(property.get('status')) : 'no status') : 'no property');
    }
    else {
        SC.Logger.debug("%@: property %@ with value %@ and status %@",
            new Date(),
            propertyName,
            property,
            property ? (property.status ? getStatusString(property.get('status')) : 'no status') : 'no property');
    }
}
function logStatus(property, propertyName, dependentPropertyName) {
    if (dependentPropertyName) {
        SC.Logger.debug("%@: %@ observed change to %@: Observed status: %@", new Date(), dependentPropertyName, propertyName,
            property ? getStatusString(property.get('status')) : 'Property undefined!');
    }
    else {
        SC.Logger.debug("%@: Status of property %@ is: %@", new Date(), propertyName,
            property ? getStatusString(property.get('status')) : 'Property undefined!');
    }
}
function logDidFetch(recordType) {
    SC.Logger.debug("%@: Did fetch recordType: %@", new Date(), recordType.toString());
}
function logDidCachedFetch(recordType) {
    SC.Logger.debug("%@: Did cached fetch recordType: %@", new Date(), recordType.toString());
}
function logCached(recordType) {
    SC.Logger.debug("%@: Added recordType %@ to the cache", new Date(), recordType.toString());
}

function logCount(property, propertyName) {
    SC.Logger.debug("Property %@, length %@", propertyName,
        property ? (typeof(property.length) == 'function' ? property.length() : property.length) : "null!");
}

function logWarning(error) {
    SC.Logger.warn(error.message || error || "Unknown Error");
    if (error.stack)
        SC.Logger.error(error.stack);
}

function logError(error) {
    SC.Logger.error(error.message || error || "Unknown Error");
    if (error.stack)
        SC.Logger.error(error.stack);
}

function logInfo(message) {
    SC.Logger.info(message);
}

/***
 * Asserts that the given state is one of the current states (or the current state)
 * @param state
 */
function assertCurrentState(state) {
    ok($.any(Footprint.statechart.currentStates(), function(state) {
        return state.kindOf(Footprint.LoadingApp);
    }),
    "Expect current state to be Footprint.statechart.loadingApp. Actual state(s): %@".fmt(Footprint.statechart.currentStates().join(', ')));
}
/**
 * Assert the given property is not null
 * @param propertyValue: the evaluated property
 * @param propertyName: the name of the property
 */
function assertNotNull(propertyValue, propertyName) {
    ok(null != propertyValue, "Expect %@ not null".fmt(propertyName));
}
function assertNull(propertyValue, propertyName) {
    ok(null != propertyValue, "Expect %@ to be null, but was %@".fmt(propertyName, propertyValue));
}

function assertStatus(property, status, propertyName) {

    assertNotNull(property, propertyName);
    equals(
        property.get('status'),
        status,
        "For property %@, expect status %@. Actual status: %@. Property value:".fmt(
            propertyName,
            getStatusString(status),
            getStatusString(property.get('status')),
            property.toString()));
}
function assertNonZeroLength(value, propertyName) {
    var length = typeof(value.length) == 'function' ? value.length() : value.length
    ok(length,
       'Expect non-zero items for %@. Actual %@'.fmt(propertyName, length));
}

function assertLength(expectedLength, property, propertyName) {
    length = typeof(property.length) == 'function' ? property.length() : property.length
    equals(expectedLength, length,
        'Expect %@ items for %@. Actual %@'.fmt(expectedLength, propertyName, length));
}

function assertEqualLength(expectedLength, actualLength, propertyName) {
    equals(expectedLength, actualLength,
        'Expected %@ items for %@. Actual %@'.fmt(expectedLength, propertyName, length));
}

function assertKindForList(type, property, propertyName) {
    var list = typeof(property.length) == 'function' ? property.toArray() : property;
    $.each(list, function(i, item) {
        ok(item.kindOf(type), 'Expected items of type %@ for %@. Actual [%@]'.fmt(
            type.toString(), propertyName, $.map(list, function(item, i) { return item.toString()}).join(';')));
    })
}

//http://stackoverflow.com/questions/3115982/how-to-check-javascript-array-equals
function normalEquals(array) {
    return array.every(function(x){return x==array[0]});
}
function zip(arrays) {
    return arrays[0].map(function(_,i){
        return arrays.map(function(array){return array[i]})
    });
}
function type(x) {
    return Object.prototype.toString.call(x);
}
function allTrue(array) {
    return array.reduce(function(a,b){return a&&b},true);
}
function deepEquals(things) {
    if( type(things[0])==type([])
        && normalEquals(things.map(type))
        && normalEquals(things.map(function(x){return x.length})) )
        return allTrue(zip(things).map(superEquals));
    else
        return normalEquals(things);
}

function dumpParentViews(view) {
    function _dump(view) {
        if (!view || view.kindOf(SC.MainPane) )
            return [view ? view.toString() : 'null'];
        else
            return [view.toString()].concat(_dump(view.get('parentView')));
    }
    return _dump(view).join("\n\n");
}

/***
 * Return the parentView at the index number
 * @param index
 */
function getParentView(view, index) {
    if (index > 0)
        return getParentView(view.get('parentView'), index-1);
    else
        return view;
}

function findParentViewByKind(view, clazz) {
    var parentView = view.get('parentView');
    if (!parentView) {
        return null;
    }
    else if (parentView.kindOf(clazz)) {
        return parentView;
    }
    else {
        return findParentViewByKind(parentView, clazz)
    }
}

function firstOrNull(array) {
    return array.length > 0 ? array[0] : null
}
// For some reason the SC.View.views array doesn't contain all the views. Use this to find relative to a known view
function findChildView(view, viewId) {
    return firstOrNull($.map(view.childViews || [], function(childView) {
        if (childView.$().attr('id')==viewId) {
            return childView;
        }
        else {
            return findChildView(childView, viewId)
        }
    }))
}

function findChildViewByKind(view, clazz) {
    return firstOrNull($.map(view.childViews || [], function(childView) {
        if (childView.kindOf(clazz)) {
            return childView;
        }
        else {
            return findChildViewByKind(childView, clazz)
        }
    }));
}

function findViewsByKind(clazz) {
    return $.grep($.values(SC.View.views), function(value) {
        return value.kindOf(clazz);
    });
}
function findChildViewsByKind(view, clazz) {
    var self = this;
    return $.map(view.childViews || [], function(childView) {
        if (childView.kindOf(clazz)) {
            return childView;
        }
        else {
            return self.findChildViewsByKind(childView, clazz)
        }
    });
}

function mouseClick(target) {
    if (!target)
        throw "view is null";
    SC.Event.trigger(target, "mousedown");
    SC.Event.trigger(target, "mouseup");
    SC.RunLoop.begin();
    SC.RunLoop.end();
}

function mouseDoubleClick(target) {
    SC.Event.trigger(target, "mousedown");
    SC.Event.trigger(target, "mouseup");
    SC.Event.trigger(target, "mousedown");
    SC.Event.trigger(target, "mouseup");
    SC.RunLoop.begin();
    SC.RunLoop.end();
}

function keyboardEnterClick(target) {
    var event = SC.Event.simulateEvent(target, "keydown", {
        which: 13,
        keyCode: 13
    });
    SC.Event.trigger(target, "keydown", event);
    event = SC.Event.simulateEvent(target, "keyup", {
        which: 13,
        keyCode: 13
    });
    SC.Event.trigger(target, "keyup", event);
    SC.RunLoop.begin();
    SC.RunLoop.end();
}

/***
 * Edits the text of the given labelView, adding __Test to the current value
 * @param labelView
 */
function editLabel(labelView, pane) {
    var parentView = labelView.get('parentView');
    var target = labelView.$().get(0);
    mouseDoubleClick(target);
    var input = parentView.$('input')[0] || (pane && pane.$('.inline-editor').find('input')[0]);
    if (!input) {
        ok(false, "Failed to invoke inline-editor with double click");
    }
    else {
        var value = labelView.get('value');
        input.value = '%@__Test'.fmt(value);
        keyboardEnterClick(target);
        parentView.$().css('position', 'relative');
    }
}

function updateNameAndValidate(pane, nameView, content, i) {
    equals(
        content.get('name'),
        nameView.get('value'),
        'Expecting a name for item index %@, representing instance %@'.fmt(i, content.toString()));
    var name = nameView.get('value');
    var updatedName = '%@__Test'.fmt(name);
    editLabel(nameView, pane);
    equals(
        updatedName,
        nameView.get('value'),
        'Expecting a view name to be updated to %@ for item index %@, representing instance %@'.fmt(updatedName, i, content.toString()));
    equals(
        updatedName,
        nameView.$().text(),
        'Expecting a view label text to be updated to %@ for item index %@, representing instance %@'.fmt(updatedName, i, content.toString()));
}

/***
 * Simply returns 'parentView' concatinated by strings for the number of times needed. A period is placed at the start but not at the end
 * @param times
 * @param path: the path to append to the parentView string
 */
function parentViewPath(times, path) {
    return '.'+$.map(new Array(times), function(x) { return 'parentView'}).join('.')+path;
}

/***
 * Vefiry that the given object is a SC.Object derivative of the specified kind
 * @param obj
 * @param kind SC.Object derived class.
 * @returns {*|Boolean}
 */
function isSCObjectOfKind(obj, kind) {
    return obj && obj.kindOf && obj.kindOf(kind);
}

/***
 * Joins all non-null path segments with a '.'. This is useful when some segments might be null
 * @param segments
 */
function formPropertyPath(segments) {
   return segments.map(function(segment) { return  segment || null }).compact().join('.')
}

/***
 * Inspects the item, which might be a Sproutcore Array and converts it to an normal array.
 * For non-arrays, the item is wrapped as an array
 * @param array
 * @returns {*}
 */
function arrayOrItemToArray(array) {
    if (!array)
        return []
    if (array.isEnumerable)
        return array.toArray();
    else
        return [array];
}

function arrayIfSingular(array) {
   return array.isEnumerable ? array : [array];
}
function firstIfArray(array) {
    return array.isEnumerable ? array.get('firstObject') : array;
}
function singularize(array) {
    if (array && array.isEnumerable && array.get('length') != 1) {
        throw Error("Attempt to singularize an array with 0 or > 1 values: %@".fmt(array))
    }
    return array && array.isEnumerable ? array.get('firstObject') : array;
}
/***
 * Returns true if the given item is one of the SC Array types
 * @param array
 * @returns {*|Boolean}
 */
function isSCArray(array) {
    return (array.kindOf && (array.kindOf(SC.Enumerable) || array.kindOf(SC.ChildArray) || array.kindOf(SC.ManyArray) || array.kindOf(SC.RecordArray) ));
}

/***
 * Returns an ObjectController with the content property made into an array if needed
 * @param context - Any number of objects
 */
function toArrayController() {
    if (!arguments.length > 0 || !arguments[0]) {
        logError("toArrayController called without context or a null context. You probably didn't want to do this. Returning an empty ArrayController");
        return SC.ArrayController.create();
    }
    // Merge the arguments
    var arrayController = SC.ArrayController.create.apply(SC.ArrayController, arguments);
    // Make sure any content is an array
    if (arrayController.get('content'))
        arrayController.set('content', arrayIfSingular(arrayController.get('content')));
    return arrayController;
}

/***
 * Maps an array of values with a function that returns a two-item array. The first item is the attribute name, the second is the mapped value
 * Returns a new SC.Object instance with those attributes and values
 * @param array
 * @param func
 * @returns {*}
 */
function mapToSCObject(array, func, target) {
    return SC.Object.create($.mapToDictionary(array, func, null, target));
}
function mapObjectToSCObject(array, func, target) {
    return SC.Object.create($.mapObjectToObject(array, func, null, target));
}

/***
* Returns the unique recordTypes for the given records of the given store
 */
function uniqueRecordTypes(store, records) {
    return records.map(function(record) {
        return store.recordTypeFor(record.get('storeKey'));
    }, this).uniq()
}

/***
 * Change a record's status to the toStatus if it matches the fromStatus.
 * This only works in limited situations, e.g. ERROR to DIRTY.
 * @param store
 * @param record
 * @param fromStatus
 * @param toStatus
 */
function changeRecordStatus(store, record, fromStatus, toStatus) {
    if (record.get('status') === fromStatus) {
        record.propertyWillChange('status');
        store.writeStatus(record.get('storeKey'), toStatus);
        record.propertyDidChange('status');
    }
}

function getCallStackDuplicateSize(start, max, match) {
    max = max || 50;
    start = start || 0
    var count = 0, fn = arguments.callee;
    while (start-- > 0)
        fn = fn.caller;
    while ( (fn = fn.caller) ) {
        if (!fn.toString().match(match))
            break;
        SC.Logger.debug(fn.toString());
        count++;
        if (count > max) {
            logError('getCallStackSize over %@'.fmt(max));
            break;
        }
    }
    return count;
}

function getCallStackSize(max) {
    max = max || 50;
    var count = 0, fn = arguments.callee;
    while ( (fn = fn.caller) ) {
        count++;
        if (count > max)
            logError('getCallStackSize over %@'.fmt(max));
    }
    return count;
}

function mapProperties(content, keys) {
    return content.map(function (next) {
        return keys.map(function(key) {
            return next ? (next.get ? next.get(key) : next[key]) : null;
        });
    });
}
