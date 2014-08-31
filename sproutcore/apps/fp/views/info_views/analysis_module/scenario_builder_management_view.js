/**
 * Created with PyCharm.
 * User: calthorpe
 * Date: 11/15/13
 * Time: 11:56 AM
 * To change this template use File | Settings | File Templates.
 */
sc_require('views/info_views/analysis_module/analysis_module_view');
sc_require('views/sections/built_form_section_view');
sc_require('views/info_views/built_form/editable_input_field_view');
sc_require('views/tool_segmented_button_view');
sc_require('views/clear_button_view');

Footprint.CoreModuleManagementView = SC.View.extend({

    classNames: "footprint-scenario-builder-module-management-view".w(),
    childViews: ['overlayView', 'manageModuleView', 'activeBuiltFormSummaryView','featureBarView', 'builtFormSectionView'],

    allResultsStatus: null,
    allResults: null,

    title: 'Scenario Builder',
    executeModuleAction: '',
    editAssumptionsAction: '',

    analysisModule: null,
    analysisModuleBinding: SC.Binding.oneWay('Footprint.analysisModulesEditController*selection.firstObject'),

    activeLayer: null,
    activeLayerBinding: SC.Binding.oneWay('Footprint.layerActiveController.content'),
    activeLayerStatus: null,
    activeLayerStatusBinding: SC.Binding.oneWay('Footprint.layerActiveController*content.status'),

    selection: null,
    selectionBinding: SC.Binding.oneWay('Footprint.builtFormCategoriesTreeController.selection'),

    selectionFirstObject: null,
    selectionFirstObjectBinding: SC.Binding.oneWay('*selection.firstObject'),

    /**
     * Returns YES if the given item is configured for the active layer and the toolsController says its type is isEnabled
     * @param item
     * @returns {*|boolean|*}
     */
    layerLookup: SC.Object.create({
        'future_agriculture_feature': {
            subtitle: 'Agriculture Painting',
            isEnabledItems:  Footprint.ToolSelectionStandardItems.concat(['doPaintApply'])
        },
        'end_state': {
            subtitle: 'Scenario Painting',
            isEnabledItems:  Footprint.ToolSelectionStandardItems.concat(['doPaintApply'])
        },
        'base_feature': {
            subtitle: 'Base Editing',
            isEnabledItems:  Footprint.ToolSelectionStandardItems.concat(['doPaintApply'])
        }
    }),
    activeLayerConfig: function () {
        if (this.get('activeLayerStatus') & SC.Record.READY)
            return this.getPath('layerLookup.%@'.fmt(this.getPath('activeLayer.db_entity_key')));
    }.property('activeLayer', 'activeLayerStatus').cacheable(),

    isItemEnabled: function (item) {
        var layerConfig = this.get('activeLayerConfig');
        // Find the optional toolController boolean for this item type
        var controllerEnabled = Footprint.toolController.get('%@IsEnabled'.fmt(item.get('type')));
        // Return YES if the layerConfig (or default config) and tool enables the item
        return (layerConfig ? layerConfig.isEnabledItems : Footprint.ToolSelectionStandardItems).contains(item.action) &&
            (typeof(controllerEnabled) == 'undefined' || controllerEnabled);
    },

    // Shows saving progress. Normally this is done in the analysis_module_section_view
    // but we need to also track saving the Features
    overlayView: Footprint.OverlayView.extend({
        contentBinding: SC.Binding.oneWay('Footprint.featuresEditController.content'),
        statusBinding:SC.Binding.oneWay('*content.status')
    }),

    activeBuiltFormSummaryView: SC.View.extend({
        layout: { top: 125, height: 85 },
        classNames: ['footprint-active-built-form-summary-view'],
        childViews: ['titleView', 'nameView', 'colorView', 'duSummaryView', 'empSummaryView'],
        backgroundColor: '#f2f1ef',
        content: null,
        contentBinding: SC.Binding.oneWay('.parentView.selectionFirstObject'),
        selection: null,
        selectionBinding: SC.Binding.oneWay('.parentView.selection'),

        titleView: SC.LabelView.extend({
            classNames: ['footprint-editable-9font-title-view'],
            layout: {left: 5, height: 14, top: 3},
            value: 'Active Built Form:'
        }),

        nameView: SC.LabelView.extend({
            classNames: ['footprint-active-built-form-name-view', 'toolbar'],
            layout: {left: 5, width:.95, height: 20, top: 18},
            valueBinding: SC.Binding.oneWay('.parentView*content.name'),
            textAlign: SC.ALIGN_CENTER

        }),

        colorView: SC.LabelView.extend({
            classNames: ['footprint-active-built-form-medium'],
            layout: {left: 5, width:60, height: 30, top: 45},
            displayProperties: ['color', 'medium'],

            medium: null,
            mediumBinding: SC.Binding.oneWay('.parentView*content.medium'),

            color: null,
            colorBinding: SC.Binding.oneWay('*medium.content').transform(function(medium) {
                if (medium) {
                    return medium.fill.color;
                }
            }),
            render: function(context) {
                sc_super();
                var color = this.get('color');
                context.setStyle("background-color", color);
            }
        }),

        duSummaryView: Footprint.NonEditableValueBottomLabelledView.extend({
            title: 'DU/Ac',
            valueBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.dwelling_unit_density').transform(function(density) {
                    if (density)
                        return (density).toFixed(2)
                    return 0
                }),
            layout: {left: 95, width: 50, height: 28, top: 50}
        }),
        empSummaryView: Footprint.NonEditableValueBottomLabelledView.extend({
            title: 'Emp/Ac',
            valueBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.employment_density').transform(function(density) {
                    if (density)
                        return (density).toFixed(2)
                    return 0
            }),
            layout: {left: 175, width: 50, height: 28, top: 50}

        })

    }),

    featureBarView: SC.View.extend({
        layout: { top: 0, height: 125 },
        childViews: 'param1View param2View param3View toggleView redevelopmentToggleView applyView clearView bufferView menuButtonView'.w(),
        classNames: ['featurer-bar'],

        param1View: Footprint.SliderInfoView.extend({
            layout: { left: 0, width: 0.3, height:43, top: 10},
            classNames: ['featurer-bar-param1'],
            valueSymbol: '%',
            title: 'Dev Pct',
            minimum: 0,
            maximum: 100,
            step: 1,
            rawValue: null,
            rawValueBinding: SC.Binding.from('Footprint.paintingController.developmentPercent'),
            value: function (propKey, value) {
                if (value !== undefined) {
                    this.set('rawValue', value / 100);
                    return value;
                }
                return this.get('rawValue') * 100;
            }.property('rawValue').cacheable()
        }),
        param2View: Footprint.SliderInfoView.extend({
            layout: { left: 0.325, width: 0.3, height:43, top: 10},
            classNames: ['featurer-bar-param2'],
            valueSymbol: '%',
            title: 'Density Pct',
            minimum: 0,
            maximum: 100,
            step: 1,
            rawValue: null,
            rawValueBinding: SC.Binding.from('Footprint.paintingController.densityPercent'),
            value: function (propKey, value) {
                if (value !== undefined) {
                    this.set('rawValue', value / 100);
                    return value;
                }
                return this.get('rawValue') * 100;
            }.property('rawValue').cacheable()
        }),
        param3View: Footprint.SliderInfoView.extend({
            layout: { left: 0.65, width: 0.3, height:43, top: 10},
            classNames: ['featurer-bar-param3'],
            valueSymbol: '%',
            title: 'Gross/Net Pct',
            minimum: 0,
            maximum: 100,
            step: 1,
            rawValue: null,
            rawValueBinding: SC.Binding.from('Footprint.paintingController.grossNetPercent'),
            value: function (propKey, value) {
                if (value !== undefined) {
                    this.set('rawValue', value / 100);
                    return value;
                }
                return this.get('rawValue') * 100;
            }.property('rawValue').cacheable()
        }),
        applyView: SC.ButtonView.extend({
            layout: { left:10, top: 62, width: 80, height: 22, border: 1},
            classNames: ['theme-button', 'theme-button-blue'],
            classNameBindings: ['isClearBase:is-clear-base'], // adds the is-editable when isEditable is YES
            title: 'Apply',
            action: 'doPaintApply',
            activeLayer: null,
            activeLayerBinding: SC.Binding.oneWay('.parentView.parentView.activeLayer'),
            isClearBase: null,
            isClearBaseBinding: SC.Binding.oneWay('.parentView.toggleView.value'),
            isEnabled: function () {
                return this.parentView.parentView.isItemEnabled(SC.Object.create({ title: 'Apply', action:'doPaintApply', isEnabled: NO, type: 'featurer'}))
            }.property('activeLayer', 'toolState').cacheable(),
            toolState: null,
            toolStateBinding: SC.Binding.oneWay('Footprint.toolController.featurerIsEnabled')
        }),

        toggleView: Footprint.CheckboxInfoView.extend({
             layout: { left:90, width: 140, height:20, top:55 },
             classNames: ['featurer-bar-toggle'],
             title: 'Clear Base Condition',
             valueBinding: 'Footprint.paintingController.isClearBase'
        }),

        redevelopmentToggleView: Footprint.CheckboxInfoView.extend({
             layout: { left:90, width: 140, height:20, top:75 },
             classNames: ['featurer-bar-toggle'],
             title: 'Redevelopment Flag',
             valueBinding: 'Footprint.paintingController.isRedevelopment'
        }),

        bufferView: SC.SegmentedView.extend({
            layout: { top: 100, left:35, height: 26, right: 15 },
            shouldHandleOverflow: NO,
            selectSegmentWhenTriggeringAction: NO,
            itemActionKey: 'action',
            itemTitleKey: 'title',
            itemKeyEquivalentKey: 'keyEquivalent',
            itemValueKey: 'title',
            itemIsEnabledKey: 'isEnabled',

            items: [
                // View and edit the selected item's attributes
                SC.Object.create({ title: 'Undo', keyEquivalent: 'ctrl_u', action: 'doPaintUndo', isEnabledBinding: SC.Binding.oneWay('Footprint.layerSelectionActiveController*featureUndoManager.canUndo').bool(), type: 'chronicler'}),
                SC.Object.create({ title: 'Redo', keyEquivalent: 'ctrl_r', action: 'doPaintRedo', isEnabledBinding: SC.Binding.oneWay('Footprint.layerSelectionActiveController*featureUndoManager.canRedo').bool(), type: 'chronicler'}),
                SC.Object.create({ title: 'Revert', keyEquivalent: '', action: 'doPaintClear', isEnabledBinding: SC.Binding.oneWay('Footprint.featuresActiveController.status').matchesStatus(SC.Record.READY), type: 'chronicler'})
            ]
        })
    }),

    builtFormSectionView: Footprint.BuiltFormSectionView.extend({
        layout: {top: 210}
    })
})