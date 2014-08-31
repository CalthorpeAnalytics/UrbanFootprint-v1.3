/**
 * Created with PyCharm.
 * User: calthorpe
 * Date: 11/15/13
 * Time: 11:56 AM
 * To change this template use File | Settings | File Templates.
 */
sc_require('views/info_views/analysis_module/label_result_views');
sc_require('views/editable_model_string_view');

Footprint.EditableConstraintPercentFieldView = SC.View.extend({
    childViews: ['nameView', 'priorityView', 'percentView'],
    nameValue:null,
    priorityValue: null,
    percentValue: null,

    nameView: SC.LabelView.extend({
        layout: {left: 0.01, width: 0.5, top: 4, bottom: 1},
        valueBinding: SC.Binding.oneWay('.parentView.nameValue'),
        textAlign: SC.ALIGN_LEFT,
        backgroundColor: '#f7f7f7'
    }),
    priorityView:  Footprint.EditableModelStringView.extend({
        classNames: ['footprint-editable-content-view'],
        layout: {left: 0.51, width: 0.24, top: 3},
        valueBinding: SC.Binding.from('.parentView.priorityValue'),
        textAlign: SC.ALIGN_CENTER
    }),
    percentView:  Footprint.EditableModelStringView.extend({
        classNames: ['footprint-editable-content-view'],
        layout: {left: 0.76, width: 0.25, top: 3},
        percent: null,
        percentBinding: SC.Binding.from('.parentView.percentValue'),
        value: function(propKey, value) {
            if (value) {
                // parse the float and round. This eliminates anything the user enters beyond 2 decimal places.
                var roundedValue = parseFloat(value).toFixed(0);
                // Parse the rounded value and divide to a decimal for setting
                this.set('percent', parseFloat(roundedValue)/100);

                // Still return the percent with rounding
                return roundedValue;
            }
            else {
                // Multiply to a percent
                return (100*parseFloat(this.get('percent'))).toFixed(0);
            }
        }.property('percent').cacheable(),

        textAlign: SC.ALIGN_CENTER
    })
})


Footprint.EnvironmentalConstraintModuleManagementView = SC.View.extend({

    classNames: "footprint-environmental-contraints-management-view".w(),
    childViews: ['titleContainerView', 'headerLabelView', 'environmentalConstraintsView', 'saveButtonView', 'updatingStatusView', 'updatingOverlayView'],

    content: null,
    contentBinding: SC.Binding.oneWay('Footprint.environmentalConstraintUpdaterToolEditController.content'),

    recordsAreUpdating: null,
    recordsAreUpdatingBinding: SC.Binding.oneWay('Footprint.environmentalConstraintUpdaterToolEditController.recordsAreUpdating'),

    isOverlayVisible: function () {
        var recordsAreUpdating = this.get('recordsAreUpdating');
        if (recordsAreUpdating) {
            return recordsAreUpdating
        }
        return NO
    }.property('recordsAreUpdating').cacheable(),

    titleContainerView: SC.ContainerView.extend({
        classNames: "footprint-analytic-module-title-container-view ".w(),
        childViews: ['titleView'],
        layout: {top: 10, left: 10, height: 40, right: 30},
        backgroundColor: 'green',
        titleView: SC.LabelView.extend({
            classNames: "footprint-analytic-module-title-view footprint-header".w(),
            layout: {top: 2, left: 3, right: 3, bottom: 2},
            scenarioName: null,
            scenarioNameBinding: SC.Binding.oneWay('Footprint.scenarioActiveController.name'),
            value: function() {
                return 'Manage  %@ \n Environmental Constraints'.fmt(this.get('scenarioName'));
            }.property('scenarioName'),
            textAlign: SC.ALIGN_LEFT
        })
    }),

    headerLabelView: SC.View.extend({
        layout: {top: 50, height: 20, left: 10, right: 30},
        childViews: ['nameTitle', 'priorityTitle', 'percentTitle'],
        backgroundColor: '#e1e1e1',
        nameTitle: SC.LabelView.extend({
            classNames: ['footprint-editable-9font-title-view'],
            layout: {width: 0.5, top: 3},
            value: 'Constraint Layer Name',
            textAlign: SC.ALIGN_CENTER
        }),
        priorityTitle: SC.LabelView.extend({
            classNames: ['footprint-editable-9font-title-view'],
            layout: {left: 0.5, width: 0.2, top: 3},
            value: 'Priority',
            textAlign: SC.ALIGN_CENTER
        }),
        percentTitle: SC.LabelView.extend({
            classNames: ['footprint-editable-9font-title-view'],
            layout: {left: 0.7, width: 0.3, top: 3},
            value: '% Constrained',
            textAlign: SC.ALIGN_CENTER
        })
    }),

    environmentalConstraintsView: SC.ScrollView.extend(SC.ContentDisplay,{
        classNames: ['footprint-environmental-constraint-percent-scroll-view'],
        layout: {right: 30, left: 10, top: 70, height: 300},
        contentBinding: SC.Binding.oneWay('.parentView*content.firstObject.environmental_constraint_percents'),
        contentDisplayProperties: ['contentFirstObject'],

        contentView: SC.SourceListView.extend(SC.ContentDisplay, {
            classNames: ['footprint-environmental-constraint-percent-source-list-view'],
            rowHeight: 20,
            isEditable: YES,
            isEnabledBinding: SC.Binding.oneWay('.content').bool(),
            contentDisplayProperties: ['content'],
            contentBinding: SC.Binding.from('.parentView.parentView.content'),

            exampleView: Footprint.EditableConstraintPercentFieldView.extend({
                nameValueBinding: '*content.db_entity.name',
                percentValueBinding: '*content.percent',
                priorityValueBinding: '*content.priority'
            })
        })
    }),

    saveButtonView: SC.ButtonView.design({
        layout: {top: 380, left: 20, height: 24, width: 60},
        title: 'Update',
        action: 'doAnalysisToolUpdate',
        isCancel: YES
    }),

    updatingStatusView: SC.View.extend({
        layout: { left: 100, right: 30, top: 380, height: 27},
        childViews: ['updatingIconView', 'updatingTitleView'],
        isVisibleBinding: SC.Binding.oneWay('.parentView.isOverlayVisible'),
        backgroundColor: '#e5e5e5',

        updatingIconView: SC.ImageView.extend({
            layout: { left:0, width:27, height:27, right: 30},
            useCanvas: NO,
            value: sc_static('footprint:images/spinner.gif')
        }),
        updatingTitleView: SC.LabelView.extend({
            layout: {left: 35, top: 5},
            value: 'Processing...'
        })
    }),

    updatingOverlayView: SC.View.extend({
        classNames: ['overlay-view'],
        childViews:['imageView'],
        layout: {right: 30, left: 10, top: 70, height: 300},

        isVisibleBinding:SC.Binding.oneWay('.parentView.isOverlayVisible'),

        imageView: SC.ImageView.extend({
            layout: { centerX:0, centerY:0, width:27, height:27},
            useCanvas: NO,
            value: sc_static('footprint:images/spinner.gif')
        })
    })
})

