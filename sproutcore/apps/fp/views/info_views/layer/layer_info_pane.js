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

/***
 * The pane used to edit the settings of a new or existing PresentationMedium and the DbEntity to which it is associated (if any). The saving order of this will have to first save a created DbEntity and then the PresentationMedium if a DbEntity is being created here
 * @type {*} */
Footprint.LayerInfoPane = SC.PanelPane.extend({

    layout: { width: 600, height: 300, centerX: 0, centerY: 0 },
    classNames:'footprint-layer-info-view'.w(),

    // Convenient UI flag.
    layerFileIsUploading: NO,

    recordType: Footprint.Layer,

    content: null,
    contentBinding: SC.Binding.oneWay('Footprint.layersEditController.content'),
    selection: null,
    selectionBinding: SC.Binding.from('Footprint.layersEditController.selection'),

    contentView: SC.View.extend({
        classNames:'footprint-info-content-view'.w(),
        childViews:['titleView', 'layerSelectView', 'editableContentView', 'buttonViews', 'uploadingOverlay'],
        content: null,
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        selection: null,
        selectionBinding: SC.Binding.from('.parentView.selection'),

        titleView: SC.LabelView.extend({
            layout: { left: 10, height: 25, top: 5 },
            classNames: ['footprint-info-title-view'],
            value: 'Manage Layers'
        }),

        layerSelectView: Footprint.EditRecordsSelectView.extend({
            contentBinding: SC.Binding.oneWay('.parentView.content'),
            selectionBinding: SC.Binding.from('.parentView.selection')
        }),

        contentIsNew: NO,
        contentIsNewBinding: SC.Binding.oneWay('Footprint.layerEditController.status').equalsStatus(SC.Record.READY_NEW),

        editableContentView: SC.View.extend({
            layout: { top: 30, left: 245, bottom: 40, right: 20 },
            classNames: 'footprint-layer-info-editable-content-view'.w(),

            childViews: ['nameView', 'sridView', 'hasFileView', 'uploadView', 'createFromLayerSelectionView'],
            nameView: Footprint.EditableCloneFieldView.extend({
                valueBinding: 'Footprint.layerEditController*name',
                title: 'Layer Name',
                layout: { height: 40 }
            }),
            sridView: Footprint.EditableCloneFieldView.extend({
                layout: { top: 45, height: 40 },
                notOriginInstance: null,
                notOriginInstanceBinding:SC.Binding.oneWay('Footprint.layerEditController.origin_instance').not(),
                isVisibleBinding: SC.Binding.and('.parentView.parentView.contentIsNew', '.notOriginInstance'),
                valueBinding: 'Footprint.layerEditController*db_entity_interest.db_entity.srid',
                title: 'SRID'
            }),
            hasFileView: SC.LabelView.extend({
                layout: { top: 95, height: 20, width: 260, centerX: 0 },
                hasFileBinding: SC.Binding.oneWay('Footprint.layerEditController*db_entity_interest.db_entity.upload_id').bool(),
                isNewBinding: SC.Binding.oneWay('.parentView.parentView.contentIsNew'),
                isVisibleBinding: SC.Binding.and('.hasFile', '.isNew'),
                value: 'File successfully uploaded, okay to save layer...'
            }),
            uploadView: SC.View.extend({
                layout: { top: 90, bottom: 40},
                notOriginInstance: null,
                notOriginInstanceBinding:SC.Binding.oneWay('Footprint.layerEditController.origin_instance').not(),
                isVisibleBinding: SC.Binding.and('.parentView.parentView.contentIsNew', '.notOriginInstance'),
                childViews: ['uploadButtonView'],

                uploadButtonView: SC.FileChooserView.extend({
                    layout: { height: 24, width: 140, centerX: 0, centerY: -10 },

                    content: null,
                    contentBinding: SC.Binding.oneWay('Footprint.layerEditController*db_entity_interest.db_entity'),
                    url: function() {
                        var content = this.get('content');
                        return content ?
                            Footprint.store.dataSource.uploadUri(
                                content.get('store'),
                                content.get('storeKey')) :
                            '/content-not-set'; // action can handle null
                    }.property('content').cacheable(),
                    // bending over backwards to proxy isUploading to somewhere central
                    isUploadingBinding: SC.Binding.oneWay('.form.isUploading'), // this should be in the view class, not here.
                    isUploadingDidChange: function() {
                        this.setPathIfChanged('pane.layerFileIsUploading', this.get('isUploading'));
                    }.observes('isUploading'),
                    resultDidUpdate: function() {
                        var result = this.get('result');
                        // We need to know the extension of the submitted file
                        if (!result)
                            return;
                        var extension = this.getPath('form.value').split('.').slice(-1)[0];
                        this.setPath('content.upload_id', '%@.%@'.fmt(result.upload_id, extension));
                        this.reset();
                    }.observes('result'),

                    form: SC.UploadForm.extend({
                        // Override this so that we can catch errors
                        iframe: SC.IFrameView.extend({
                            load: function () {
                                try {
                                    sc_super()
                                }
                                catch(e) {
                                    // Clear the value so the user can try again
                                    this.setPath('parentView.input.value', null);
                                    SC.AlertPane.warn({
                                        message: "Upload failed",
                                        description: "Only zipped shape files are supported. Contact us if something else is wrong."
                                    });
                                }
                                this.setPath('parentView.isUploading', NO);
                            }
                        }),
                        submitOnChange: SC.outlet('parentView.submitOnChange'),
                        inputName: SC.outlet('parentView.inputName')
                    })
                })
            }),

            createFromLayerSelectionView: Footprint.CheckboxInfoView.extend({
                classNames: 'footprint-layer-info-create-from-layer-selection-view'.w(),
                layout: { left: 0, bottom: 20, height: 20 },
                buttonLayout: { left: 0 },
                titleLayout: { left: 15 },
                isVisibleBinding: SC.Binding.and('.parentView.parentView.contentIsNew', 'Footprint.layerEditController.origin_instance'),
                title: 'Limit to current features of source layer selection',
                valueBinding: 'Footprint.layerEditController.create_from_selection'
            })
        }),

        buttonViews: SC.View.extend({
            layout: { bottom: 0, height: 30, left: 245, right: 20 },
            childViews: ['newButtonView', 'cancelButtonView', 'saveButtonView'],
            content: null,
            contentBinding: SC.Binding.oneWay('Footprint.layerEditController.content'),

            newButtonView: SC.ButtonView.extend({
                layout: { bottom: 5, left: 0, height: 24, width: 95 },
                title: 'New Layer',
                icon: 'add-icon',
                action: 'doCreateLayer'
            }),
            cancelButtonView: Footprint.CancelButtonView.extend({
                layout: { bottom: 5, right: 130, height: 24, width: 80 },
                calculatedStatusBinding: SC.Binding.oneWay('Footprint.layersEditController.calculatedStatus')
            }),
            saveButtonView: SC.ButtonView.extend({
                layout: { bottom: 5, right: 0, height: 24, width: 120 },

                uploadId: null,
                uploadIdBinding: SC.Binding.oneWay('Footprint.layerEditController*db_entity_interest.db_entity.upload_id'),
                originInstance: null,
                originInstanceBinding: SC.Binding.oneWay('Footprint.layerEditController.origin_instance'),
                contentIsNew: null,
                contentIsNewBinding: SC.Binding.oneWay('.parentView.parentView.contentIsNew'),
                isEnabled: function() {
                    // Enable saves for new content if an uploadId exists or its a clone
                    // Enable saves for all existing content
                    return !this.get('contentIsNew') || (this.get('uploadId')!=null || this.get('originInstance'));
                }.property('contentIsNew', 'uploadId', 'originInstance').cacheable(),

                content: null,
                contentBinding: SC.Binding.oneWay('.parentView.content'),
                title: 'Save All Changes',
                action: 'doSave'
            })
        }),

        uploadingOverlay: SC.View.extend({
            classNames: ['form-info-overlay'],
            isVisibleBinding: SC.Binding.oneWay('.pane.layerFileIsUploading'),
            childViews: ['labelView'],
            labelView: SC.LabelView.extend({
                layout: { height: 20, width: 250, centerX: 0, centerY: 0 },
                value: 'Uploading...'
            })
        })
    })
});
