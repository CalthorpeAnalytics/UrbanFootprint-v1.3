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

//wrapper to an observable that requires accept/cancel
ko.protectObservable = function (observable) {
    //private variables
    var _actualValue = observable;
    var _tempValue = observable();

    //dependentObservable that we will return
    var result = ko.dependentObservable({
        //always return the actual value
        read: function () {
            return _actualValue();
        },
        //stored in a temporary spot until commit
        write: function (newValue) {
            _tempValue = newValue;
        }
    });

    //if different, commit temp value
    result.commit = function () {
        if (_tempValue !== _actualValue()) {
            _actualValue(_tempValue);
        }
    };

    //force subscribers to take original
    result.reset = function () {
        _actualValue.valueHasMutated();
        _tempValue = _actualValue();   //reset temp value
    };

    result.actual = function() {
        return _actualValue;
    };

    return result;
};

ko.isObservableArray = function(obj) {
    return ko.isObservable(obj) && !(obj.destroyAll === undefined);
};
ko.isProtectedObservable = function(obj) {
    return ko.isObservable(obj) && !(obj.commit === undefined);
};

ko.protectObservableArray = function(observableArray) {

    var protectedObservableArray = ko.observableArray($.map(observableArray(), protectItem));
    protectedObservableArray._actual = observableArray;

    function protectItem(observable) {
        return $.isPlainObject(observable) ?
            ko.protect(observable) :
            ko.protectObservable(observable);
    }
    function unprotectItem(protectedObservable) {
        return protectedObservable.actual();
    }

    protectedObservableArray.commit = function () {
        // Commit each item
        var self = this;
        for (var key in self()) {
           self()[key].commit();
        }
        this._actual.removeAll();
        for (var key in self()) {
            self._actual.push(self()[key])
        }
    };

    protectedObservableArray.reset = function () {
        this.removeAll();
        $.each(self._actual(), function(i, item) {
           self.push(protectItem(item))
        });
    };
    protectedObservableArray.actual = function() {
        return self._actual;
    };

    return protectedObservableArray;
};


ko.protect = function (model) {


    //build the new protected model by prototyping from the model
    var protectedModel = Object.create(model) ;
    protectedModel._model = model;

    protectedModel.commit = function () {
        for (var key in this) {
            if (ko.isProtectedObservable(this[key]))
                this[key].commit();
        }
    };

    protectedModel.reset = function () {
        for (var key in this) {
            if (ko.isProtectedObservable(this[key]))
                this[key].reset();
        }
    };

    protectedModel.actual = function() {
        return model;
    };

    protectedModel.protectProperties = function() {
        $.each(model, function(key, property) {
            //only protect writable observables, but also copy other properties
            //so the new protected model can still be data bound
            prop = model[key];
            if (ko.isWriteableObservable(property)) {
                protectedModel[key] = ko.protectProperty(property)
            }
            else {
                protectedModel[key] = property;
            }
        })
    };

    protectedModel.protectProperties(model, protectedModel);
    return protectedModel;
};

ko.protectProperty = function(prop) {
    if (ko.isObservableArray(prop)) {
        return ko.protectObservableArray(prop)
    }
    else if ($.isPlainObject(prop)) {
        return ko.protect(prop)
    }
    return ko.protectObservable(prop);
};
