sc_require('models/key_mixin');
sc_require('models/deletable_mixin');


Footprint.AnalysisModule = Footprint.Record.extend(Footprint.Key, Footprint.Deletable, {
    deleted: SC.Record.attr(Boolean),

    config_entity: SC.Record.toOne("Footprint.ConfigEntity", {
        isMaster: YES
    }),
    // The base class version of the tools. Subclass versions are resolved by the AnalysisModule states
    analysis_tools: SC.Record.toMany("Footprint.AnalysisTool", {
        nested: YES
    }),

    configuration: SC.Record.attr(Object),
    // Defines an undo manager for this instance
    undoManager: null
});

