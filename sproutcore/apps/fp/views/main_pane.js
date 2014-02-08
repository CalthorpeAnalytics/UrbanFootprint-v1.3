sc_require('views/sections/scenario_section_view');
sc_require('views/sections/result_section_view');
sc_require('views/sections/map_section_view');
sc_require('views/sections/analytic_section_view');
sc_require('views/sections/layer_section_view');
sc_require('views/sections/tool_section_view');
sc_require('views/sections/built_form_section_view');

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

                contentBinding: SC.Binding.oneWay('.parentView.content'),

                // TODO: Hook these back up for use in the statecharts.
                recordType: null,
                activeRecord: null,
                menuItems: [
                    SC.Object.create({ title: 'Get Info', isEnabled:NO}),
                    SC.Object.create({ title: 'Manage Projects', isEnabled:NO})
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
            sizeOffset:-5,
            canCollapse:YES,
            layoutDirection: SC.LAYOUT_HORIZONTAL,

            childViews: ['scenarioSectionView', 'resultSectionView'],
            scenarioSectionView: Footprint.ScenarioSectionView.extend(SC.SplitChild, {
                size: 470,
                sizeOffset:-5,
                canCollapse:YES
            }),
            resultSectionView: Footprint.ResultSectionView.extend(SC.SplitChild, {
                autoResizeStyle: SC.RESIZE_AUTOMATIC,
                positionOffset:5,
                sizeOffset:-5,
                canCollapse:YES
            })
        }),
        bottomView: SC.SplitView.extend(SC.SplitChild, {
            autoResizeStyle: SC.RESIZE_AUTOMATIC,
            positionOffset:5,
            sizeOffset:-5,
            canCollapse:YES,

            childViews: ['sidebarView', 'mapView', 'analyticView'],
            sidebarView: SC.View.extend(SC.SplitChild, {
                classNames: "footprint-sidebar-view".w(),
                size: 350,
                sizeOffset:-5,
                canCollapse:YES,
                childViews: ['sidebarViewItself', 'copyrightView'],
                sidebarViewItself: SC.SplitView.extend({
                    layout: { bottom: 35 },

                    childViews:['layerSectionView', 'toolsetView', 'builtFormsView'],
                    layoutDirection: SC.LAYOUT_VERTICAL,

                    layerSectionView: Footprint.LayerSectionView.extend(SC.SplitChild, {
                        size: 150,
                        autoResizeStyle: SC.RESIZE_AUTOMATIC,
                        sizeOffset:-5,
                        canCollapse:YES
                    }),
                    toolsetView: Footprint.ToolSectionView.extend(SC.SplitChild, {
                        size: 130,
                        maximumSize: 130,
                        minimumSize: 130,
                        sizeOffset: -10,
                        positionOffset: 5,
                        canCollapse:YES
                    }),
                    builtFormsView: Footprint.BuiltFormSectionView.extend(SC.SplitChild, {
                        size: 100,
                        sizeOffset: -5,
                        positionOffset: 5,
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
                        value: 'UrbanFootprint rev. 2014.1.27 \n © 2013 Calthorpe Associates',
                        layout: {top: 0.05, left: 40}
                    })
                })
            }),
            mapView: Footprint.MapSectionView.extend(SC.SplitChild, {
                autoResizeStyle: SC.RESIZE_AUTOMATIC,
                sizeOffset:-5,
                positionOffset:5,
                canCollapse:NO
            }),
            analyticView: Footprint.AnalyticSectionView.extend(SC.SplitChild, {
                 size: 275,
                 sizeOffset:-5,
                 positionOffset:5,
                 canCollapse:YES
            })
        })
    })
});
