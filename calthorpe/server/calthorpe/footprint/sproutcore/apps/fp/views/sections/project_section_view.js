sc_require('views/label_select_view');
sc_require('views/section_titlebars/label_select_toolbar_view');

/***
 * Tests the binding and display of data in view Footprint.ProjectTitlebarView.
 */
Footprint.ProjectSectionView = SC.View.extend({
    childViews: 'toolbarView'.w(),
    classNames: "footprint-project-section-view".w(),

    toolbarView: Footprint.LabelSelectToolbarView.extend({
//        layout: { centerX: .001, width:0.9},
        layout: { height: 24},
        anchorLocation: SC.ANCHOR_TOP,
        controlSize: SC.REGULAR_CONTROL_SIZE,
        title: 'Edit',

        classNames: "footprint-toolbar-view".w(),
        contentBinding: SC.Binding.oneWay('Footprint.projectsController.content'),
        selectionBinding: SC.Binding.oneWay('Footprint.projectsController'),
        itemTitleKey: 'name'
    })
});

