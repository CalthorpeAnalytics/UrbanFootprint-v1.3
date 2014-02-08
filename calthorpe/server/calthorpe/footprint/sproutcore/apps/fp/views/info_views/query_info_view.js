
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
sc_require('views/info_views/select_info_view');

// TODO this will become more complicated to handle separate group bys
Footprint.QueryInfoView = Footprint.InfoView.extend({
    classNames:'footprint-query-info-view'.w(),
    childViews:'titleView activeLayerNameView contentView joinView queryButtonView'.w(),
    recordType: null,
    layout: {left: 0.01, width: 0.3, top: 5, height: 24},

    title: 'Select * From',
    /*
    aggregatesView: Footprint.InfoView.extend({
        classNames:'footprint-query-info-aggregates-view'.w(),
        layout: {left: 0, right:0.2, top:26, height: 24},
        title: 'Aggregates',
        contentView: Footprint.EditableModelStringView.extend({
            layout: {left: 0.2},
            isMultiLine: YES,
            valueBinding: parentViewPath(1,'*content.aggregates'),
            contentBinding: parentViewPath(1,'*content')
        })
    }),
    */
    activeLayerNameView: SC.LabelView.create({
        layout: {left: 0.1, width: 0.6, height:24},
        valueBinding: SC.Binding.oneWay('Footprint.layerActiveController.name')
    }),


    contentView: Footprint.InfoView.extend({
        classNames:'footprint-query-info-content-view'.w(),
        layout: {left: 0.03, right:0.2, top:30, height: 24},
        title: 'Where:',
        contentView: Footprint.EditableModelStringView.extend({
            layout: {width: 0.5, left: 0.08},
            isMultiLine: YES,
            valueBinding: parentViewPath(1,'*content.query_string'),
            contentBinding: parentViewPath(1,'*content')
        })
    }),

    joinView: Footprint.SelectInfoView.extend({
        classNames:'footprint-query-info-group-by-view'.w(),
        layout: {left: 0.06, width:0.4, top:65, height: 24},
        title: 'Join:',
        recordType:null,
        recordTypeBinding:SC.Binding.oneWay('.parentView.recordType'),
        contentBinding: SC.Binding.oneWay('Footprint.featuresActiveDbEntityKeysController.content'),
        selectionBinding: SC.Binding.oneWay('Footprint.featuresActiveDbEntityKeysController'),
        includeNullItem:YES,
        nullTitle: 'None'
    }),
    /*
    groupByView: Footprint.SelectInfoView.extend({
        classNames:'footprint-query-info-group-by-view'.w(),
        layout: {left: 0, right:0.2, top:78, height: 24},
        title: 'Group By',
        recordType:null,
        recordTypeBinding:SC.Binding.oneWay('.parentView.recordType'),
        contentBinding: SC.Binding.oneWay('Footprint.featuresActivePropertiesController.content'),
        // TODO this should be the selection property, but update the SelectionSet directly is hard because it gets frozen
        selectionSupportBinding: SC.Binding.oneWay('Footprint.featuresActivePropertiesController')
    }),
    */

    queryButtonView: SC.ButtonView.design({
        classNames:'footprint-query-info-query-button-view'.w(),
        layout: {left:0.49, width:0.1, top:30, height: 24},
        title: 'Select',
        action: 'doQuerySelection',
        queryString: null,
        queryStringBinding: SC.Binding.oneWay('.parentView.contentView.contentView.value'),
        aggregatesString: null,
        aggregatesStringBinding: SC.Binding.oneWay('.parentView.aggregatesView.value'),
        groupByString: null,
        groupByStringBinding: SC.Binding.oneWay('.parentView.groupByView.value'),
        joins: null,
        joinsBinding: SC.Binding.oneWay('Footprint.featuresActiveDbEntityKeysController.selection'),
        isVisibleBinding: '.parentView.isEnabled',
        valueBinding: parentViewPath(1,'*content.query'),
        contentBinding: parentViewPath(1,'*content')
    })
});
