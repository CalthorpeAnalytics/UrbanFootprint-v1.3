/**
 *
 * Created by calthorpe on 2/12/14.
 */

sc_require('controllers/controllers');
sc_require('models/analysis_module_model');

Footprint.analysisModulesController = SC.ArrayController.create(Footprint.RecordControllerChangeSupport, {
    selectedItemDidChangeEvent:'analysisModuleDidChange',
    contentDidChangeEvent:'analysisModulesDidChange',
    // Convenient UI flag.
    analysisModuleSectionIsVisible: NO
});

/***
 * The controller used to edit the AnalysisModules, which for now just means saving them in order to
 * run them.
 */
Footprint.analysisModulesEditController = Footprint.EditArrayController.create({
    allowsEmptySelection:NO,
    firstSelectableObject: function() {
        return (this.get('content') || []).find(function(analysisModule) {
            // Pick core if it exists
            return analysisModule.get('key')=='core'
        }) || this.get('firstObject');
    }.property('content'),
    contentBinding:SC.Binding.oneWay('Footprint.projectActiveController.children'),
    sourceController: Footprint.analysisModulesController,
    isEditable:YES,
    recordType: 'Footprint.AnalysisModule',
    parentEntityKey: 'config_entity',
    parentRecordBinding: SC.Binding.oneWay('Footprint.scenariosController*selection.firstObject'),
    nestedStore:null,
    selectionBinding: SC.Binding.from('Footprint.analysisModulesController.selection')
});

Footprint.environmentalConstraintModuleController = SC.ArrayController.create({
    allowsEmptySelection:YES,
    recordType: Footprint.EnvironmentalConstraintModule
});

Footprint.environmentalConstraintModuleEditController = Footprint.EditArrayController.create({
    allowsEmptySelection:YES,
    sourceController: Footprint.environmentalConstraintModuleController,
    isEditable:YES,
    recordsAreUpdating: NO,
    recordType: Footprint.EnvironmentalConstraintModule,
    parentEntityKey: 'config_entity',
    parentRecordBinding: SC.Binding.oneWay('Footprint.scenariosController*selection.firstObject')
});

Footprint.supplementalModuleControllerLookup = SC.Object.create({
    environmental_constraint: Footprint.environmentalConstraintModuleController
})

Footprint.supplementalModuleEditControllerLookup = SC.Object.create({
    environmental_constraint: Footprint.environmentalConstraintModuleEditController
})
