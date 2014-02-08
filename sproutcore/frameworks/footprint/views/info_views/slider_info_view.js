
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

Footprint.SliderInfoView = SC.View.extend({
    childViews: 'titleView symbolView labelView sliderView'.w(),
    classNames: ['slider-item'],
    valueSymbol: '%',
    title: 'Title',
    minimum: 0,
    maximum: 1,
    step: .01,
    value:null,

    titleView: SC.LabelView.design({
        classNames: ['slider-item-title'],
        layout: { bottom: 0.05, left: 0.1, right:.1, height:.25 },
        localize: true,
        textAlign: SC.ALIGN_CENTER,
        valueBinding: SC.Binding.oneWay('.parentView.title')
    }),

    symbolView: SC.LabelView.design({
        classNames: ['slider-item-symbol-label'],
        layout: { top: 1, left: 0.75, height:0.25 },
        valueBinding: SC.Binding.from('.parentView.valueSymbol')
    }),

    labelView: Footprint.EditableModelStringView.design({
        classNames: ['slider-item-value-label'],
        layout: { right:.3, left:.3, top:0, height: 0.3},
        textAlign: SC.ALIGN_CENTER,
        valueBinding: SC.Binding.from('.parentView.value')
    }),

    sliderView: SC.SliderView.design({
        classNames: ['slider-item-slider'],
        layout: { left:.1, right:.1, top:.2, height: 0.6 },
        minimumBinding: SC.Binding.oneWay('.parentView.minimum'),
        maximumBinding: SC.Binding.oneWay('.parentView.maximum'),
        stepBinding: SC.Binding.oneWay('.parentView.step'),
        valueBinding: SC.Binding.from('.parentView.value')
    })
})