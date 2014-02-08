/**
 * Created with PyCharm.
 * User: calthorpe
 * Date: 12/11/13
 * Time: 5:19 PM
 * To change this template use File | Settings | File Templates.
 */


Footprint.BuiltFormItemsScrollView = SC.View.extend({

    childViews: ['overlayView', 'copyButtonView', 'deleteButtonView', 'scrollView'],

    media: null,
    content: null,
    selection: null,
    // recordType is used for cloning
    recordType: null,

    overlayView: Footprint.OverlayView.extend({
        contentBinding: SC.Binding.from('.parentView.content'),
        statusBinding:SC.Binding.oneWay('*content.status')
    }),

    copyButtonView: Footprint.CopyButtonView.extend({
        layout: { left: 0, width: 16, top: 0, height: 16 },
        action: 'doCloneRecord',
        // We want to clone the selected item
        contentBinding: SC.Binding.oneWay('.parentView*selection.firstObject'),
        recordTypeBinding: SC.Binding.oneWay('.parentView.recordType'),
        isVisibleBinding: SC.Binding.oneWay('.content').bool()
    }),

    deleteButtonView: Footprint.DeleteButtonView.extend({
        layout: { left: 24, width: 16, top: 0, height: 16},
        action: 'doPromptDeleteRecord',
        // We want to delete the selected item
        contentBinding: SC.Binding.oneWay('.parentView*selection.firstObject'),
        isVisibleBinding: SC.Binding.oneWay('.content').bool()
    }),

    scrollView: SC.ScrollView.extend({
        layout: { top: 20},
        classNames: ['footprint-built-form-scroll-view'],

        media: null,
        mediaBinding: SC.Binding.oneWay('.parentView.media'),

        content: null,
        contentBinding:SC.Binding.oneWay('.parentView.content'),

        selection: null,
        selectionBinding: SC.Binding.from('.parentView.selection'),

        contentView: SC.SourceListView.extend({
            isEnabledBinding: SC.Binding.oneWay('.content').bool(),
            rowHeight: 20,
            actOnSelect: NO,
            contentIconKey: 'medium',
            contentValueKey: 'name',
            contentBinding: SC.Binding.oneWay('.parentView.parentView.content'),
            selectionBinding: SC.Binding.from('.parentView.parentView.selection'),

            exampleView: SC.View.extend(SC.Control, SC.ContentDisplay, {
                classNames: ['footprint-built-form-item'],
                contentDisplayProperties: ['name'],
                classNameBindings: ['isNew:new-record', 'isDirty:dirty-record'],
                childViews:['progressOverlayView'],

                status: null,
                statusBinding: SC.Binding.oneWay('.content.status'),
                isNew: function() {
                    return this.get('status') === SC.Record.READY_NEW;
                }.property('status').cacheable(),

                isDirty: function() {
                    return this.get('status') === SC.Record.READY_DIRTY;
                }.property('status').cacheable(),

                progressOverlayView: Footprint.ProgressOverlayView.extend({
                    layout: { left:.5, width:.5, centerY: 0, height: 16},
                    contentBinding: SC.Binding.oneWay('.parentView.content')
                }),

                render: function(context) {
                    // Color swab
                    var color = this.getPath('content.medium.content.fill.color');
                    context.begin()
                        .addClass(this.getPath('theme.classNames'))
                        .addClass(['sc-view', 'footprint-medium-color'])
                        .setStyle({ 'background-color': color })
                        .end();
                    // Label
                    context.begin()
                        .addClass(this.getPath('theme.classNames'))
                        .addClass(['sc-view', 'sc-label-view', 'footprint-built-form-item-label-view'])
                        .push(this.getPath('content.name'))
                        .end();
                },
                update: function ($context) {
                    $context.find('.footprint-medium-color').css('background-color', this.getPath('content.medium.content.fill.color'));
                    $context.find('.footprint-built-form-item-label-view').text(this.getPath('content.name'));
                }
            })
        })
    })
})