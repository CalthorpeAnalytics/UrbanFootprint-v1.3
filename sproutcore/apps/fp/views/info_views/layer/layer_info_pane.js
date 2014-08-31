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
sc_require('views/info_views/label_select_info_view');
sc_require('views/info_views/editable_tags_view');

/***
 * The pane used to edit the settings of a new or existing PresentationMedium and the DbEntity to which it is associated (if any). The saving order of this will have to first save a created DbEntity and then the PresentationMedium if a DbEntity is being created here
 * @type {*} */
Footprint.LayerInfoPane = SC.PanelPane.extend({

    layout: { width: 800, height: 400, centerX: 0, centerY: 0 },
    classNames:'footprint-layer-info-view'.w(),

    // Convenient UI flag.
    layerFileIsUploading: NO,

    // Tells the pane elements that a save is underway, which disables user actions
    isSaving: null,
    isSavingBinding: SC.Binding.oneWay('Footprint.layersEditController.isSaving'),

    recordType: Footprint.Layer,

    content: null,
    contentBinding: SC.Binding.oneWay('Footprint.layersEditController.content'),
    selection: null,
    selectionBinding: SC.Binding.from('Footprint.layersEditController.selection'),

    /***
     * Indicates whether or not the layer being edited is new
     */
    contentIsNew: NO,
    contentIsNewBinding: SC.Binding.oneWay('Footprint.layerEditController.status').equalsStatus(SC.Record.READY_NEW),

    contentView: SC.View.extend({
        classNames:'footprint-info-content-view'.w(),
        childViews:['newButtonView', 'layerSelectView', 'editableContentView', 'sourceContentView', 'buttonViews', 'overlayView'],
        content: null,
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        selection: null,
        selectionBinding: SC.Binding.from('.parentView.selection'),

        newButtonView: SC.ButtonView.extend({
                layout: { left: 250, height: 24, bottom: 5, width: 150 },
                title: 'Add New Layer',
                icon: 'add-icon',
                action: 'doCreateLayer'
            }),

        /***
         * The left-hand view listing the layers. The selected layer is that being edited on the right-hand side
         */
        layerSelectView: Footprint.EditRecordsSelectView.extend({
            layout: {left:10, width:230, top:10, bottom: 5},
            contentBinding: SC.Binding.oneWay('.parentView.content'),
            selectionBinding: SC.Binding.from('.parentView.selection'),
            deletableNameProperty: 'db_entity_interest.db_entity.isDeletable'
        }),

        editableContentView: SC.View.extend({
            layout: { top: 10, bottom: 40, left: 250, width: 300 },
            classNames: 'footprint-layer-info-editable-content-view'.w(),
            childViews: ['editableDbEntityView'],

            content: null,
            contentBinding: SC.Binding.oneWay('Footprint.layerEditController.content'),
            contentIsNew: NO,
            contentIsNewBinding: SC.Binding.oneWay('.pane.contentIsNew'),

            /***
             * Shows and edits top-level properties of the DbEntity.
             * The user sees it as a Layer, but Layer is merely the UI wrapper around the DbEntity instance
             */
            editableDbEntityView: SC.View.extend({
                layout: { width: 300},
                childViews: ['nameView', 'scopeSelectView', 'featureUploadView'],
                content: null,
                contentBinding: SC.Binding.oneWay('.parentView*content.db_entity_interest.db_entity'),
                /***
                 * The Editable name of the Layer, delegates to the DbEntity
                 */
                nameView: Footprint.EditableCloneFieldView.extend({
                    layout: { height: 40 },
                    isEditable: YES,
                    classNames:['editable-db-entity-name-view'],
                    valueBinding: '.parentView*content.name',
                    title: 'Layer Name'
                }),

                scopeSelectView: Footprint.LabelSelectInfoView.extend({
                    layout: { top: 44, height: 40 },
                    classNames:['layer-scope-select-view'],
                    // Scope can only be set when the record is new
                    isEnabledBinding : SC.Binding.oneWay('.pane.contentIsNew'),
                    itemTitleKey:'name',
                    title: function() {
                        return 'Scope' + (!this.get('isEnabled') ? ' (locked)' : '');
                    }.property('isEnabled').cacheable(),
                    contentBinding: 'Footprint.dbEntityInterestScopesController.content',
                    // The controller's selection is bound to the behavior instance of the current DbEntity.feature_behavior
                    selectionBinding: 'Footprint.dbEntityInterestScopesController.selection'
                }),

                /***
                 * The Footprint.Behavior instance to be associated with the DbEntity via a Footprint.FeatureBehavior
                 */
                featureUploadView: SC.View.extend({
                    layout: { top: 85, bottom: 5 },
                    classNames:['editable-feature-behavior-view'],
                    childViews: ['behaviorSelectView', 'intersectionSelectView', 'sridView', 'sourceIdView', 'cloneSourceView', 'createSourceView', 'readOnlyView'],
                    content: null,
                    contentBinding: SC.Binding.oneWay('.parentView.content'),

                    behaviorSelectView: Footprint.LabelSelectInfoView.extend({
                        layout: { top: 5, height: 40 },
                        classNames:['editable-feature-behavior-behavior-select-view'],
                        // Behavior can be changed as long as it's not locked at the DbEntity level
                        isEnabledBinding : SC.Binding.oneWay('.parentView.parentView*content.feature_behavior.behavior_locked').not(),
                        itemTitleKey:'name',
                        //includeNullItem: YES,
                        title: function() {
                            return 'Assigned Behavior' + (!this.get('isEnabled') ? ' (locked)' : '');
                        }.property('isEnabled').cacheable(),
                        //nullTitle: 'None Selected',
                        contentBinding: 'Footprint.behaviorsEditController.arrangedObjects',
                        // The controller's selection is bound to the behavior instance of the current DbEntity.feature_behavior
                        selectionBinding: 'Footprint.behaviorsEditController.selection',
                        action: 'doPickBehavior'
                    }),

                    intersectionSelectView: Footprint.LabelSelectInfoView.extend({
                        layout: { top: 52, height: 40},
                        classNames:['editable-feature-behavior-intersection-select-view'],
                        itemTitleKey:'description',
                        //includeNullItem: YES,
                        title: 'Intersection Type',
                        //nullTitle: 'None Selected',
                        contentBinding: 'Footprint.intersectionsEditController.content',
                        // The controller's selection is bound to the Intersection instance of the current DbEntity.feature_behavior
                        selectionBinding: 'Footprint.intersectionsEditController.selection'
                    }),

                    sridView: Footprint.EditableCloneFieldView.extend({
                        layout: { top: 100, height: 40, width: 120 },
                        classNames:['footprint-source-content-info-srid-view'],
                        title: 'SRID',
                        isEditable:YES,
                        contentId:null,
                        contentIdBinding:SC.Binding.oneWay('*content.parentRecord.id'),
                        content: null,
                        contentBinding: SC.Binding.oneWay('.parentView.content'),
                        isVisible: function() {
                            if (this.getPath('contentId') < 0) {
                                return YES;
                            }
                            else {
                                return NO
                            }
                        }.property('content', 'contentId').cacheable(),
                        valueBinding: SC.Binding.from('.parentView*content.srid')
                    }),

                    sourceIdView: Footprint.EditableCloneFieldView.extend({
                        intersectionSelection: null,
                        intersectionSelectionBinding: SC.Binding.oneWay('Footprint.intersectionsEditController*selection.firstObject'),
                        isVisible: function() {
                        if (this.getPath('intersectionSelection.join_type') == 'attribute') {
                            return YES;
                            }
                        else {
                            return NO
                            }
                        }.property('intersectionSelection').cacheable(),

                        layout: { top: 100, height: 40, left: 125, right: 5 },
                        classNames:['footprint-source-content-info-source-id-view'],
                        title: 'Source ID Column Name',
                        isEditable:YES,
                        valueBinding: '.parentView*content.feature_class_configuration.primary_key'
                    }),

                    cloneSourceView: SC.View.extend({
                        layout: { bottom: 20, height: 20 },
                        isVisibleBinding: SC.Binding.and('*content.origin_instance', '.pane.contentIsNew'),
                        childViews: ['createFromLayerSelectionView'],
                        classNames:['source-content-clone-source-view'],

                        content: null,
                        contentBinding: SC.Binding.oneWay('.parentView.content'),

                        createFromLayerSelectionView: Footprint.CheckboxInfoView.extend({
                            classNames: ['footprint-layer-info-create-from-layer-selection-view'],
                            content: null,
                            contentBinding: SC.Binding.oneWay('.parentView*content'),
                            layout: { top: 0, height: 20 },
                            buttonLayout: { left: 0 },
                            titleLayout: { left: 20 },
                            title: 'Limit to selected features of source layer',
                            valueBinding: '*content.feature_class_configuration.source_from_origin_layer_selection',
                            valueObserver: function() {
                                if (!(this.getPath('content.status') & SC.Record.READY))
                                    return;
                                // If checked, set the origin_layer property to the origin layer. If not checked clear to null.
                                this.setPath('content.feature_class_configuration.origin_layer_id',
                                             this.get('value') && this.getPath('content.origin_instance') ?
                                                 Footprint.layersEditController.find(function(layer) {
                                                    return layer.getPath('db_entity_interest.db_entity.id') === this.getPath('content.origin_instance.id');
                                                 }, this).get('id')
                                                 : null);
                            }.observes('.content', '.value')
                        })
                    }),
                            /***
                     * Describes sources uploaded via the interface
                     */
                    createSourceView: SC.View.extend({
                        layout: { top:170, height: 60 },
                        notOriginInstance: null,
                        notOriginInstanceBinding:SC.Binding.oneWay('*content.origin_instance').not(),
                        isVisibleBinding: SC.Binding.and('.pane.contentIsNew', '.notOriginInstance'),
                        childViews: ['hasFileView', 'uploadView'],
                        classNames:['source-content-create-source-view'],

                        content: null,
                        contentBinding: SC.Binding.oneWay('.parentView.content'),

                        uploadView: SC.View.extend({
                            childViews: ['uploadButtonView', 'hasFileView'],
                            content: null,
                            contentBinding: SC.Binding.oneWay('.parentView*content'),

                            uploadButtonView: SC.FileChooserView.extend({
                                layout: { height: 24, left: 60},

                                content: null,
                                contentBinding: SC.Binding.oneWay('.parentView.content'),
                                url: function() {
                                    var content = this.get('content');
                                    return content ?
                                        Footprint.store.dataSource.uploadUri(content) :
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
                            }),

                            hasFileView: SC.LabelView.extend({
                                layout: { top: 30},
                                hasFile: null,
                                hasFileBinding: SC.Binding.oneWay('.parentView*content.upload_id').bool(),
                                isNew: null,
                                isNewBinding: SC.Binding.oneWay('.pane.contentIsNew'),
                                isVisibleBinding: SC.Binding.and('.hasFile', '.isNew'),
                                value: 'File successfully uploaded, okay to save layer...'
                            })
                        })
                    }),
                    readOnlyView: Footprint.CheckboxInfoView.extend({
                        layout: { bottom: 0, height: 20, width: 130 },
                        classNames:['editable-feature-behavior-readonly-view'],
                        buttonLayout: { left: 0 },
                        titleLayout: { left: 20, width: 100 },
                        title: 'Features are locked',
                        valueBinding: '.parentView.readonly'
                    })
                })
            })
        }),

        // Edits data about the source data of the layer
        sourceContentView: SC.View.extend({
            layout: {left: 570, bottom:40, top: 10},
            childViews: ['infoView', 'featureBehaviorView'],
            classNames:['layer-info-pane-source-content-view'],

            content: null,
            contentBinding: SC.Binding.oneWay('Footprint.layerEditController.content'),

            /***
             * Describes sources configured on the server
             */
            infoView: SC.View.extend({
                layout: { top: 0, height: 160 },
                childViews: ['titleView', 'datesView'],
                classNames:['source-content-info-view'],
                content: null,
                contentBinding: SC.Binding.oneWay('.parentView.content'),

                titleView: SC.LabelView.extend({
                    layout: { top: 0, height: 40 },
                    classNames:['footprint-source-content-info-title-view'],
                    value: 'Layer Information'
                }),

                datesView: SC.View.extend({
                    childViews: ['dateCreatedView', 'dateUpdatedView'],
                    layout: { top: 88, height: 50 },
                    dateCreatedView: Footprint.EditableCloneFieldView.extend({
                        layout: { top: 0 },
                        editableContentViewLayout: { top: 0, left: 50 },
                        title: 'Created:',
                        classNames:['source-content-info-date-created-view'],
                        valueBinding: SC.Binding.oneWay('.parentView*content.db_entity_interest.db_entity.created'),
                        isVisibleBinding: SC.Binding.oneWay('.value').bool()
                    }),
                    dateUpdatedView: Footprint.EditableCloneFieldView.extend({
                        layout: { top: 20 },
                        editableContentViewLayout: { top: 0, left: 50 },
                        title: 'Updated:',
                        classNames:['source-content-info-date-created-view'],
                        valueBinding: SC.Binding.oneWay('.parentView*content.db_entity_interest.db_entity.updated'),
                        isVisibleBinding: SC.Binding.oneWay('.value').bool()
                    })
                })
            }),

            featureBehaviorView: SC.View.extend({
                layout: { top: 160 },
                classNames:['editable-feature-behavior-view'],
                childViews: ['tagsView'],
                content: null,
                contentBinding: SC.Binding.oneWay('.parentView*content.db_entity_interest.db_entity.feature_behavior'),

                tagsView: Footprint.EditableTagsView.extend({
                    layout: { top: 0, right: 15},
                    classNames:['editable-feature-behavior-tags-view'],
                    tags:null,
                    tagsBinding: SC.Binding.oneWay('.parentView*content.tags'),
                    // Use gatekeeper to prevent writing the tags when the instance isn't ready, sigh
                    content: function(propKey, value) {
                        if (typeof(value) !== 'undefined' && (this.getPath('tags.status') & SC.Record.READY)) {
                            this.setPath('parentView.content.tags', value)
                        }
                        return this.get('tags');
                    }.property('tags').cacheable(),
                    computedTagsBinding: '.parentView*content.computedTags'
                })
            })
        }),

        buttonViews: SC.View.extend({
            layout: { bottom: 0, height: 30, width: 245, right: 100},
            childViews: ['cancelButtonView', 'saveButtonView'],
            content: null,
            contentBinding: SC.Binding.oneWay('Footprint.layerEditController.content'),

            cancelButtonView: Footprint.CancelButtonView.extend({
                layout: { bottom: 5, right: 10, height: 24, width: 80 },
                calculatedStatusBinding: SC.Binding.oneWay('Footprint.layersEditController.calculatedStatus')
            }),
            saveButtonView: SC.ButtonView.extend({
                layout: { bottom: 5, left: 5, height: 24, width: 120 },

                uploadId: null,
                uploadIdBinding: SC.Binding.oneWay('Footprint.layerEditController*db_entity_interest.db_entity.upload_id'),
                originInstance: null,
                originInstanceBinding: SC.Binding.oneWay('Footprint.layerEditController.origin_instance'),
                contentIsNew: null,
                contentIsNewBinding: SC.Binding.oneWay('.pane.contentIsNew'),
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

        overlayView: Footprint.SaveOverlayView.extend({
            isUploading: NO,
            isUploadingBinding: SC.Binding.oneWay('.pane.layerFileIsUploading'),
            isSaving: NO,
            isSavingBinding: SC.Binding.oneWay('.pane.isSaving'),
            isVisibleBinding: SC.Binding.or('.isUploading', '.isSaving'),

            savingMessage: function() {
                if (this.get('isUploading'))
                    return 'Uploading...'
                return 'Saving...';
            }.property('isSaving', 'isUploading').cacheable()
        })
    })
});
