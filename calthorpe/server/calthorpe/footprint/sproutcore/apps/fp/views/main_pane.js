sc_require('views/sections/top_half_view');
sc_require('views/sections/bottom_half_view');
sc_require('views/sections/project_section_view');
sc_require('views/sections/right_logo_section_view');
sc_require('views/sections/left_logo_section_view');
sc_require('views/user/account_view')

Footprint.MainPane = SC.MainPane.extend({
    childViews: 'projectSectionView leftlogoView rightlogoView accountView splitView'.w(),

    projectSectionView: Footprint.ProjectSectionView.extend({
        layout: { height: 24, left: 0.35, right: 0.35 }
    }),

    leftlogoView: Footprint.LeftLogoSectionView.extend({
        layout: { height: 24, left: 0, width: 0.35 }
    }),

    rightlogoView: Footprint.RightLogoSectionView.extend({
        layout: { height: 24, right:.05, width: 0.35 }
    }),

    accountView: Footprint.AccountView.extend({
        layout: { height: 24, right: 0, width: 0.05 }
    }),

    splitView: SC.SplitView.extend({
        layout: { top: 25 },
        defaultThickness: 0.3,
        layoutDirection: SC.LAYOUT_VERTICAL,
        topLeftView: Footprint.TopHalfView,
        bottomRightView: Footprint.BottomHalfView
    })

});