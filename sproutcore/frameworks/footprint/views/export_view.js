/**
 * Created by calthorpe on 12/15/13.
 */

Footprint.ExportView = SC.View.extend({
    classNames: ['footprint-export-view'],
    childViews: ['exportButtonView'], //, 'copyButtonView'],

    content: null,
    /***
     * YES if the export is simply exporting the content
     */
    isLocalExport: null,

    exportButtonView: SC.ButtonView.extend({
        classNames: ['footprint-export-button-view'],
        layout: {width:100, right:0},
        title: 'Export as CSV',
        isLocalExport: null,
        isLocalExportBinding: SC.Binding.oneWay('.parentView.isLocalExport'),
        action: 'doExport',
        content: null,
        contentBinding: SC.Binding.oneWay('.parentView.content')
    }),

    copyButtonView: SC.ButtonView.extend({
        classNames: ['footprint-export-button-view'],
        layout: {left:0.5, right:0},
        title: 'Copy as CSV',
        action: 'doCopy',
        content: null,
        contentBinding: SC.Binding.oneWay('.parentView.content')
    })
});