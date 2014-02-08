
Footprint.LoadingPane = SC.MainPane.extend({
    childViews: 'loadingView progressView'.w(),

    loadingView: SC.ImageView.extend({
        classNames:'loading-image'.w(),
        useCanvas:NO,
        layout: {centerX: 0, centerY:0, width:500, height:500},
        value:sc_static('images/loading.png')
    }),
    progressView: SC.ProgressView.extend({
        layout: {centerX:.0001, centerY:0, width:.2, height:16, top:0.9},
        valueBinding:SC.Binding.oneWay('Footprint.loadingStatusController.content'),
        minimum:0,
        maximum:10
    })
});

