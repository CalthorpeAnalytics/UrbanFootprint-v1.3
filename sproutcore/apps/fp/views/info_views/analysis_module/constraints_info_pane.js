/**
 * Created with PyCharm.
 * User: calthorpe
 * Date: 12/9/13
 * Time: 10:08 AM
 * To change this template use File | Settings | File Templates.
 */
sc_require('views/info_views/built_form/urban_built_forms/manage_building_view');

Footprint.ConstraintsInfoPane = SC.PalettePane.extend({
    classNames: ['footprint-add-building-pane'],
    layout: { right: 300, centerY: 50, width: 450, height: 300 },
    nowShowing:function() {
        return this.getPath('context.nowShowing') || 'Footprint.EnvironmentalConstraintsManagementView';
    }.property('context').cacheable(),

    contentView: SC.ContainerView.design({
        classNames: ['footprint-add-built-form-container-view'],
        childViews: ['toggleButtonsView'],

        recordType: null,
        // The recordType is stored in the contentView of this view (the nowShowing view)
        recordTypeBinding: SC.Binding.oneWay('*contentView.recordType'),
        // Likewise for the current selectedItem
        selectedItemBinding: SC.Binding.oneWay('*contentView.selectedItem'),

        nowShowingBinding: SC.Binding.oneWay('.parentView.nowShowing'),

        toggleButtonsView: SC.SegmentedView.extend({
            layout: {top: 5, centerY:0, height:22},
            crudType: 'view',
            selectSegmentWhenTriggeringAction: YES,
            itemTitleKey: 'title',
            itemActionKey: 'action',
            itemValueKey: 'title',
            items: [
                {title: 'Environmental',  action: '', recordType:''},
                {title: 'Redevelopment', action: '', recordType:''}
            ],
            value: null
        })
    })
})



