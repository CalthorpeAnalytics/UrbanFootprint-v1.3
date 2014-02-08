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

// FeatureControllers are always in the scope of the active ConfigEntity. They don't load all feature instances of a class but simply pull down those that make up a selection. Therefore the Datasource always expects an id list in the query to limit them

sc_require('controllers/layer_controllers');
sc_require('controllers/property_controllers');

/***
 * Controls the active features of the configEntity that are selected based on the LayerSelection
 * @type {*|void}
 */
Footprint.featuresActiveController = Footprint.ArrayController.create({
    recordTypeBinding: SC.Binding.oneWay('.activeRecordType'),

    layer:null,
    layerBinding:SC.Binding.oneWay('Footprint.layerSelectionActiveController.layer'),

    /***
     * The Feature subclass of the active features, e.g. BaseFeature
     */
    activeRecordType: function() {
        return this.get('layer') && this.getPath('layer.status') & SC.Record.READY && this.get('layer').featureRecordType();
    }.property('layer').cacheable(),

    /***
     * Lookup the of Footprint.Feature subclass by db_entity_key
    */
    dbEntityKeyToFeatureRecordType: function () {
        return SC.Object.create({
            base_feature: Footprint.BaseFeature,
            base_parcel_feature: Footprint.BaseParcelFeature,
            cpad_holdings: Footprint.CpadHoldingsFeature,
            developable: Footprint.DevelopableFeature,
            increment: Footprint.IncrementFeature,
            end_state: Footprint.EndStateFeature,
            future_scenario_feature: Footprint.FutureScenarioFeature,
            census_tract: Footprint.CensusTract,
            census_blockgroup: Footprint.CensusBlockgroup,
            census_block: Footprint.CensusBlock,
    //                // TODO SACOG/SCAG specific layer. This logic needs to be separated out
    //                existing_land_use_parcels:
    //                    var className = 'Footprint.%@ExistingLandUseParcelFeature'.fmt(Footprint.regionActiveController.get('key').classify());
    //                    var cls = SC.objectForPropertyPath(className);
    //                    if (!cls)
    //                        throw "ExistingLandUseParcelFeature subclass not found";
    //                    cls;
    //                scag pilot 'Irvine' specific features
            existing_land_use_parcels: Footprint.ScagExistingLandUseParcelFeature,
            general_plan_parcels: Footprint.ScagGeneralPlanParcelsFeature,
            primary_spz: Footprint.ScagPrimarySpzFeature,
            jurisdiction_boundary: Footprint.ScagJurisdictionBoundary,
            sphere_of_influence: Footprint.ScagSphereOfInfluence,
            tier1_taz: Footprint.ScagTier1Taz,
            tier2_taz: Footprint.ScagTier2Taz,
            transit_areas: Footprint.ScagTransitAreas,
            parks_open_space: Footprint.ScagParksOpenSpace,
            floodplain: Footprint.ScagFloodplain,

            //sacog specfic features
            streams: Footprint.SacogStreamFeature,
            wetlands: Footprint.SacogWetlandFeature,
            vernal_pools: Footprint.SacogVernalPoolFeature,

            //sandag specfic features
            scenario_c_boundary: Footprint.SandagScenarioCBoundaryFeature,
            scenario_b_boundary: Footprint.SandagScenarioBBoundaryFeature,
            '2050_rtp_transit_network': Footprint.Sandag2050RtpTransitNetworkFeature,
            '2050_rtp_transit_stops': Footprint.Sandag2050RtpTransitStopFeature
        });
    }.property().cacheable()

});

Footprint.featuresActivePropertiesController = Footprint.PropertiesController.create({
    allowsMultipleSelection:NO,
    recordTypeBinding: SC.Binding.oneWay('Footprint.featuresActiveController.activeRecordType')
});
Footprint.featuresActiveDbEntityKeysController = SC.ArrayController.create(SC.SelectionSupport, {
    allowsMultipleSelection:NO,
    layerLibrary:null,
    layerLibraryBinding: SC.Binding.oneWay('Footprint.layerLibraryActiveController.content'),
    contentBinding:SC.Binding.oneWay('.layerLibrary').transform(function(value) {
        return value && value.getPath('presentation_media').mapProperty('db_entity_key');
    })
});
