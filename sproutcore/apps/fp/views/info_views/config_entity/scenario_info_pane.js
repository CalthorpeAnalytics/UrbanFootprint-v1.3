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
 *
 */

sc_require('views/info_views/config_entity/editable_clone_field_view');
sc_require('views/info_views/edit_records_select_view');
sc_require('views/cancel_button_view');
sc_require('views/save_overlay_view');
sc_require('views/info_views/info_pane_crud_buttons_view');

/***
 * The pane used to edit the settings of a new or existing PresentationMedium and the DbEntity to which it is associated (if any). The saving order of this will have to first save a created DbEntity and then the PresentationMedium if a DbEntity is being created here
 * @type {*} */
Footprint.ScenarioInfoPane = SC.PanelPane.extend({

    layout: { width: 600, height: 300, centerX: 0, centerY: 0 },
    classNames:'footprint-scenario-info-view'.w(),

    recordType:Footprint.Scenario,

    // Tells the pane elements that a save is underway, which disables user actions
    isSaving: null,
    isSavingBinding: SC.Binding.oneWay('Footprint.scenariosEditController.isSaving'),

    content: null,
    contentBinding: SC.Binding.oneWay('Footprint.scenariosEditController.arrangedObjects'),
    selection: null,
    selectionBinding: SC.Binding.from('Footprint.scenariosEditController.selection'),

    contentView: SC.View.extend({
        classNames:'footprint-info-content-view'.w(),
        childViews:['titleView', 'scenarioSelectView', 'editableContentView', 'infoPaneButtonsView', 'overlayView'],
        content: null,
        contentBinding: SC.Binding.oneWay('.parentView.content'),

        selection: null,
        selectionBinding: SC.Binding.from('.parentView.selection'),

        titleView: SC.LabelView.extend({
            layout: { left: 10, height: 25, top: 5 },
            classNames: ['footprint-info-title-view'],
            value: 'Manage Scenarios'
        }),

        scenarioSelectView: Footprint.EditRecordsSelectView.extend({
            contentBinding: SC.Binding.oneWay('.parentView.content'),
            selectionBinding: SC.Binding.from('.parentView.selection'),
            deletableNameProperty: 'isDeletable'
        }),

        overlayView: Footprint.SaveOverlayView.extend({
            isVisibleBinding: SC.Binding.oneWay('.pane.isSaving')
        }),

        editableContentView: SC.View.extend({
            layout: { top: 30, left: 245, bottom: 40, right: 20 },
            classNames:'footprint-scenario-info-editable-content-view'.w(),
            childViews:['nameView', 'yearView', 'descriptionView'],

            content: null,
            contentBinding: SC.Binding.oneWay('.parentView.selection'),

            nameView: Footprint.EditableCloneFieldView.extend({
                layout: { height: 40 },
                valueBinding: '.parentView*content.firstObject.name',
                title: 'Scenario Name'
            }),

            yearView: Footprint.EditableCloneFieldView.extend({
                layout: { top: 45, height: 40 },
                valueBinding: '.parentView*content.firstObject.year',
                title: 'Scenario Year'
            }),

            descriptionView: Footprint.EditableCloneFieldView.extend({
                layout: { top: 90, bottom: 0 },
                valueBinding: '.parentView*content.firstObject.description',
                title: 'Description'
            })
        }),

        infoPaneButtonsView: Footprint.InfoPaneCrudButtonsView.extend({
            layout: { bottom: 0, height: 30, left: 245, right: 20 },
            recordTypeName: 'Scenario',
            contentBinding: SC.Binding.oneWay('.parentView.content'),
            createButtonLayout: {bottom: 5, left: 0, height:24, width:120},
            closeButtonLayout: { bottom: 5, right: 130, height: 24, width: 80 },
            saveButtonLayout: { bottom: 5, right: 0, height: 24, width: 120 }
        })
    })
});
