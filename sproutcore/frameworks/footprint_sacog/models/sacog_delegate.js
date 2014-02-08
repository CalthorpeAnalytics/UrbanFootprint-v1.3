/**
 *
 * Created by calthorpe on 11/4/13.
 */

sc_require('models/sacog_existing_land_use_parcel_feature_model');
sc_require('models/sacog_hardwood_feature_model');
sc_require('models/sacog_stream_feature_model');
sc_require('models/sacog_vernal_pool_feature_model');
sc_require('models/sacog_wetland_feature_model');

FootprintSacog.SacogDelegate = Footprint.DefaultDelegate.extend({
    dbEntityKeyToFeatureRecordType: function() {
        return SC.Object.create({
            sacog_existing_land_use_parcels: FootprintSacog.SacogExistingLandUseParcelFeature,
            streams: FootprintSacog.SacogStreamFeature,
            wetlands: FootprintSacog.SacogWetlandFeature,
            vernal_pools: FootprintSacog.SacogVernalPoolFeature,
            hardwoods: FootprintSacog.SacogHardwoodFeature,
            light_rail:FootprintSacog.SacogLightRailFeature,
            light_rail_stops:FootprintSacog.SacogLightRailStopsFeature,
            light_rail_stops_one_mile:FootprintSacog.SacogLightRailStopsOneMileFeature,
            light_rail_stops_half_mile:FootprintSacog.SacogLightRailStopsHalfMileFeature,
            light_rail_stops_quarter_mile: FootprintSacog.SacogLightRailStopsQuarterMileFeature
        }, sc_super())
    }.property('parentDelegate').cacheable(),

    loadingRegionStateClass: function() {
        return SC.objectForPropertyPath('FootprintSacog.LoadingRegionSacogState')
    }.property().cacheable()
});
