/**
 * Created with PyCharm.
 * User: calthorpe
 * Date: 11/14/13
 * Time: 3:54 PM
 * To change this template use File | Settings | File Templates.
 */

sc_require('views/info_views/analytics/fiscal_model_management_view');


Footprint.analyticModelManagementView = SC.View.extend({
    classNames: "footprint-analytic-model-management-view".w(),
    childViews: 'contentView'.w(),
    contentView: SC.SegmentedView.extend({
        layout: { top:.02, height: 0.98, right: 4, width: 110 },
        layoutDirection: SC.LAYOUT_VERTICAL,
        selectSegmentWhenTriggeringAction: YES,
        itemTitleKey: 'title',
        itemValueKey: 'value',
        items: [
                {title: 'Travel', value: ''},
                {title: 'Fiscal', value: 'Footprint.fiscalModelManagementView'},
                {title: 'Water', value: ''},
                {title: 'Building Energy', value: ''},
                {title: 'Emissions', value: ''},
                {title: 'Public Health', value: ''}
            ],
        nowShowingBinding: '.parentView.nowShowing'


    })

})