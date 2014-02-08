
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

Footprint.LoadingScenarioDependencyState = Footprint.LoadingState.extend({

    loadingStatusValue:1,

    enterState: function() {
        sc_super()
    },

    parameters: {},
    eventKey:null,
    recordArray:function() {
        return Footprint.store.find(SC.Query.create({
            recordType: this.get('recordType'),
            location: SC.Query.REMOTE,
            parameters:this.get('parameters')
        }));
    },
    didLoadEvent:function() {
        return '%@IsReady'.fmt(this.get('eventKey'));
    }.property('loadingController', 'eventKey').cacheable(),


    didFailEvent: function() {
        return '%@DidFail'.fmt(this.get('eventKey'));
    }.property('loadingController', 'eventKey').cacheable()
});

Footprint.LoadingScenarioCategoriesState = Footprint.LoadingScenarioDependencyState.extend({
    recordType:Footprint.Category,
    parameters: {
        key: 'category'
    },
    loadingController: Footprint.scenarioCategoriesController,
    eventKey:'scenarioCategoriesController'
});

Footprint.LoadingBuiltFormTagsState = Footprint.LoadingScenarioDependencyState.extend({
    recordType:Footprint.Tag,
    loadingController: Footprint.builtFormTagsController,
    eventKey:'builtFormTagsController'
});
Footprint.LoadingLayerTagsState = Footprint.LoadingScenarioDependencyState.extend({
    recordType:Footprint.Tag,
    loadingController: Footprint.layerTagsController,
    eventKey:'layerTagsController'
});

Footprint.LoadingPresentationsState = Footprint.LoadingScenarioDependencyState.extend({
    recordType:Footprint.Presentation,
    // Use a private controller to load presentations. The public controllers split them between LayerLibrary
    // and ResultLibrary presentations
    loadingController: SC.ArrayController.create(),
    eventKey:'presentationsController'
});

Footprint.LoadingBuiltFormSetsState = Footprint.LoadingScenarioDependencyState.extend({
    recordType:Footprint.BuiltFormSet,
    loadingController: Footprint.builtFormSetsController,
    eventKey:'builtFormSetsController'
});

Footprint.LoadingPolicySetsState = Footprint.LoadingScenarioDependencyState.extend({
    recordType:Footprint.PolicySet,
    loadingController: Footprint.policySetsController,
    eventKey:'builtFormSetsController'
});
