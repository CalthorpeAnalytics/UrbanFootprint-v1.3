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

sc_require('resources/jqueryExtensions');
sc_require('models/presentation_models');
sc_require('controllers/controller_mixins');
sc_require('controllers/scenarios/scenario_controllers');
sc_require('controllers/presentation_controllers');

Footprint.resultLibrariesController = Footprint.PresentationsController.create({
    contentBinding:SC.Binding.oneWay('Footprint.scenarioActiveController*presentations.results')
});

Footprint.resultLibraryActiveController = Footprint.PresentationController.create({
    presentationsBinding:SC.Binding.oneWay('Footprint.resultLibrariesController.content'),
    key: 'result_library__default'
});

/**
 * The results of the active resultLibraryActiveController. Results are subclasses of PresentationMedium instances
 * @type {*}
 */
Footprint.resultsController = Footprint.PresentationMediaController.create({
    presentationBinding: SC.Binding.oneWay('Footprint.resultLibraryActiveController.content')
});

/**
 * This aggregates the public-facing properties of the other controllers
 * The resentationMedium instances for results represent Result instances
 * @type {*|void}
 */
Footprint.resultLibraryContent = Footprint.LibraryContent.create({
    presentationController: Footprint.resultLibraryActiveController,
    presentationMediaController:Footprint.resultsController
});

/***
 *  Aggregates the public-facing properties of the other controllers
 * @type {*|void}
 */
Footprint.resultLibraryController = SC.ObjectController.create({
    // Binding content makes all other properties accessible via delegation
    contentBinding: SC.Binding.oneWay('Footprint.resultLibraryContent')
});

/***
 * Binds to the currently selected Result
 * @type {*}
 */
Footprint.resultActiveController = Footprint.PresentationMediumActiveController.create({
    listController: Footprint.resultsController
});

/***
 * Edits the active Result, a clone of the active Result, or a brand new Result
 * @type {*|void}
 */
Footprint.resultEditController = Footprint.PresentationMediumEditController.create({
    objectControllerBinding:'Footprint.resultActiveController'
});

Footprint.resultControllers = Footprint.ControllerConfiguration.create({
    editController:Footprint.resultEditController,
    itemsController:Footprint.resultsController,
    recordSetController:Footprint.resultLibraryController
});
