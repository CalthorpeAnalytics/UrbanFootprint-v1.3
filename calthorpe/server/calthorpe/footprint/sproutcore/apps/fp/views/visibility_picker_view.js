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

/***
 * Displays a visible, invisible, and solo button as a segmented view. Exactly one value can be set at.
 */
Footprint.VisibilityPickerView = SC.SegmentedView.design({
    content:null,
    allowsMultipleSelection:NO,
    // Don't present the more... button
    shouldHandleOverflow:NO,
    // In addition to sending the action, also call set('value')
    //selectSegmentWhenTriggeringAction:YES,

    items: [
//        SC.Object.create({
//            value: Footprint.SOLO,
//            title: 's',
//            //icon:static_url('images/solo.png'),
//            width:'.4',
//            action:'soloAction',
//        }),
        SC.Object.create({
            value: Footprint.VISIBLE,
            direction:SC.LAYOUT_VERTICAL,
            theme: SC.ButtonView,
            size: SC.AUTO_CONTROL_SIZE,
//            title: 'v',
//            icon:static_url('/images/1371432545_eye_inv.png'),
           // width:'.4',
            action:'visibleAction',

        })
    ],
    toggle: function() {
        logProperty('v','v', 'toggle')
    },

    // A property that must take 'visible', 'solo', or 'hidden' as possible values. 'hidden' can be anything since it instructs the SegmentedView to not select either button
//    itemTitleKey: 'title',
    itemValueKey: 'value',
    height: 'size',
    theme: 'theme',
//    itemIconKey: 'icon',
    itemActionKey: 'action',
//    itemTargetKey: 'target',
    layoutDirection: 'direction',
    itemWidthKey: 'width',
});
