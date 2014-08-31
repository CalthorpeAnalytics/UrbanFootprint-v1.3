
// Just a base class for more interesting subclasses
Footprint.AnalysisTool = Footprint.Record.extend(Footprint.Key, {
    config_entity: SC.Record.toOne("Footprint.ConfigEntity", {}),
    behavior: SC.Record.toOne("Footprint.Behavior", {})
});

Footprint.EnvironmentalConstraintUpdaterTool = Footprint.AnalysisTool.extend({
    primaryKey: 'unique_id',
    config_entity: SC.Record.toOne("Footprint.ConfigEntity"),
    environmental_constraint_percents: SC.Record.toMany('Footprint.EnvironmentalConstraintPercent', {nested: YES}),
    undoManager: null
});

Footprint.EnvironmentalConstraintPercent = Footprint.Record.extend({
    db_entity: SC.Record.toOne("Footprint.DbEntity", {nested: YES}),
    analysis_tool: SC.Record.toOne("Footprint.EnvironmentalConstraintUpdaterTool"),
    percent: SC.Record.attr(Number),
    priority: SC.Record.attr(Number)
});
