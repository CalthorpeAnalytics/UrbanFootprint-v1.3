/**
 * Created by calthorpe on 11/4/13.
 */
sc_require('resources/scag_delegate');

FootprintScag.ScagIrvineDelegate = FootprintScag.ScagDelegate.extend({
    parentDelegate: Footprint.ScagDelegate,
    dbEntityToFeatureRecordType: function() {
        return SC.Object.create({
            general_plan_parcels: Footprint.ScagGeneralPlanParcelFeature,
            base_parcel_feature: Footprint.BaseParcelFeature,
            primary_spz: Footprint.ScagPrimarySpzFeature,
            jurisdiction_boundary: Footprint.ScagJurisdictionBoundary,
            sphere_of_influence: Footprint.ScagSphereOfInfluence,
            tier1_taz: Footprint.ScagTier1Taz,
            tier2_taz: Footprint.ScagTier2Taz,
            transit_areas: Footprint.ScagTransitAreas,
            parks_open_space: Footprint.ScagParksOpenSpace,
            floodplain: Footprint.ScagFloodplain
        }, sc_super());
    }.property('parentDelegate').cacheable()
});