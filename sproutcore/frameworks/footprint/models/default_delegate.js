/**
 *
 * Created by calthorpe on 11/4/13.
 */

Footprint.DefaultDelegate = SC.Object.extend({
    dbEntityKeyToFeatureRecordType: function() {
        return SC.Object.create({
            base_feature: Footprint.BaseFeature,
            cpad_holdings: Footprint.CpadHoldingsFeature,
            developable: Footprint.DevelopableFeature,
            increments: Footprint.IncrementsFeature,
            end_state: Footprint.EndStateFeature,
            base_demographic_feature: Footprint.BaseDemographicFeature,
            base_agriculture_feature: Footprint.BaseAgricultureFeature,
            future_agriculture_feature: Footprint.FutureAgricultureFeature,
            end_state_demographic_feature: Footprint.EndStateDemographicFeature,
            future_scenario_feature: Footprint.FutureScenarioFeature,
            census_tract: Footprint.CensusTract,
            census_blockgroup: Footprint.CensusBlockgroup,
            census_block: Footprint.CensusBlock,
            vmt_feature: Footprint.VmtFeature
        });
    }.property().cacheable(),

    loadingRegionStateClass: function() {
        return null;
    }.property().cacheable()
});
