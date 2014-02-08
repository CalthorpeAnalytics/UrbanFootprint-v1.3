sc_require('views/sections/map_section_view');
sc_require('views/sections/sidebar_view');
sc_require('views/sections/policy_section_view');

Footprint.BottomHalfView = SC.View.extend({
    childViews:'sidebarView mapView policiesView'.w(),
    classNames: "footprint-bottom-half-view".w(),

    //---------------------
    // sidebar

    sidebarView: Footprint.SidebarView.extend({
        layout: { left:0, width:0.2, top: 0, bottom: 0 }
    }),

    //---------------------
    // map

    mapView: Footprint.MapSectionView.extend({
        layout: { left:0.2, right:0, top:0, bottom: 0 },
        visible:NO
    }),

    //---------------------
    // Policy Set

    policiesView: Footprint.PolicySectionView.extend({
        layout: { left:.999, right:0, top:0, bottom: 0 },
        visible:NO
    })
});
