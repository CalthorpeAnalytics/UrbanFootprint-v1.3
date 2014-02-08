
sc_require('resources/donutChartMaker');
sc_require('resources/builtFormVisUtils');
sc_require('views/info_views/vis_pane_views/examples_view');
sc_require('views/info_views/vis_pane_views/development_chars_view');
sc_require('views/info_views/vis_pane_views/donut_charts_view');
sc_require('views/info_views/vis_pane_views/bar_chart_view');
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

 Footprint.VisualizePane = SC.PanelPane.extend(SC.ActionSupport, {
//     modalPane: SC.ModalPane.extend({
//         classNames: ['footprint-background-pane']
//     }),

     contentView: SC.View.extend({

         layout: { height:630, width:1300, centerX: 0, centerY: 0 },
         classNames:['footprint-visualize-palette-pane'],
         content:null,
         isModal: NO,
         contentBinding: SC.Binding.oneWay('Footprint.builtFormActiveController.content'),
         childViews:'mainView listView'.w(),

         mainView: SC.View.extend({
             layout: { left:.20 },
             classNames:['footprint-visualize-pane-content'],
             childViews:'headerView descriptionView examplesView barChartView donutChartsView rightOfBarChartView developmentCharsView footerView'.w(),
             content: null,
             contentBinding: SC.Binding.oneWay('.parentView.content'),
             /***
              * Closes the view, discarding edited values that haven't been saved.
              */
             color: null,
             colorBinding: SC.Binding.oneWay('*content.medium').transform(function(medium) {
                 if (medium) {
                     return medium.getPath('content.fill.color');
                 }
             }),


             headerView: SC.LabelView.extend({
                 classNames: ['footprint-visualize-pane-header'],
                 layout: { left: 0, right: 0, top: 0, height: 0.07 },
                 displayProperties: ['content', 'color'],

                 valueBinding: SC.Binding.oneWay('.parentView*content.name'),

                 color: null,
                 colorBinding: SC.Binding.oneWay('.parentView.color'),

                 backgroundColor:null,
                 backgroundColorBinding: SC.Binding.oneWay('.parentView.color'),

                 classNameBindings: ['hasLightBackground'],

                 hasLightBackground: function(){

                     if (this.get('color')) {
                         return isLightColor(this.get('color'));
                     }

                 }.property('color').cacheable(),

                 render: function(context) {
                     sc_super();
                 }

             }),
             descriptionView: SC.View.design({
                 layout: { top: 0.06, left: 0, right:.65, bottom: 0.75},
                 classNames: ['descriptionBlock'],
                 displayProperties: ['content'],

                 content: null,
                 contentBinding: SC.Binding.oneWay('.parentView.content'),
                 didCreateLayer: function() {
                     this.addObserver('content', this, 'updateDescription');
                 },
                 updateDescription: function() {
                     if (this.get('content')) {
                         createDescription(this.get("content"));
                     }
                 }

             }),
             rightOfBarChartView: SC.View.design({
                 layout: { top: 0.06, left: 0.95, bottom: 0.75},
                 classNames: ['rightOfBarChart']
                // this is a hack to get the rounded edge below the header

             }),
             barChartView: Footprint.BarChartView.design({

             }),
             donutChartsView: Footprint.DonutChartsView.design({

             }),
             examplesView: Footprint.ExamplesView.design({

             }),
             developmentCharsView: Footprint.DevelopmentCharsView.design({

             }),
             footerView: SC.View.extend({

                 childViews: 'cancelButtonView'.w(),
                 classNames: ['footprint-visualize-pane-footer'],
                 layout: { left: 0, right: 0, top: 0.95 },
                 displayProperties: ['content', 'color'],

                 color: null,
                 colorBinding: SC.Binding.oneWay('.parentView.color'),


                 render: function(context) {
                     sc_super();
                     var color = this.get('color');
                     context.addStyle("background-color", color);
                 },

                 cancelButtonView: SC.ButtonView.design({
                     layout: {bottom: 5, right: 20, height:24, width:80},
                     title: 'Close',
                     action: 'doClose',
                     isCancel: YES
                 })

             })
         }),
         listView: SC.ScrollView.extend({
             layout: { right:.80},
             media: null,
             // TODO this doesn't make sense
             loadMedia: function () {
                 this.set('media', Footprint.store.find(SC.Query.local(
                     Footprint.Medium, {
                         orderBy: 'key' })));
             }.observes('Footprint.scenarioActiveController.content'),


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
         })
     })
 });

