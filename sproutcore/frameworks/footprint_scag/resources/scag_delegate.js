/**
 * Created by calthorpe on 11/4/13.
 */

FootprintScag.ScagDelegate = Footprint.DefaultDelegate.extend({
    dbEntityKeyToFeatureRecordType: function() {
        return SC.Object.create({
            existing_land_use_parcels: Footprint.ScagExistingLandUseParcelFeature
        }, sc_super())
    }.property('parentDelegate').cacheable(),

    loadingRegionStateClass: function() {
        return SC.objectForPropertyPath('FootprintScag.LoadingRegionScagState')
    }.property().cacheable()
});