/***
 * Tests the binding and display of data in view Footprint.ProjectTitlebarView.
 */
Footprint.LeftLogoSectionView = SC.View.extend({
    childViews: 'leftlogopaneView1'.w(),
    classNames: "footprint-left-logo-section-view".w(),

    leftlogopaneView1: SC.View.extend({
        childViews: 'leftlogoimageView1'.w(),
        layout: { height: 24, left: 0.05, width: 24 },
        leftlogoimageView1: SC.ImageView.extend({
            projectkey: null,
            regionkey: null,
            projectkeyBinding: SC.Binding.oneWay("Footprint.projectActiveController.key"),
            regionkeyBinding: SC.Binding.oneWay("Footprint.regionActiveController.key"),
            value: function () {
                if (this.get('projectkey') && this.get('regionkey')) {
                    var image_path = 'images/client/%@/%@_logo.png'.fmt(this.get('regionkey'), this.get('projectkey'));
                    return Footprint.STATIC.fmt(image_path);
                }
            }.property('projectkey', 'regionkey').cacheable()
        })
    })

})
//    citytitleView: SC.LabelView.create({
//        classNames: "footprint-left-city-title-view",
//        layout: {left: 0.15, top: .15, width: 0.05},
//        value: 'City:'
//    }),
//    citytitlecontentView: SC.LabelView.create({
//        classNames: "footprint-left-city-content-view",
//        layout: {left: 0.22, top: .15, width: 0.16},
//        valueBinding: SC.Binding.oneWay("Footprint.projectActiveController.name")
//    }),
//
//    countytitleView: SC.LabelView.create({
//        classNames: "footprint-left-county-title-view",
//        layout: {left: 0.35, top: .15, width: 0.09},
//        value: 'County:'
//    }),
//    countytitlecontentView: SC.LabelView.create({
//        classNames: "footprint-left-county-content-view",
//        layout: {left: 0.45, top: .15, width: 0.25},
//        value: 'Orange'
//    }),
//
//    statetitleView: SC.LabelView.create({
//        classNames: "footprint-left-county-title-view",
//        layout: {left: 0.63, top: .15, width: 0.09},
//        value: 'State:'
//    }),
//    statetitlecontentView: SC.LabelView.create({
//        classNames: "footprint-left-county-content-view",
//        layout: {left: 0.72, top: .15, width: 0.25},
//        value: 'California'
//    })


//    leftlogoimageView1: SC.ImageView.extend({
//        value: function () {
//            var image_path = 'images/default_logos/uf_thumbnail_24.png';
//            return Footprint.STATIC + image_path;
//        }.property().cacheable(),
//        layout: { height: 24, left: 0.02, width: 24 }
//    }),
//    