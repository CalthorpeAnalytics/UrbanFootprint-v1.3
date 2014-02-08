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

/***
 * Controls the use of map tools by enabling or disabling them depending on the application state
 * @type {*
*/
Footprint.toolController = SC.Object.create({
    /***
     * Controls if navigation tools are enabled
     */
    navigatorIsEnabled: YES,
    /***
     * Controls if selection tools are enabled
     */
    selectorIsEnabled: NO,
    /***
     * Controls if feature edit/info tools are enabled
     */
    featurerIsEnabled: NO,

    /***
     * Set true whenever the selector needs refresh, which clears the box or other shape it makes
     */
    selectionToolNeedsReset: NO
});

Footprint.paintingController = SC.Object.create({
    developmentPercent: 1,
    densityPercent: 1,
    isFullRedevelopment: NO
});
