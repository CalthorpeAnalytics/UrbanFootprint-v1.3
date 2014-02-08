/*  * UrbanFootprint-California (v1.0), Land Use Project Development and Modeling System.
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

sc_require('models/config_entity_models');
sc_require('controllers/regions_controllers');
sc_require('controllers/controllers');
sc_require('controllers/selection_controllers');

/*
 * projectsController binds to a flat list of the Projects in the current context
 * @type {*}
 */
Footprint.projectsController = Footprint.ArrayController.create(Footprint.ArrayContentSupport, {
    contentBinding:SC.Binding.oneWay('Footprint.regionActiveController.children')
});

/***
 * projectSelectionController keeps track of the active Project
 * @type {*}
 */
Footprint.projectActiveController = Footprint.ActiveController.create(Footprint.ConfigEntityDelegator, {
    parentConfigEntityDelegator: Footprint.regionActiveController,

    listController:Footprint.projectsController
});

/***
 * A separate controller from the regionActiveController so that a region can be added or edited without necessarily being the region in context for the rest of the application
 * @type {*}
 */
Footprint.projectEditController = SC.ObjectController.create({
    // Used to create new instances
    recordType: Footprint.Project,
    // The bound object controller, which interacts with its content record directly, rather than via a nested store
    objectControllerBinding:SC.Binding.oneWay('Footprint.projectActiveController')
});

/***
 * Configuration of controllers for use by edit views
 * @type {*}
 */
Footprint.projectControllers = Footprint.ControllerConfiguration.create({
    editController:Footprint.projectEditController,
    itemsController:Footprint.projectsController,
    recordSetController:Footprint.projectsController
});
