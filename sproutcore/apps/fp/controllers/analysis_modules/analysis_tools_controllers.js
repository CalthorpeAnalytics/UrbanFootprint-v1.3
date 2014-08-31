sc_require('models/analysis_tool_models')

Footprint.environmentalConstraintUpdaterToolController = SC.ArrayController.create({
    allowsEmptySelection:YES,
    recordType: Footprint.EnvironmentalConstraintUpdaterTool
});

Footprint.environmentalConstraintUpdaterToolEditController = Footprint.EditArrayController.create({
    allowsEmptySelection:YES,
    sourceController: Footprint.environmentalConstraintUpdaterToolController,
    isEditable:YES,
    recordsAreUpdating: NO,
    recordType: Footprint.EnvironmentalConstraintUpdaterTool,
    parentEntityKey: 'config_entity',
    parentRecordBinding: SC.Binding.oneWay('Footprint.scenariosController*selection.firstObject')
});

/**
 * The AnalysisTools of the current AnalysisModules.
 * These are base class instances. The analysisToolControllerLookup
 * resolves them to a controller containing the subclass
 */
Footprint.analysisToolsController = SC.ArrayController.create({
      allowsEmptySelection: NO,
      analysisModule: null,
      analysisModuleBinding: SC.Binding.oneWay('Footprint.analysisModulesController*selection.firstObject'),
      contentBinding: SC.Binding.oneWay('*analysisModule.analysis_tools')
});

Footprint.analysisToolControllerLookup = SC.Object.create({
    environmental_constraint_updater_tool: Footprint.environmentalConstraintUpdaterToolController
});

Footprint.analysisToolEditControllerLookup = SC.Object.create({
    environmental_constraint_updater_tool: Footprint.environmentalConstraintUpdaterToolEditController
});

