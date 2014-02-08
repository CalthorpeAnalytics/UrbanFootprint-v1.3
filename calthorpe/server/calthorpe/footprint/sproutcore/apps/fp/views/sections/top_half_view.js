sc_require('views/sections/scenario_section_view');
sc_require('views/sections/result_section_view');

Footprint.TopHalfView = SC.View.extend({

    childViews: 'upperSplitView'.w(),
    classNames: "footprint-top-half-view".w(),
    upperSplitView: SC.SplitView.extend({
        layoutDirection: SC.LAYOUT_HORIZONTAL,
        defaultThickness: 0.3,
        topLeftView: Footprint.ScenarioSectionView,
        bottomRightView: Footprint.ResultSectionView
    })
});
