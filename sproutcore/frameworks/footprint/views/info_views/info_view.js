
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
*
* Base class for a editing. Provides a view for the title and the item itself
* @type {Class}
*/
Footprint.InfoView = SC.View.extend({
    childViews:'titleView contentView rangeView'.w(),
    classNames: "footprint-info-view".w(),

    title: null,
    rangeValue: null,
    value:null,
    isEditable:YES,

    titleView: SC.LabelView.extend({
        classNames: "footprint-infoview-title-view".w(),
        layout: {left: 0.01, height: 24, width: 0.3},
        valueBinding: '.parentView.title'
    }),
    // Override this
    contentView: null,

    rangeView: SC.LabelView.extend({
        classNames: "footprint-infoview-range-view".w(),
        layout: {left: .65, width: .3},
        isTextSelectable:YES,
        valueBinding: SC.Binding.oneWay('.parentView.rangeValue'),
        isVisibleBinding:SC.Binding.oneWay('.value').bool()
    }),

    toString: function() {
        return "%@:\n%@".fmt(sc_super(), this.toStringAttributes(this._toStringAttributes()));
    },

    _toStringAttributes: function() {
        return 'title content'.w()
    },

    recordTypeToInfoView: function() {
        return mapToSCObject(Footprint.InfoView.featureInfoViews(Footprint.InfoView), function(infoView) {
            return infoView.prototype.recordType ? [infoView.prototype.recordType, infoView] : null;
        })
    }.property().cacheable()
});

Footprint.InfoView.mixin({
    featureInfoViews: function(clazz) {
        return $.shallowFlatten(clazz.subclasses.map(function (subclass) {
            return [subclass].concat(Footprint.InfoView.featureInfoViews(subclass));
        }, this).compact());
    }
});
