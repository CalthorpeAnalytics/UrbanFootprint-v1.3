/***
 * Tests the binding and display of data in view Footprint.ProjectTitlebarView.
 */

Footprint.RightLogoSectionView = SC.View.extend({
    childViews: 'titleView rightlogopaneView1'.w(),
    classNames: "footprint-right-logo-section-view".w(),

    titleView: SC.LabelView.create({
        classNames: "footprint-right-logo-title-view",
        name: null,
        nameBinding: SC.Binding.oneWay("Footprint.regionActiveController.name"),
        value: function () {
            if (this.get('name'))
                return "%@ UrbanFootprint Scenario Planning Model".fmt(this.get('name'), this.get('name'))
        }.property('name').cacheable(),
        layout: {left: 0.1, top: .15}
    }),

    rightlogopaneView1: SC.View.extend({
        childViews: 'rightlogoimageView1'.w(),
        layout: {right: 0.02, width: 143},
        rightlogoimageView1: SC.ImageView.extend({
            key: null,
            keyBinding: SC.Binding.oneWay("Footprint.regionActiveController.key"),
            value: function () {
                if (this.get('key')) {
                    var image_path = 'images/client/%@/%@_logo.png'.fmt(this.get('key'), this.get('key'));
                    return Footprint.STATIC.fmt(image_path);
                }
            }.property('key').cacheable()
        })
    })


})
