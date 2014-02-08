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

/**
 *  A Library of functional extensions to jquery to be created as needed.
 *  Functions and methods can be created as follows:
 *
 *  $.fn.extend({
 *	    myMethod: function(){...}
 *	});
 *	//jQuery("div").myMethod();
 *
 *	$.extend({
 *	    myFunction: function(){...}
 *	});
 *	//jQuery.myFunction();
 */

$.extend({
    /**
     * dualMap allows two equal length collections to be mapped in parallel
     */
    dualMap: function(array1, array2, func) {
        if (array1.length != array2.length) {
            throw new Error($.format("Array lengths are not equal. array1:{0}, array2:{1}",
                array1.length,
                array2.length));
        }
        $.map(array1, function(value, index) {
           return func(value, array2[index]);
        });
    }
});

$.extend({
    /**
     * dualMapToDictionary maps two arrays to keys and values, respectively. The array must be the same length.
     */
    dualMapToDictionary: function(array1, array2) {
        if (array1.length != array2.length) {
            throw new Error($.format("Array lengths are not equal. array1:{0}, array2:{1}",
                array1.length,
                array2.length));
        }
        return $.mapToDictionary(array1, function(value, index) {
            return [value, array2[index]];
        });
    }
});

$.extend({
    /* Maps each value to a two item array which becomes a key value of a hash. Duplicates are overriden.
    *  func optionall maps the item to two other values, returning a two item array
    */
    mapToDictionary: function(array, func) {
        func = func || function(a) { return a;}
	    var hash = {};
        $.each(array, function(index, value) {
	       var result = func(value, index);
           if (result)
             hash[result[0]] = result[1]
        });
	    return hash;
    },

    /**
     * Maps the array to a function that returns a list of values where each value represents a dimension of the result hash,
     * except for the last value which represents the value of the inner most hash.
     * Thus three function returning ['a','b','c'], ['a','d','e'], ['b','f','g']
     * create a hash {a:{b:c}, a:{d:e}, b:{f:g}}
     * Duplicates are overwritten
     * @param array
     * @param func
     * @return {Object}
     */
    mapToMultiDimensionalDictionary: function(array, func) {
        var hash = {};
        $.each(array, function(index, value) {
            results = func(value, index);
            $.addDeep(hash, results)
        });
        return hash;
    }
});

$.extend({
    arrayOrIfEmpty: function(array, defaultArray) {
        return array.length > 0 ? array : defaultArray;
    }
})

// **************************************************************************
// Copyright 2007 - 2009 Tavs Dokkedahl
// Contact: http://www.jslab.dk/contact.php
//
// This file is part of the JSLab Standard Library (JSL) Program.
//
// JSL is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation; either version 3 of the License, or
// any later version.
//
// JSL is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program. If not, see <http://www.gnu.org/licenses/>.
// ***************************************************************************

// Return new array with duplicate values removed
// Modified to extend jQuery instead of Array
$.extend({
    uniqueItems: function(array) {
        var a = [];
        var l = array.length;
        for(var i=0; i<l; i++) {
            for(var j=i+1; j<l; j++) {
                // If this[i] is found later in the array
                if (array[i] === array[j])
                    j = ++i;
            }
            a.push(array[i]);
        }
        return a;
    },
    lastItem: function(array) {
        return array[array.length-1];
    },
    /**
     *  Prepends prepend to the given string if it doens't already begin with prepend. Useful for adding a # to a color string
     * @param string
     * @param prepend
     * @return {*}
     */
    prependIfNeeded: function(string, prepend) {
        return string.indexOf(prepend)==0 ? string : prepend+string;
    },
    /**
     * Rounds a float to the given number of decimals by multiplying-dividing it
     * @param floaty
     * @param decimals
     * @return {Number}
     */
    roundFloat: function(floaty, decimals) {
        return Math.round(floaty*Math.pow(10,decimals))/Math.pow(10,decimals);
    },
    /**
     * Returns the first and last elements of the given array as a two element array
     * @param array
     * @return {Array}
     */
    extremes: function(array) {
        return [array[0], array[array.length-1]];
    },
    /**
     * Shallow flatten an array of arrays. This just uses $.map with the identity function,
     * since jQuery's map shallow flattens results.
     * @param array
     */
    shallowFlatten: function(array) {
        return $.map(array, function(a) {return a;});
    },
    deepEquals: function(a, b) {
        var result = true;

        function typeTest(a, b) {return (typeof a == typeof b)}

        function test(a, b) {
            if (!typeTest(a, b)) return false;
            if (typeof a == 'function' || typeof a == 'object') {
                for (var p in a) {
                    result = test(a[p], b[p]);
                    if (!result) return false;
                }
                return result;
            }
            return (a == b);
        }
        return test(a, b);
    }
});

$.extend({
    has: function(array, v) {
        for (i=0;i<array.length;i++){
            if (array[i]==v) return i;
        }
        return false;
    },
    addDeep: function(hash, dimensions) {
        current = hash;
        last_key = null;
        $.each(dimensions, function(i, dimension) {
           if (i==dimensions.length-1) {
                current[last_key] = dimension
           }
           else if (!current[dimension]) {
               current[dimension] = {};
               current = current[dimension];
               last_key = dimension;
           }
        });
    }
});

String.prototype.capitalize = function() {
    return this.replace(/(?:^|\s)\S/g, function(a) { return a.toUpperCase(); });
};

$.fn.extend ({
    /**
     * Calls the given getter function (e.g. 'width') indicated by a string on each parent until the value isn't null
     * @param item
     * @param getter
     */
    ancestorNonZeroValue: function(getter) {
       var value = this[getter]();
       return (value != 0) ? value : this.parent().ancestorNonZeroValue(getter);
    }
});
$.fn.htmlClean = function() {
    this.contents().filter(function() {
        if (this.nodeType != 3) {
            $(this).htmlClean();
            return false;
        }
        else {
            return !/\S/.test(this.nodeValue);
        }
    }).remove();
}

/* Extend jQuery with functions for PUT and DELETE requests. (http://homework.nwsnet.de/news/9132_put-and-delete-with-jquery */

function _ajax_request(url, data, callback, type, method) {
    if (jQuery.isFunction(data)) {
        callback = data;
        data = {};
    }
    return jQuery.ajax({
        type: method,
        url: url,
        data: data,
        success: callback,
        dataType: type
    });
}

$.extend({
    put: function(url, data, callback, type) {
        return _ajax_request(url, data, callback, type, 'PUT');
    },
    delete: function(url, data, callback, type) {
        return _ajax_request(url, data, callback, type, 'DELETE');
    }
});
