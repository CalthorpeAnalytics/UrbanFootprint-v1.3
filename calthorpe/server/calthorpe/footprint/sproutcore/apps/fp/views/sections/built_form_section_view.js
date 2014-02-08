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

sc_require('views/section_titlebars/edit_button_view');
sc_require('views/section_titlebars/built_form_toolbar_view');

Footprint.BuiltFormSectionView = SC.View.extend({
    childViews: 'toolbarView listView copyrightView'.w(),
    classNames: "footprint-built-form-section-view".w(),

    //isEnabled: SC.Binding.oneWay('Footprint.builtFormCategoriesTreeController').matchesStatus(SC.Record.READY_CLEAN),

    toolbarView: Footprint.BuiltFormToolbarView.extend({
    }),

    copyrightView: SC.View.extend({
        childViews: 'copyrightimageView copyrightlabelView'.w(),
        classNames: "footprint-copyright-view",
        layout: {height: 35, bottom: 0},
        copyrightimageView: SC.ImageView.extend({
            value: function () {
                var image_path = 'images/default_logos/uf_thumbnail_35.png';
                return Footprint.STATIC.fmt(image_path);
            }.property().cacheable(),
            layout: { height: 35, left: 0, width: 35 }
        }),

        copyrightlabelView: SC.LabelView.create({
            classNames: "footprint-copyright-label-view",
            value: 'UrbanFootprint rev. 20130925 \n © 2013 Calthorpe Associates',
            layout: {top: 0.05, left: 40}
        })
    }),

    listView: SC.ScrollView.extend({
        layout: { top: 24, bottom: 35 },
        media: null,
        // TODO this doesn't make sense


        contentView: SC.SourceListView.extend({
            isEnabledBindng: SC.Binding.oneWay('content').bool(),
            rowHeight: 20,
            isEditable: YES,
            actOnSelect: NO,
            canEditContent: YES,
            canDeleteContent: YES,
            canReorderContent: YES,
            // Dummy value. We just need to tell the view that we have an icon so it calls our renderIcon
            contentIconKey: 'medium',

            contentBinding: SC.Binding.oneWay('Footprint.builtFormCategoriesTreeController.arrangedObjects'),
            contentValueKey: 'name',

            selectionBinding: SC.Binding.from('Footprint.builtFormCategoriesTreeController.selection'),
            exampleView: SC.View.extend(SC.Control, {
                layout: { height: 24 },
                classNames: ['sc-list-item-view', 'footprint-built-form-item'],
                displayProperties: 'content color'.w(),
                childViews: 'labelView'.w(),

                contentValueKey: 'name',
                actOnSelect: YES,
                canEditContent: YES,
                canDeleteContent: YES,
                canReorderContent: YES,

                color: null,
                colorBinding: SC.Binding.oneWay('*content.medium.content.fill.color'),

//                click: function(evt) {
//                    Footprint.statechart.sendAction('doViewBuiltForm', SC.Object.create({content : Footprint.builtFormCategoriesTreeController.getPath('selection.firstObject')}));
//                },

                render: function (context) {
                    sc_super();
                    if (this.get('content').kindOf(Footprint.TreeItem))
                        return;

                    // get a class name and url to include if relevant
                    var url = null,
                        className = null,
                        classArray = [];
                    if (this.get('icon') && SC.ImageView.valueIsUrl(this.get('icon'))) {
                        className = '';
                        url = icon;
                    } else {
                        className = 'footprint-medium-color';
                        url = SC.BLANK_IMAGE_URL;
                    }

                    // I don't know how to add the default theme and app classes automagically
                    // generate the img element...
                    classArray.push('ace', 'footprint', className);
                    var color = this.get('color')
                    // The left swab swab
                    context.begin('span')
                        .addClass(classArray)
                        .attr('style', 'width:20px; background-color:%@'.fmt(color))
                        .end();
                    // TODO do background-image instead
                    //context.begin('img')
                    //   .addClass(classArray)
                    //    .attr('src', url)
                    //    .end();
                },
                update: function ($context) {
                    $context.find('span').css('background-color', this.get('color'));
                    // TODO handle image too
                },
                labelView: SC.LabelView.extend({
                    layout: { left: 25 },
                    valueBinding: SC.Binding.oneWay('.parentView*content.name')
                })
            })
        })
    }),
    render: function (context, firstTime) {
        sc_super();
    }
});
