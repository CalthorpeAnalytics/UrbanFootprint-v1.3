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
sc_require('views/export_view');
sc_require('views/overlay_view');

Footprint.TableInfoView = Footprint.InfoView.extend({
    classNames: "footprint-table-info-view".w(),
    childViews:'titleView zoomToSelectionView tableExportView contentView overlayView'.w(),
    classes: ['footprint-table-info-view'],
    layout: {height: 150},

    title: 'Feature Summary',
    count: null,
    columns: null,
    // SC.Object to map content fields to different column names
    mapProperties:null,
    selection: null,
    recordType: null,
    layerSelection: null,
    // Makes the zoomToSelection conditionally visible
    zoomToSelectionIsVisible: NO,
    // Set this to the status that should make the overlay visible if the status is BUSY
    overlayStatus: null,

    titleView: SC.LabelView.extend({
        classNames: "footprint-infoview-title-view".w(),
        layout: {left: 0.01, height: 24, width: 0.6},
        valueBinding: '.parentView.title'
    }),
    zoomToSelectionView: SC.View.extend({
        classNames: "footprint-table-infoview-zoom-to-selection-view".w(),
        layout: { height: 24, width: 175, right: 150},
        childViews: ['zoomToSelectionLabelView', 'zoomToSelectionButtonView'],
        isVisibleBinding: SC.Binding.oneWay('.parentView.zoomToSelectionIsVisible'),
        isEnabledBinding: SC.Binding.notEmpty('.parentView.layerSelection.features', NO),
        zoomToSelectionLabelView: SC.LabelView.extend({
            classNames: 'footprint-map footprint-map-rezoom-to-extent-label'.w(),
            layout: { height: 24, width: 150, right: 25},
            value: 'Zoom map to selection'
        }),
        zoomToSelectionButtonView: SC.ButtonView.extend({
            classNames: 'footprint-map footprint-map-rezoom-to-extent-button'.w(),
            layout: { height: 24, width: 20, right: 0},
            icon: sc_static('footprint:images/zoom_to_extent.png'),
            action: 'zoomToSelectionExtent'
        })
    }),
    tableExportView: Footprint.ExportView.extend({
        classNames: 'footprint-table-info-export-button'.w(),
        layout: { height: 24, width: 100, right: 0},
        content:null,
        contentBinding:SC.Binding.oneWay('.parentView.contentView.exportContent'),
        isLocalExport: YES,
        isEnabledBinding:SC.Binding.oneWay('.parentView.content.status').matchesStatus(SC.Record.READY)
    }),

    overlayView: Footprint.OverlayView.extend({
        layout: {left: 0.01, right: 0.02, height: 0.83, top: 0.07},
        contentBinding:SC.Binding.oneWay('.parentView.content'),
        statusBinding:SC.Binding.oneWay('.parentView.overlayStatus'),
        // This will stop the overlay view being visible when the content is empty
        showOnBusyOnly: YES
        //testItems: YES
    }),

    contentView: SCTable.TableView.design({
        layout: {left: 0.01, right: 0.02, height: 0.83, top: 0.07},

        isVisibleBinding: SC.Binding.oneWay('.parentView.overlayView.isVisible').not(),

        _content: null,
        _contentBinding: SC.Binding.oneWay('.parentView.content'),
        _contentStatus: null,
        _contentStatusBinding: SC.Binding.oneWay('*_content.status'),

        mapProperties:null,
        mapPropertiesBinding: SC.Binding.oneWay('.parentView*mapProperties'),

        exportContent: function() {
            return [this.get('resolvedColumns')].concat(mapProperties(this.get('content'), this.get('resolvedColumns')));
        }.property('content', 'resolvedColumns').cacheable(),

        content:function() {
            if (!this.get('_content'))
                return [];
            var mapProperties = this.get('mapProperties') || (this.get('recordType') && this.get('recordType').mapProperties()) || SC.Object.create();
            var sortedProperties =
                (this.getPath('sortedProperties') && this.getPath('sortedProperties.length') > 0 && this.getPath('sortedProperties')) ||
                (this.getPath('parentView.columns') && this.getPath('parentView.columns.length') > 0 && this.getPath('parentView.columns')) ||
                (this.getPath('_content.firstObject.attributeKeys') ? this.getPath('_content.firstObject').attributeKeys() : []);
            return this.get('_content').map(function(item) {
                return $.mapToDictionary(sortedProperties, function(key) {
                    var path = mapProperties.getPath(key);
                    return [key, path ? item.getPath(path) : item.get(key)];
                });
            }, this);
        }.property('_content', 'mapProperties').cacheable(),

        // TODO I can't find a way to notify content that _content changed from an edit session update
        recordsDidUpdateObserver: function() {
            this.propertyDidChange('content');
        }.observes('Footprint.featuresActiveController.updateDate'),

        selectionBinding: '.parentView.selection',
        recordType: null,
        recordTypeBinding: SC.Binding.oneWay('.parentView.recordType'),

        parentColumns: null,
        parentColumnsBinding: SC.Binding.oneWay('.parentView.columns'),

        resolvedColumns: function() {
            if (this.get('parentColumns') && this.getPath('parentColumns.length') > 0)
                return this.get('parentColumns');
            else if (this.get('recordType') && this.get('recordType') != Footprint.Feature) {
                var recordType = this.get('recordType');
                // Sort the keys by the propertySortPriority if there is one
                return this.get('sortedProperties');
            }
            else if (this.getPath('_content.firstObject.attributeKeys'))
                return this.getPath('_content.firstObject').attributeKeys();
            else
                return [];
        }.property('parentColumns', 'sortedProperties', '_content').cacheable(),

        columns: function () {
            return this.get('resolvedColumns').map(function (key) {
                return SC.Object.create(SCTable.Column, {
                    name: key,
                    valueKey: key,
                    width: 150
                });
            });
        }.property('resolvedColumns').cacheable(),

        sortedProperties: function() {
            var recordType = this.get('recordType');
            if (!recordType)
                return null;
            var properties = recordType.allRecordAttributeProperties();
            var priorityProperties = recordType.priorityProperties().copy() || [];
            var excludeProperties = recordType.excludeProperties().copy() || [];
            return priorityProperties.concat(properties.removeObjects(priorityProperties).removeObjects(excludeProperties));
        }.property('recordType').cacheable()
    })
});
