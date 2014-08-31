sc_require('views/sections/scenario_section_view');
sc_require('views/sections/result_section_view');
sc_require('views/sections/map_section_view');
sc_require('views/sections/analysis_module_section_view');
sc_require('views/sections/layer_section_view');
sc_require('views/sections/visible_layer_section_view');

Footprint.MainPane = SC.MainPane.extend({
    childViews: ['headerBarView', 'bodyView'],

    headerBarView: SC.View.extend({
        layout: { height: 35 },
        classNames: ['footprint-project-section-view', 'toolbar'],
        childViews: ['projectView', 'clientView', 'logoutButtonView'],
        projectView: SC.View.extend({
            layout: { width: 285 },

            contentBinding: SC.Binding.oneWay('Footprint.projectsController.content'),
            selectionBinding: 'Footprint.projectsController.selection',

            childViews: ['projectLogoView', 'projectSelectView', 'projectMenuView'],

            projectLogoView: SC.ImageView.extend({
                layout: { left: 5, height: 24, width: 24, centerY: 0 },
                clientBinding: SC.Binding.oneWay('Footprint.regionActiveController.client'),
                projectKeyBinding: SC.Binding.oneWay("Footprint.projectActiveController.key"),
                value: function () {
                    var client = this.get('client'),
                        projectKey = this.get('projectKey');
                    if (client && projectKey) {
                        var image_path = 'images/%@_logo.png'.fmt(projectKey);
                        return client.STATIC.fmt(image_path);
                    }
                }.property('client', 'projectKey').cacheable()
            }),
            projectSelectView: Footprint.LabelSelectView.extend({
                layout: { left: 35, right: 40, height: 22, centerY: 0, border: 1 },
                contentBinding: SC.Binding.oneWay('.parentView.content'),
                selection: null,
                selectionBinding: '.parentView.selection',
                selectedItemBinding: '*selection.firstObject',
                itemTitleKey: 'name'
            }),
            projectMenuView: Footprint.EditButtonView.extend({
                layout: { right: 6, width: 26, height: 22, centerY: 0, border: 1 },

                icon: sc_static('images/section_toolbars/pulldown.png'),

                contentBinding: SC.Binding.oneWay('Footprint.scenarioActiveController.content'),

                // TODO: Hook these back up for use in the statecharts.
                recordType: Footprint.Scenario,
                activeRecordBinding: SC.Binding.oneWay('Footprint.scenarioActiveController.content'),
                menuItems: [
                    SC.Object.create({ title: 'Manage Projects', keyEquivalent: 'c', action: 'doManageProjects', isEnabled:NO }),
                    SC.Object.create({ isSeparator: YES }),
                    SC.Object.create({ title: 'Manage Scenarios', keyEquivalent: 'ctrl_i', action: 'doManageScenarios' }),
                    SC.Object.create({ title: 'Export Scenario', keyEquivalent: 'ctrl_e', action: 'doExportRecord', isEnabled:NO }),
                    SC.Object.create({ title: 'Remove Scenario', keyEquivalent: ['ctrl_delete', 'ctrl_backspace'], action: 'doRemoveRecord', isEnabled:NO })
                ]
            })
        }),
        clientView: SC.View.extend({
            layout: { left: 280, right: 80 },
            childViews: ['titleView', 'clientLogoView'],
            titleView: SC.LabelView.create({
                layout: { right: 145, height: 24, centerY: 0 },
                classNames: "footprint-right-logo-title-view",
                valueBinding: SC.Binding.oneWay("Footprint.regionActiveController.name").transform(function(name) {
                    if (name)
                        return "%@ UrbanFootprint Scenario Planning Model".fmt(name);
                })
            }),
            clientLogoView: SC.ImageView.extend({
                layout: { width: 145, right: 0, height: 33, centerY: 0 },
                scale: SC.BEST_FIT,
                valueBinding: SC.Binding.oneWay('Footprint.regionActiveController*client.logoPath')
            })
        }),
        logoutButtonView: SC.ButtonView.extend({
            layout: { width: 70, right: 5, height: 22, centerY: 0, border: 1 },
            classNames: ['theme-button', 'theme-button-gray'],
            title: 'Logout',
            action: 'doLogout'
        })
    }),

    bodyView: SC.SplitView.extend({
        layout: { top: 35 },
        layoutDirection: SC.LAYOUT_VERTICAL,
        childViews: ['topView', 'bottomView'],
        topView: SC.SplitView.extend(SC.SplitChild, {
            size: 200,
            sizeOffset:-2,
            canCollapse:YES,
            layoutDirection: SC.LAYOUT_HORIZONTAL,

            childViews: ['scenarioSectionView', 'resultSectionView'],
            scenarioSectionView: Footprint.ScenarioSectionView.extend(SC.SplitChild, {
                size: 470,
                sizeOffset:-2,
                canCollapse:YES
            }),
            resultSectionView: Footprint.ResultSectionView.extend(SC.SplitChild, {
                autoResizeStyle: SC.RESIZE_AUTOMATIC,
                positionOffset:2,
                sizeOffset:-2,
                canCollapse:YES
            })
        }),
        bottomView: SC.SplitView.extend(SC.SplitChild, {
            autoResizeStyle: SC.RESIZE_AUTOMATIC,
            positionOffset:2,
            sizeOffset:-2,
            canCollapse:YES,

            childViews: ['sidebarView', 'centerView'],
            sidebarView: SC.View.extend(SC.SplitChild, {
                classNames: "footprint-sidebar-view".w(),
                size: 350,
                sizeOffset:-2,
                canCollapse:YES,
                childViews: ['sidebarViewItself', 'copyrightView'],
                sidebarViewItself: SC.SplitView.extend({
                    layout: { bottom: 35 },

                    childViews:['layerSectionView'],
                    layoutDirection: SC.LAYOUT_VERTICAL,

                    layerSectionView: Footprint.LayerSectionView.extend(SC.SplitChild, {
                        size: 150,
                        autoResizeStyle: SC.RESIZE_AUTOMATIC,
                        sizeOffset:-2,
                        canCollapse:YES
                    })
                }),
                copyrightView: SC.View.extend({
                    layout: { height: 35, bottom: 0 },
                    childViews: 'copyrightImageView copyrightLabelView'.w(),
                    classNames: "footprint-copyright-view",
                    copyrightImageView: SC.ImageView.extend({
                        layout: { height: 35, left: 0, width: 35 },
                        value: sc_static('images/default_logos/uf_thumbnail_35.png')
                    }),
                    copyrightLabelView: SC.LabelView.create({
                        classNames: "footprint-copyright-label-view",
                        value: 'UrbanFootprint rev. 2014.4.7 \n © 2014 Calthorpe Associates',
                        layout: {top: 0.05, left: 40}
                    })
                })
            }),
            centerView:SC.View.extend(SC.SplitChild, {
                autoResizeStyle: SC.RESIZE_AUTOMATIC,
                sizeOffset:-2,
                positionOffset:2,
                canCollapse:NO,

                childViews: ['mapView', 'layersMenuView', 'modulesView', 'modulesButtonView'],
                mapView: Footprint.MapSectionView,
                layersMenuView: Footprint.VisibleLayerSectionView.extend({
                    layout: { width: 250, borderRight: 1 },
                    isVisible: NO,
                    isVisibleBinding: 'F.layersVisibleController.layersMenuSectionIsVisible',
                    transitionShow: SC.View.SLIDE_IN,
                    transitionShowOptions: { duration: 0.2 },
                    transitionHide: SC.View.SLIDE_OUT,
                    transitionHideOptions: { direction: 'left', duration: 0.2 }
                }),
                modulesView: Footprint.AnalysisModuleSectionView.extend({
                    layout: { width: 275, right: 0, borderLeft: 1, top: 24 },
                    isVisible: NO,
                    isVisibleBinding: 'F.analysisModulesController.analysisModuleSectionIsVisible',
                    transitionShow: SC.View.SLIDE_IN,
                    transitionShowOptions: { direction: 'left', duration: 0.2 },
                    transitionHide: SC.View.SLIDE_OUT,
                    transitionHideOptions: { duration: 0.2 }
                }),
                modulesButtonView: SC.ButtonView.extend({
                    // This button is rotated, making its layout a bit fiddly.
                    layout: { top: 55, right: -30, height: 20, width: 80, rotateZ: -90 },
                    classNames: ['theme-button', 'theme-button-gray', 'theme-button-shorter', 'theme-button-flat-bottom'],
                    valueBinding: 'Footprint.analysisModulesController.analysisModuleSectionIsVisible',
                    icon: function() {
                        if (this.get('value')) return sc_static('fp:images/section_toolbars/pulldown.png');
                        else return sc_static('fp:images/section_toolbars/pullup.png')
                    }.property('value').cacheable(),
                    title: function() {
                        if (this.get('value')) return 'Collapse';
                        else return 'Analysis';
                    }.property('value').cacheable(),
                    buttonBehavior: SC.TOGGLE_BEHAVIOR
                })
            })
        })
    })
});
