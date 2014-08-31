/***
 * The buttons at the bottom of an info pane.
 * Save, Revert, and Close are enabled according to the bound content's nestedStore
 * status.
 * @type {*|RangeObserver|Class|void}
 */
Footprint.InfoPaneCrudButtonsView = SC.View.extend({
    childViews: 'closeButtonView revertButtonView createButtonView saveButtonView'.w(),
    classNames: ['footprint-add-building-buttons-view'],
    // The name used to describe the Record type being edited. Used for the doCreate[recordTypeName] action
    recordTypeName: null,
    content: null,
    /***
     * Required. The layout of the close button if visible.
     */
    closeButtonLayout: null,
    /***
     * Optional. The layout of the revert button if visible.
     */
    revertButtonLayout: null,
    /***
     * Optional. The layout of the created button if visible.
     */
    createButtonLayout: null,
    /***
     * Required. The layout of the save button if visible.
     */
    saveButtonLayout: null,

    closeButtonView: SC.ButtonView.design({
        layoutBinding: SC.Binding.oneWay('.parentView.closeButtonLayout'),
        title: 'Close',
        action: 'doPromptCancel',
        isCancel: YES
    }),
    revertButtonView: SC.ButtonView.design({
        layoutBinding: SC.Binding.oneWay('.parentView.revertButtonLayout').transform(function(value) {
            return value || {};
        }),
        isVisibleBinding: SC.Binding.oneWay('.parentView.revertButtonLayout').bool(),
        title: 'Revert',
        action: 'doRevert',
        isEnabledBinding: SC.Binding.and('.parentView*content.nestedStore.hasChanges', '.parentView*content.nestedStore.hasNoBusyRecords')
    }),
    createButtonView: SC.ButtonView.design({
        layoutBinding: SC.Binding.oneWay('.parentView.createButtonLayout').transform(function(value) {
            return value || {};
        }),
        isVisibleBinding: SC.Binding.oneWay('.parentView.createButtonLayout').bool(),
        recordTypeName: null,
        recordTypeNameBinding: SC.Binding.oneWay('.parentView.recordTypeName'),
        icon: 'add-icon',
        title: function() {
            return 'New %@'.fmt(this.get('recordTypeName'));
        }.property('recordTypeName').cacheable(),
        action: function() {
            return 'doCreate%@'.fmt(this.get('recordTypeName'));
        }.property('recordTypeName').cacheable()
    }),

    saveButtonView: SC.ButtonView.design({
        layoutBinding: SC.Binding.oneWay('.parentView.saveButtonLayout'),
        title: 'Save',
        action: 'doSave',
        isEnabledBinding: SC.Binding.and('.parentView*content.nestedStore.hasChanges', '.parentView*content.nestedStore.hasNoBusyRecords')
    })
})
