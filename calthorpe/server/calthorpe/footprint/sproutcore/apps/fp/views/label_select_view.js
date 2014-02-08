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
sc_require('views/mixins/view_validation');
sc_require('views/mixins/selected_item');
sc_require('views/editable_model_string_view');
sc_require('views/menu_button_view');

Footprint.LabelSelectView = SC.PopupButtonView.extend(Footprint.ViewValidation, {

    classNames:'footrint-label-select-view'.w(),
    requiredProperties: 'title menuItems'.w(),
    validationControllerBinding: SC.Binding.oneWay('.controller'),
    layout: {height: 24, width: .8, left: 0.1},

    /**
     * Required. the items to select from.
     */
    content: null,
    selection:null,
    includeNullItem:NO,
    nullTitle: null,

    // This is all hacked since firstSelection won't update as it should
    selectionDiDUpdate:NO,
    firstSelectedItem:null,
    firstSelectedItemBinding:SC.Binding.oneWay('*selection.selection.firstObject'),
    selectedItem: function() {
        if (this.get('selectionDidUpdate')) {
            this.set('selectionDidUpdate', NO);
        }
        return this.getPath('selection.selection.firstObject');
    }.property('selectionDidUpdate', 'firstSelectedItem').cacheable(),

    contentStatus: null,
    contentStatusBinding: SC.Binding.oneWay('*content.status'),

    /**
     * Required. The attribute of each item to display in the menu and label
     */
    itemTitleKey: null,

    // Resolves the attribute value of itemTitleKey on the value.
    title: function () {
        var selectedItem = this.get('selectedItem');
        return selectedItem && this.get('itemTitleKey') ? selectedItem.get(this.get('itemTitleKey')) :selectedItem;
    }.property('contentStatus', 'selectedItem', 'itemTitleKey').cacheable(),

    itemsStatus: null,
    itemsStatusBinding: SC.Binding.oneWay('*items.status'),
    menuItems: function () {
        if (this.getPath('contentStatus') === SC.Record.READY_CLEAN ||
            (this.get('content') && !this.getPath('content.status'))) {
                // If includeNullItem make an ObjectController whose content is null
            return (this.get('includeNullItem') ? [this.get('nullItem')] : []).concat(
                // Wrap each item of the content as an ObjectController. This allows us to add useful properties
                // like isSelected and the itemTitleKey gets delegated to the content
                this.get('content').map(function (item) {
                    return SC.ObjectController.create({
                        itemContainer: this,
                        selectedValue: null,
                        selectedValueBinding: SC.Binding.oneWay('.itemContainer.selectedItem'),
                        content: item,
                        isSelected: function () {
                            return this.get('content') === this.get('selectedValue');
                        }.property('content', 'selectedValue').cacheable()
                    })
            }, this))
        }
    }.property('contentStatus', 'content').cacheable(),

    /**
     * Creates an SC.ObjectController to server as the null menu item
     */
    nullItem: function() {
        var controller = SC.ObjectController.create({
            itemContainer: this,
            selectedValue: null,
            selectedValueBinding: SC.Binding.oneWay('.itemContainer.selectedItem'),
            content: null, // null is the value of this item
            isSelected: function () {
                return null === this.get('selectedValue');
            }.property('content', 'selectedValue').cacheable()
        });
        // Set the variable itemTitleKey.
        controller.set(this.get('itemTitleKey'), this.get('nullTitle'));
        return controller;
    }.property('itemTitleKey', 'nullTitle').cacheable(),

    menu: SC.MenuPane.extend({
        layout: {width: 200},
        itemsBinding: SC.Binding.oneWay('*anchor.menuItems'),
        itemCheckboxKey: 'isSelected',
        itemTitleKeyBinding: SC.Binding.oneWay('.anchor.itemTitleKey').transform(function(value) {
            // default to content for primitives, otherwise the titleKey will delegate through content
            return value || 'content';
        }),
        /**
         * When the menu's selectedItem changes we change the controller's selection to reflect it.
         */
        selectedItemDidChange: function () {
            // Resolve the content from the selected objectController instance
            var content = this.getPath('selectedItem.content');
            // Set the SelectionSupport mixin implementor selection
            this.getPath('anchor.selection').selectObject(content);
            this.setPath('anchor.selectionDidUpdate', YES); // Hack to force update
        }.observes('selectedItem')
    }),

    init: function () {
        sc_super();
        this.setPath('menu.anchor', this);
    }
});
