sc_require('views/info_views/table_info_view')

Footprint.FeatureTableInfoView = Footprint.TableInfoView.extend({
    classNames: "footprint-query-info-results-view".w(),
    layout: {top: 125, bottom:.05, left:0, right:0.4},
    status:null,
    title: function() {
        return '%@ Query or Selection Results'.fmt(
            this.get('status') & SC.Record.READY || this.get('status') === SC.Record.EMPTY ? this.getPath('content.length') || 0 : 'Loading');
    }.property('content', 'status').cacheable(),

    layerSelection: null,
    layerSelectionStatus: null,
    layerSelectionStatusBinding: SC.Binding.oneWay('*layerSelection.status'),

    // The overlay is visible if either feature of layerSelection status is BUSY
    overlayStatus: function() {
        return Math.max(this.get('status'), this.get('layerSelectionStatus'));
    }.property('status', 'layerSelectionStatus').cacheable(),

    columns: function() {
        if (!(this.get('layerSelectionStatus') & SC.Record.READY))
            return [];
        var layerSelection = this.get('layerSelection');
        return (layerSelection.get('result_fields') || []).map(function(field) {
            return layerSelection.getPath('result_field_title_lookup.%@'.fmt(field));
        });
    }.property('layerSelectionStatus').cacheable(),
    mapProperties: function() {
        if (!(this.get('layerSelectionStatus') & SC.Record.READY))
            return SC.Object.create();
        return mapToSCObject(
            Footprint.layerSelectionEditController.getPath('result_fields') || [],
            function(field) {
                return [Footprint.layerSelectionEditController.getPath('result_field_title_lookup.%@'.fmt(field)), field];
            },
            this
        );
    }.property('layerSelectionStatus').cacheable(),
    // Enable the zoom to selection button
    zoomToSelectionIsVisible: YES
});