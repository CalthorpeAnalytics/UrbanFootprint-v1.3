sc_require('views/sections/layer_section_view');
sc_require('views/sections/tool_section_view');
sc_require('views/sections/built_form_section_view');

Footprint.SidebarView = SC.SplitView.extend({
    classNames: "footprint-sidebar-view".w(),
    childViews:'layerLibraryView toolSetView builtFormsView'.w(),
    layoutDirection: SC.LAYOUT_VERTICAL,
    autoresizeBehavior:SC.RESIZE_TOP_LEFT,

    topLeftView: Footprint.LayerSectionView.extend({
        layout: { height:150}
    }),
    bottomRightView: SC.View.extend({
        childViews:'toolsetView builtFormsView'.w(),
        toolsetView: Footprint.ToolSectionView.extend({
            layout: {height:130}
        }),
        builtFormsView: Footprint.BuiltFormSectionView.extend({
            layout: { top:130, bottom:0 }
        })
    })
});
