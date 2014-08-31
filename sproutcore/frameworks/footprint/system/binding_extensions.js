
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

SC.Binding.oneWaySelectionSetSingleFilter = function() {
    return this.transform(function(value, isForward) {
        if (isForward) {
            // The selection has changed, get the first item
            // The _objects property doesn't exist until there is a selection.
            if (value)
                return value._objects ? value._objects[0] : null;
            else
                return value;
        }
    })
};

SC.Binding.singleFilter = function() {
    return this.transform(function(value, isForward) {
        if (isForward) {
            // The selection has changed, get the first item
            // The _objects property doesn't exist until there is a selection.
            if (value)
                return value.firstObject ? value.firstObject() : value[0];
            else
                return value;
        }
    })
};

SC.Binding.matchesStatus = function(status) {
    return this.transform(function(value, isForward) {
        return !!(value && (value & status));
    });
};

SC.Binding.equalsStatus = function(status) {
    return this.transform(function(value, isForward) {
        return value && (value === status);
    });
};

SC.Binding.allMatchStatus = function(status) {
    return this.transform(function(content, isForward) {
        return (content || []).filter(function(item) {
            return (!(item && (item.get('status') & status)))
        }).get('length') == 0
    });
};

SC.Binding.lengthOf = function() {
    return this.transform(function(value, binding) {
        return value ? arrayOrItemToArray(value).length : 0;
    });
};

SC.Binding.isGreaterThan = function (minValue) {
    return this.transform(function (value, binding) {
        return (SC.typeOf(value) === SC.T_NUMBER) && (value > minValue);
    });
};

SC.Binding.notContentKind = function(type) {
    /***
     * Returns true if the value is not a kindOf the type
     */
    return this.transform(function(value, binding) {
        return !(value && value.kindOf(type));
    });
};

/***
 * Compensates for ManyArray's absent status by converting the ManyArray to a RecordArray by querying on the storeKeys.
 * The recordType is induced from the first item of value.
 * @returns The RecordArray matching the ManyArray items.
 */
SC.Binding.convertToRecordArray = function() {
    return this.transform(function(value, binding) {
        if (!value)
            return value;

        var recordType = Footprint.store.recordTypeFor(value.getPath('firstObject.storeKey'));

        return Footprint.store.find(SC.Query.local(
            recordType || SC.Record, {
                conditions: '{storeKeys} CONTAINS storeKey',
                storeKeys:value.mapProperty('storeKey')
            }));
    });
};

SC.Binding.defaultValue = function(defaultValue) {
    return this.transform(function(value, binding) {
        return value || defaultValue;
    });
};

/*** Transforms a Footprint.BuildingUsePercent array to the BuildingUsePercent property value whose BuildingUseDefinition name matches the given category ***/
SC.Binding.propertyTransform = function(property) {
    return this.transform(function(obj) {
        return obj && obj.getPath(property);
    });
}
/*** Transforms the given list to true if it contains the given value ***/
SC.Binding.contains = function(value) {
    return this.transform(function(list) {
        return list && list.contains(value)
    })
}
