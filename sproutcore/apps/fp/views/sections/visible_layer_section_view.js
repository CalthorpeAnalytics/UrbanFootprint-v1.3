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

Footprint.VisibleLayerSectionView = SC.View.extend({
    classNames: ['footprint-visible-layer-section', 'footprint-map-overlay-section'],
    childViews: ['backgroundView', 'foregroundView'],
    backgroundView: SC.View.extend({
        layout: { height: .35 },
        childViews: ['backgroundLabelView', 'backgroundListView'],
        backgroundLabelView: SC.LabelView.extend({
            layout: { top: 5, height: 20, left: 5 },
            classNames: ['footprint-header'],
            value: 'Background Layers'
        }),
        backgroundListView: SC.ScrollView.extend({
            layout: { top: 30, bottom: 5, left: 5, right: 5 },
            contentView: SC.SourceListView.extend({
                contentBinding: SC.Binding.oneWay('F.layersVisibleBackgroundController.arrangedObjects'),
                contentValueKey: 'name',
                canReorderContent: YES
            })
        })
    }),

    foregroundView: SC.View.extend({
        layout: { top: .35 },
        childViews: ['foregroundLabelView', 'foregroundListView'],
        foregroundLabelView: SC.LabelView.extend({
            layout: { top: 5, height: 20, left: 5 },
            classNames: ['footprint-header'],
            value: 'Foreground Layers'
        }),
        foregroundListView: SC.ScrollView.extend({
            layout: { top: 30, bottom: 5, left: 5, right: 5 },
            contentView: SC.SourceListView.extend({
                contentBinding: SC.Binding.oneWay('F.layersVisibleForegroundController.arrangedObjects'),
                contentValueKey: 'name',
                canReorderContent: YES
            })
        })
    })
});
