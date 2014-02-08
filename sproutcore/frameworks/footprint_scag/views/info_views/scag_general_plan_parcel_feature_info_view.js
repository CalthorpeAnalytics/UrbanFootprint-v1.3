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

FootprintScag.ScagGeneralPlanParcelFeatureInfoView = Footprint.FeatureEditView.extend({
    classNames: 'footprint-general-plan-feature-info-view'.w(),
    childViews:' headerTitleView landUseTitleView landUseDefinitionView commentsTitleView commentsView commitButtonsView bufferView'.w(),
    recordType: FootprintScag.ScagGeneralPlanParcelFeature,

    headerTitleView: SC.LabelView.create({
        layout: {left: 0.02, top: 0.02},
        value: 'Editable Fields'
    }),

    landUseTitleView: SC.LabelView.create({
        layout: {left: 0.03, bottom: 0.68, width: 0.9, height:24},
        value: 'Land Use Definition'
    }),
    contentStatus: null,
    contentStatusBinding: SC.Binding.oneWay('*content.status'),

    land_use_definition: Footprint.pluralProperty,
    land_use_definitionBinding: 'Footprint.clientLandUseDefinitionController.singleSelection',

    landUseDefinitionView: Footprint.SelectInfoView.extend({
        layout: {bottom: 0.62, width: 0.95, height:24},
        includeNullItem: YES,
        contentBinding: SC.Binding.oneWay('Footprint.clientLandUseDefinitionController.content'),
        selectionBinding: SC.Binding.oneWay('Footprint.clientLandUseDefinitionController'),
        recordType: Footprint.ClientLandUseDefinition,
        itemTitleKey: 'land_use_description'
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