/* 
 * UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
 * 
 * Copyright (C) 2012 Calthorpe Associates
 * 
 * This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
 * 
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * 
 * Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
 */

Footprint.BuiltFormSectionView = SC.View.extend({
    childViews: 'toolbarView listView overlayView'.w(),
    classNames: "footprint-built-form-section-view".w(),

    toolbarView: Footprint.LabelSelectToolbarView.extend({
        classNames: "footprint-built_form-toolbar-view".w(),
        titleViewLayout: {height: 24},
        controlSize: SC.REGULAR_CONTROL_SIZE,
        icon: sc_static('images/section_toolbars/pulldown.png'),

        contentBinding: 'Footprint.builtFormSetsController.content',
        isVisibleBinding: SC.Binding.oneWay('Footprint.builtFormSetsController.status').matchesStatus(SC.Record.READY),
        selectionBinding: 'Footprint.builtFormSetsController.selection',
        recordType: Footprint.BuiltForm,
        activeRecordBinding: SC.Binding.oneWay('Footprint.builtFormActiveController.content'),

        title: null,
        itemTitleKey: 'name',

        menuItems: [
            // View and edit the selected item's attributes
            { title: 'Manage Urban Built Forms', action: 'doManageBuiltForms'},
            { title: 'Manage Agriculture Types', action: 'doManageAgricultureTypes'},

            { title: 'Visualize', keyEquivalent: 'ctrl_v', action: 'doVisualize'}
            //{ title: 'Export Selected', keyEquivalent: 'ctrl_e', action: 'doExportRecord', isEnabled:NO},
            //{ title: 'Remove Selected', keyEquivalent: ['ctrl_delete', 'ctrl_backspace'], action: 'doRemove', isEnabled:NO},
        ]
    }),

    overlayView: Footprint.OverlayView.extend({
        layout: { top: 24 },
        contentBinding: SC.Binding.oneWay('Footprint.builtFormCategoriesTreeController'),
        statusBinding:SC.Binding.oneWay('*content.status')
    }),

    listView: SC.ScrollView.extend({
        layout: { top: 24 },
        media: null,
        // TODO this doesn't make sense

        contentView: SC.SourceListView.extend({
            isEnabledBinding: SC.Binding.oneWay('.content').bool(),
            rowHeight: 20,
            actOnSelect: NO,
            // Dummy value. We just need to tell the view that we have an icon so it calls our renderIcon
            contentIconKey: 'medium',

            contentBinding: SC.Binding.oneWay('Footprint.builtFormCategoriesTreeController.arrangedObjects'),
            contentValueKey: 'name',

            selectionBinding: SC.Binding.from('Footprint.builtFormCategoriesTreeController.selection'),
            
            groupExampleView: SC.View.extend(SC.ContentDisplay, {
                contentDisplayProperties: ['name'],
                render: function(context) {
                    context = context.begin()
                           .addClass(['sc-view', 'footprint-built-form-group-view'])
                           .addClass(this.getPath('theme.classNames'));
                    context.begin()
                           .addClass(['sc-view', 'footprint-built-form-group-label-view'])
                           .addClass(this.getPath('theme.classNames'))
                           .push(this.getPath('content.name'))
                           .end();
                    context = context.end();
                },
                update: function($context) {
                    $context.find('.footprint-built-form-group-label-view').text(this.getPath('content.name'));
                }
            }),
            exampleView: SC.View.extend(SC.Control, SC.ContentDisplay, {
                classNames: ['footprint-built-form-item'],
                contentDisplayProperties: ['name'],

                mediumContent: null,
                mediumContentBinding: SC.Binding.oneWay('*content.medium.content'),
                displayProperties: ['mediumContent'],

                render: function(context) {
                    // Color swab
                    var color = this.getPath('content.medium.content.fill.color') || '';
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
                    $context.find('.footprint-medium-color').css('background-color', this.getPath('content.medium.content.fill.color') || '');
                    $context.find('.footprint-built-form-item-label-view').text(this.getPath('content.name'));
                }
            })
        })
    })
});
