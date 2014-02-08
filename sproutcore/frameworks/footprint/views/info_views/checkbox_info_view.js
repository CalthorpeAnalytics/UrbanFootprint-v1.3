
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

Footprint.CheckboxInfoView = SC.View.extend({
    childViews: 'checkboxView titleView'.w(),
    title: 'Title',
    value:null,
    titleLayout: { bottom:.0, height:.4},
    buttonLayout: { top:.02, left:.35, width:.32, height:.4 },

    titleView: SC.LabelView.design({
        classNames: ['footprint-checkbox-item-title'],
        layoutBinding: SC.Binding.oneWay('.parentView.titleLayout'),
        textAlign: SC.ALIGN_CENTER,
        valueBinding: SC.Binding.oneWay('.parentView.title')
    }),
    checkboxView: SC.CheckboxView.design({
        classNames: ['footprint-checkbox-item-checkbox'],
        layoutBinding: SC.Binding.oneWay('.parentView.buttonLayout'),
        valueBinding: SC.Binding.from('.parentView.value')
    })
})