
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

Footprint.CheckboxItemView = SC.View.extend({
    childViews: 'checkboxView titleView'.w(),
    title: 'Title',
    value:null,

    titleView: SC.LabelView.design({
        classNames: ['checkbox-item-title'],
        layout: { top:.0, height:.4 },
        valueBinding: SC.Binding.oneWay('.parentView.title')
    }),
    checkboxView: SC.CheckboxView.design({
        classNames: ['checkbox-item-checkbox'],
        layout: { top:.4, left:.4, width:.25 },
        valueBinding: SC.Binding.from('.parentView.value')
    })
})