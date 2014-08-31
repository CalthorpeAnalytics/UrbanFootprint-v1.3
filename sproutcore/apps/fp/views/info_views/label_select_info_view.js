/***
 * A LabelSelectView along with a label
 * @type {*|SC.RangeObserver|Class|void}
 */
Footprint.LabelSelectInfoView = SC.View.extend(SC.Control, {
    layout: { height: 40 },
    classNames: ['footprint-editable-view'],
    childViews:['nameTitleView', 'labelSelectView'],
    title: null,

    content: null,
    itemTitleKey:null,
    includeNullItem:null,
    nullTitle:null,
    selection: null,
    action: null,

    nameTitleView: SC.LabelView.extend({
        layout: {height:12},
        classNames: ['footprint-editable-title-view'],
        valueBinding: SC.Binding.oneWay('.parentView.title')
    }),

    labelSelectView: Footprint.LabelSelectView.extend({
        layout: { top: 12, height: 24 },
        classNames:['footprint-label-select-info-label-select-view'],
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        selectionBinding: '.parentView.selection',
        itemTitleKeyBinding: SC.Binding.oneWay('.parentView.itemTitleKey'),
        includeNullItemBinding: SC.Binding.oneWay('.parentView.includeNullItem'),
        nullTitleBinding: SC.Binding.oneWay('.parentView.nullTitle'),
        selectionActionBinding: SC.Binding.oneWay('.parentView.action')
    })
});
