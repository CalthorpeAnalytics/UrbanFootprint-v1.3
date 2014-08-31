
 /* 
* UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
* 
* Copyright (C) 2014 Calthorpe Associates
* 
* This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
* 
* This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
* 
* You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
* 
* Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
*/

Footprint.TitleView = SC.ToolbarView.extend({
     classNames: "footprint-title-view".w(),
     childViews:'labelView'.w(),
     anchorLocation: SC.ANCHOR_TOP,
     labelViewLayout: {left:0, right:0},

     title:null,
     content:null,
     contentNameProperty:null,

     labelView: SC.LabelView.extend({
         layoutBinding:SC.Binding.oneWay('.parentView.labelViewLayout'),
         content:null,
         contentBinding:SC.Binding.oneWay('.parentView.content'),

         contentStatus:null,
         contentStatusBinding:SC.Binding.oneWay('*content.status'),
         contentNameProperty:'name',
         contentNamePropertyBinding:SC.Binding.oneWay('.parentView.contentNameProperty').transform(function(name) {
            return name || 'name';
         }),

         title:null,
         titleBinding:SC.Binding.oneWay('.parentView.title'),

         fullLabel:function() {
             if (this.get('contentStatus') & SC.Record.READY) {
                 var subtitle = this.getPath('content.%@'.fmt(this.get('contentNameProperty')));
                 if (subtitle)
                     return '%@ for %@'.fmt(this.get('title'), subtitle);
             }
             return 'Loading';
         }.property('content', 'contentStatus', 'title', 'contentNameProperty').cacheable(),
         value: null,
         valueBinding: SC.Binding.oneWay('.fullLabel')
     })
 });
