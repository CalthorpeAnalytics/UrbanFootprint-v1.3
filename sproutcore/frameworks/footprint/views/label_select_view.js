/*
 * UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
 *
 * Copyright (C) 2013 Calthorpe Associates
 *
 * This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
 *
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
 */
sc_require('views/editable_model_string_view');
sc_require('views/menu_button_view');

Footprint.LabelSelectView = SC.PopupButtonView.extend({

    classNames:'footprint-label-select-view theme-button theme-button-gray'.w(),
    requiredProperties: 'title menuItems'.w(),
    validationControllerBinding: SC.Binding.oneWay('.controller'),
    layout: {height: 24, width: .8, left: 0.1},

    /**
     * Required. the items to select from.
     */
    content: null,
    selection:null,
    // Indicates if items in the list can be selected
    isSelectable: YES,
    includeNullItem:NO,
    nullTitle: null,

    // The max height of the popup panel
    maxHeight: 72,

    // This is all hacked since firstSelection won't update as it should
    firstSelectedItem:null,
    firstSelectedItemBinding:SC.Binding.oneWay('*selection.firstObject'),
    selectedItem: function() {
        if (this.get('selectionDidUpdate')) {
            this.set('selectionDidUpdate', NO);
        }
        return this.getPath('selection.firstObject');
    }.property('firstSelectedItem').cacheable(),

    contentStatus: null,
    contentStatusBinding: SC.Binding.oneWay('*content.status'),

    selectedItemStatus: null,
    selectedItemStatusBinding: SC.Binding.oneWay('*selectedItem.status'),

    /**
     * The attribute of each item to display in the menu and label. null for primitives
     */
    itemTitleKey: null,

    // Resolves the attribute value of itemTitleKey on the value.
    title: function () {
        var selectedItem = this.get('selectedItem');
        var nullTitle = this.get('nullTitle');
        return selectedItem && this.get('itemTitleKey') ? selectedItem.get(this.get('itemTitleKey')) : nullTitle;
    }.property('selectedItemStatus', 'selectedItem', 'itemTitleKey', 'nullTitle').cacheable(),

    itemsStatus: null,
    itemsStatusBinding: SC.Binding.oneWay('*items.status'),
    menuItems: function () {
        if (this.getPath('contentStatus') & SC.Record.READY ||
            (this.get('content') && !this.getPath('content.status'))) {
                // If includeNullItem make an ObjectController whose content is null
            return (this.get('includeNullItem') ? [this.get('nullItem')] : []).concat(this.get('content').toArray());
        }
    }.property('contentStatus', 'content').cacheable(),

    /**
     * Creates an SC.ObjectController to server as the null menu item
     */
    nullItem: function() {
        var obj = SC.Object.create();
        // Set the variable itemTitleKey.
        obj.set(this.get('itemTitleKey'), this.get('nullTitle'));
        return obj;
    }.property('itemTitleKey', 'nullTitle').cacheable(),

    menu: SC.PickerPane.extend({
        layout: {top: 16, height: 0, left:0, width:200},
        maxHeightBinding: SC.Binding.oneWay('*anchor.maxHeight'),

        popup: function (anchorViewOrElement, preferType, preferMatrix, pointerOffset) {
            sc_super();
            if (this._anchorView) {
                this.set('anchor', this._anchorView);
                this.adjust('width', this._anchorView.getPath('frame.width'));
            }
        },
        contentBinding: SC.Binding.oneWay('*anchor.menuItems'),
        selection: null,
        selectionBinding: '*anchor.selection',
        isSelectable: null,
        isSelectableBinding: '*anchor.isSelectable',
        // default to content for primitives, otherwise the titleKey will delegate through content
        itemTitleKeyBinding: SC.Binding.oneWay('*anchor.itemTitleKey'),

        contentView: SC.ScrollView.extend({

            content: null,
            contentBinding: SC.Binding.oneWay('.parentView.content'),
            selection: null,
            selectionBinding: '.parentView.selection',
            isSelectable: null,
            isSelectableBinding: '.parentView.isSelectable',
            itemTitleKey:null,
            itemTitleKeyBinding:SC.Binding.oneWay('.parentView.itemTitleKey'),

            contentView: SC.SourceListView.extend({
                classNames:'footprint-label-select-content-view'.w(),
                rowHeight: 18,
                actOnSelect:YES,
                action:'doPickSelection',

                contentBinding: SC.Binding.oneWay('.parentView.parentView.content'),
                selectionBinding: '.parentView.parentView.selection',
                isSelectableBinding: SC.Binding.oneWay('.parentView.parentView.isSelectable'),
                itemTitleKey:null,
                itemTitleKeyBinding:SC.Binding.oneWay('.parentView.parentView.itemTitleKey'),
                isEnabledBinding: SC.Binding.oneWay('.content').bool(),

                frameDidChange: function() {
                    if (!this.getPath('pane.maxHeight'))
                        return;
                    if (this.getPath('frame.height') !== this._height) {
                        this.get('pane').adjust('height', [this.getPath('pane.maxHeight'), this.getPath('frame.height')].min());
                        this.invokeLast(function() { this.getPath('pane.contentView').notifyPropertyChange('frame'); });
                    }
                    this._height = this.getPath('frame.height');
                }.observes('.frame'),

                exampleView: SC.View.extend(SC.Control, {
                    classNames:'footprint-label-select-item-view'.w(),
                    childViews:['labelView'],

                    itemTitleKey:null,
                    itemTitleKeyBinding:SC.Binding.oneWay('.parentView.itemTitleKey'),

                    labelView: SC.LabelView.extend({
                        classNames:'footprint-label-select-item-label-view'.w(),
                        layout: {top: 0, left: 0},
                        contentBinding: SC.Binding.oneWay('.parentView.content'),
                        contentValueKey: null,
                        contentValueKeyBinding: SC.Binding.oneWay('.parentView.itemTitleKey'),
                        value: function() {
                            if (this.get('content') && !this.get('contentValueKey'))
                                // content is string case. Otherwise we rely on content+contentValueKey
                                return this.get('content');
                            return this.get('content') && this.get('content').getPath(this.get('contentValueKey'));
                        }.property('contentValueKey', 'content')
                    })
                })
            })
        })
    })
});
