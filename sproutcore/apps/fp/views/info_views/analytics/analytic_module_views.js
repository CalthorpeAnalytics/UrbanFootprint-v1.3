/**
 * Created with PyCharm.
 * User: calthorpe
 * Date: 1/13/14
 * Time: 3:03 PM
 * To change this template use File | Settings | File Templates.
 */


Footprint.ManageModuleView = SC.View.extend({
    classNames: "footprint-manage-module-view".w(),
    childViews: ['titleView', 'executeModuleView', 'editPolicyView', 'infoButtonView'],
    layout: {height: 120},
    title: null,
    titleBinding: SC.Binding.oneWay('.parentView.title'),
    executeModuleAction: null,
    executeModuleActionBinding: SC.Binding.oneWay('.parentView.executeModuleAction'),
    editAssumptionsAction: null,
    editAssumptionsActionBinding: SC.Binding.oneWay('.parentView.editAssumptionsAction'),

    titleView: SC.LabelView.extend({
        classNames: "footprint-analytic-module-title-view".w(),
        layout: {top: 15, left: 40, right: 40, height: 24},
        valueBinding: SC.Binding.oneWay('.parentView.title'),
        textAlign: SC.ALIGN_CENTER
    }),

    infoButtonView: SC.ButtonView.extend({
        classNames: "footprint-info-button-view".w(),
        layout: {left: 10, height: 24, width: 24, top: 13},
        childViews: ['iconView'],
        menuItems: function () {
            return this.get('defaultMenuItems');
        }.property('defaultMenuItems').cacheable(),
        defaultMenuItems: '--',
        iconView: SC.ImageView.extend({
            layout: {left: 2, width: 20, height: 20, top: 1},
            value: sc_static('fp:images/info_logo.png')
        })
    }),

    executeModuleView: SC.ButtonView.extend({
            layout: { left: 40, right: 40, height: 24, border: 1, top:55, width: 200},
            title: 'Run Module',
            actionBinding: SC.Binding.oneWay('.parentView.executeModuleAction')
    }),

    editPolicyView: SC.ButtonView.extend({
            layout: { left: 40, right: 40, height: 24, border: 1, top:80, width: 200},
            title: 'Edit Assumptions',
            actionBinding: SC.Binding.oneWay('.parentView.editAssumptionsAction')
    })
});