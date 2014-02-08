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

FootprintScag.ScagPrimarySpzFeatureInfoView = Footprint.FeatureEditView.extend({
    classNames: 'footprint-primary-spz-feature-info-view'.w(),
    childViews:'headerTitleView commentsTitleView commentsView commitButtonsView bufferView'.w(),
    recordType: FootprintScag.ScagPrimarySpzFeature,
    content: null,

    headerTitleView: SC.LabelView.create({
        layout: {left: 0.02, top: 0.02},
        value: 'Editable Fields'
    }),

    commentsTitleView: SC.LabelView.create({
        layout: {left: 0.03, bottom: 0.45, width: 0.9, height:24},
        value: 'Comment'
    }),

    commentsView: Footprint.EditableStringView.extend({
           layout: {left: 0.05, width: 0.9, bottom: 0.13, height: 0.32},
            contentBinding: SC.Binding.oneWay('.parentView.content'),
            comments: Footprint.pluralProperty,
            valueBinding:'.comments'
    }),

    commitButtonsView: Footprint.SaveButtonView.extend({
        layout: {height: 30, width: 100, left: 0.04, bottom: 0.01},
        isEditable: YES,
        contentBinding: SC.Binding.oneWay('.parentView.content')
        }),

    bufferView: SC.SegmentedView.extend({
            layout: {height: 30, width: 100, left: 0.34, bottom: 0.01},
            selectSegmentWhenTriggeringAction: NO,
            itemActionKey: 'action',
            itemTitleKey: 'title',
            itemKeyEquivalentKey: 'keyEquivalent',
            itemValueKey: 'title',
            itemIsEnabledKey: 'isEnabled',

            items: [
                // View and edit the selected item's attributes
                SC.Object.create({ title: 'Undo', keyEquivalent: 'ctrl_u', action: '', isEnabled: NO, type: 'chronicler'}),
                SC.Object.create({ title: 'Redo', keyEquivalent: 'ctrl_r', action: '', isEnabled: NO, type: 'chronicler'})
            ]
        })

});
