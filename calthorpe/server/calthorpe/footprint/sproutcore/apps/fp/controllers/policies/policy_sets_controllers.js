
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

sc_require('controllers/controllers');
sc_require('controllers/selection_controllers');
sc_require('controllers/sets_controllers');

Footprint.policySetsController = Footprint.SetsController.create({
    listControllerBinding: SC.Binding.oneWay('Footprint.scenariosController'),
    property:'policy_sets'
});

/***
 * The active policy, as dictated by the user's selection
 * @type {*}
 */
Footprint.policySetActiveController = Footprint.ActiveController.create({
    listController:Footprint.policySetsController
});


Footprint.policySetEditController = SC.ObjectController.create({
    // Used to create new instances
    recordType: Footprint.Policy,
    // The bound object controller, which interacts with its content record directly, rather than via a nested store
    objectControllerBinding:'Footprint.policySetActiveController',

    // Coerce single tag selection into the built_forms's tags collection
    // TODO the view control should support multiple selection
    tag: function(propKey, value) {
        if (value !== undefined) {
            this.get('tags').removeObjects(this.get('tags'));
            this.get('tags').pushObject(value);
        }
        else
            return this.get('tags').objectAt(0);
    }.property('*content.tags')
});

Footprint.policySetControllers = Footprint.ControllerConfiguration.create({
    editController:Footprint.policySetEditController,
    itemsController:Footprint.policySetsController,
    recordSetController:Footprint.policySetsController
});
