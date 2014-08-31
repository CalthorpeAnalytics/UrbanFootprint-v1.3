
Footprint.FeatureClassConfiguration = Footprint.Record.extend({
    // Add attributes whenever they need to be observed
    source_from_origin_layer_selection: SC.Record.attr(Boolean),
    // Set to the layer id being used for the source LayerSelection
    origin_layer_id: SC.Record.attr(Number),
    generated: SC.Record.attr(Boolean),
    // abstract_class_name is maintained during cloning
    abstract_class_name: SC.Record.attr(String),
    primary_key: SC.Record.attr(String)
});