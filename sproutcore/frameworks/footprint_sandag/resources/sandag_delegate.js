/**
 *
 * Created by calthorpe on 11/4/13.
 */

FootprintSandag.SandagDelegate = Footprint.DefaultDelegate.extend({
    dbEntityKeyToFeatureRecordType: function() {
        return SC.Object.create({
//            scenario_c_boundary: Footprint.SandagScenarioCBoundaryFeature,
//            scenario_b_boundary: Footprint.SandagScenarioBBoundaryFeature,
            '2050_rtp_transit_network': Footprint.Sandag2050RtpTransitNetworkFeature,
            '2050_rtp_transit_stops': Footprint.Sandag2050RtpTransitStopFeature
        }, sc_super())
    }.property('parentDelegate').cacheable()
});
