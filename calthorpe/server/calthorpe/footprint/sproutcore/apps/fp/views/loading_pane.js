sc_require('views/sections/top_half_view');
sc_require('views/sections/bottom_half_view');
sc_require('views/sections/project_section_view');
sc_require('views/sections/right_logo_section_view');
sc_require('views/sections/left_logo_section_view');

Footprint.LoadingPane = SC.MainPane.extend({
    childViews: 'loadingView progressView'.w(),

    loadingView: SC.ImageView.extend({
        classNames:'loading-image'.w(),
        useCanvas:NO,
        layout: {centerX:.0001, centerY:.0001, width:500, height:500},
        value:sc_static('images/loading.png')
    }),
    progressView: SC.ProgressView.extend({
        layout: {centerX:.0001, centerY:0, width:.2, height:16},
        valueBinding:SC.Binding.oneWay('Footprint.loadingStatusController.content'),
        minimum:0,
        maximum:10
    })
});

