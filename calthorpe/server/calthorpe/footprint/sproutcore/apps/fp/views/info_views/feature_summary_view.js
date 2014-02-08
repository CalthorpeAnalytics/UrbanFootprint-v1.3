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

sc_require('views/info_views/info_view');


Footprint.FeatureSummaryView = Footprint.InfoView.extend({
    classNames: "footprint-feature-summary-view".w(),
    classes: ['footprint-feature-summary-view'],
    layout: {height: 150},

    title: 'Feature Summary',
    count: null,
    columns: null,
    selection: null,
    recordType: null,

    contentView: SCTable.TableView.design({
        layout: {left: 0.01, right: 0.02, height: 0.83, top: 0.07},

        _content:null,
        _contentBinding: SC.Binding.oneWay('.parentView.content').transform(function(value) {
            return value || []
        }),
        _status:null,
        _statusBinding: SC.Binding.oneWay('.parentView*content.status'),

        content:function() {
            if (!this.get('recordType') || !this.get('_content') || !(this.get('_status') & SC.Record.READY))
                return [];
            var mapProperties = this.get('recordType').mapProperties();
            var sortedProperties = this.getPath('sortedProperties');
            return this.get('_content').map(function(item) {
                return mapToSCObject(sortedProperties, function(key) {
                    var path = mapProperties.getPath(key);
                    return [key, path ? item.getPath(path) : item.get(key)];
                });
            }, this);
        }.property('recordType', '_content', '_status').cacheable(),

        selectionBinding: '.parentView.selection',
        recordType: null,
        recordTypeBinding: SC.Binding.oneWay('.parentView.recordType'),

        columns: function () {
            if (this.get('recordType')) {
                var recordType = this.get('recordType');
                // Sort the keys by the propertySortPriority if there is one
                var sortedProperties = this.get('sortedProperties');
                return sortedProperties.map(function (key) {
                    return SC.TableColumn.create({
                        name: key, //.capitalize().replace(/_/g, ' ').split('.').slice(-1)[0],
                        valueKey: key,
                        width: 150
                    });
                });
            }
            return [];
        }.property('recordType').cacheable(),

        sortedProperties: function() {
            var recordType = this.get('recordType');
            if (!recordType)
                return [];
            var properties = recordType.allRecordAttributeProperties();
            var priorityProperties = recordType.priorityProperties().copy() || [];
            var excludeProperties = recordType.excludeProperties().copy() || [];
            return priorityProperties.concat(properties.removeObjects(priorityProperties).removeObjects(excludeProperties));
        }.property('recordType')
    })
});
