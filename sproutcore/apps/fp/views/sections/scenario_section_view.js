sc_require('views/section_toolbars/scenario_toolbar_view');
sc_require('views/sections/section_view');
sc_require('views/info_views/analytics/fiscal_model_management_view');
sc_require('views/config_entity/analytic_bar_view');


Footprint.ScenarioSectionView = SC.View.extend({
    classNames: "footprint-scenario-section-view".w(),
    childViews: 'overlayView toolbarView listView'.w(),

    overlayView: Footprint.OverlayView.extend({
        contentBinding: SC.Binding.oneWay('Footprint.scenarioCategoriesTreeController'),
        statusBinding:SC.Binding.oneWay('Footprint.scenarioCategoriesTreeController.status')
    }),
    toolbarView: Footprint.ScenarioToolbarView.extend({
        layout: { height: 17},
        controller: Footprint.projectsController
    }),
    listView: SC.ScrollView.extend({
        layout: { top: 18 },

        contentView: SC.SourceListView.extend({
            isEnabledBinding: SC.Binding.oneWay('.content').bool(),
            rowHeight: 20,
            isEditable: YES,
            actOnSelect: YES,
            canEditContent: YES,
            canDeleteContent: YES,
            canReorderContent: YES,

            contentBinding: SC.Binding.oneWay('Footprint.scenarioCategoriesTreeController.arrangedObjects'),
            contentValueKey: 'name',
            selectionBinding: SC.Binding.from('Footprint.scenarioCategoriesTreeController.selection'),

            // This is used to show progress bar overlays after clone/create/update
            editControllerContent:null,
            editControllerContentBinding: SC.Binding.from('Footprint.scenariosEditController.content'),

            groupExampleView: SC.View.extend(SC.ContentDisplay, {
                contentDisplayProperties: ['name'],
                render: function(context) {
                    var title = this.getPath('content.name') || '';
                    title = title.titleize();
                    context.begin()
                           .addClass(this.getPath('theme.classNames'))
                           .addClass(['sc-view', 'footprint-scenario-group'])
                           .push(title)
                           .end();
                },
                update: function($context) {
                    var title = this.getPath('content.name') || '';
                    title = title.titleize();
                    $context.find('.footprint-scenario-group').text(title);
                }
            }),
            exampleView: SC.View.extend(SC.Control, {
                classNames: ['sc-list-item-view', 'footprint-scenario-item'],
                childViews: 'progressOverlayView nameView populationView dwellingUnitsView employmentView'.w(),

                // The view that can be edited by double-clicking
                editableChildViewKey: 'nameView',
                editControllerContent: null,
                editControllerContentBinding: SC.Binding.oneWay('.parentView.editControllerContent'),

                nameView: Footprint.EditableModelStringView.extend({
                    isEditable: NO,
                    layout: {left: 0, right:270, top: 1},
                    valueBinding: SC.Binding.oneWay('.parentView*content.name')
                }),
                progressOverlayView: Footprint.ProgressOverlayView.extend({
                    layout: { left:0, right: 270, centerY: 0, height: 16},
                    contentBinding: SC.Binding.oneWay('.parentView.content')
                }),
                // TODO these will be dynamic based on the Result(s) with type 'analytic_bars'
                // TODO Find the first Result with result_type=='analytic_bars'. Assume the result has the following
                // attribute keys
                populationView: Footprint.AnalyticBarView.extend({
                    layout: {right:180, width: 90},

                    configEntityBinding: SC.Binding.from('.parentView.content'),
                    queryAttributeKey: 'population',
                    isVisibleBinding: SC.Binding.from(".parentView.content").notContentKind(Footprint.TreeItem)
                }),
                dwellingUnitsView: Footprint.AnalyticBarView.extend({
                    layout: {right:90, width: 90},

                    configEntityBinding: SC.Binding.from('.parentView.content'),
                    queryAttributeKey: 'dwelling_units',
                    isVisibleBinding: SC.Binding.from(".parentView.content").notContentKind(Footprint.TreeItem)
                }),
                employmentView: Footprint.AnalyticBarView.extend({
                    layout: {right:0, width: 90},

                    configEntityBinding: SC.Binding.from('.parentView.content'),
                    queryAttributeKey: 'employment',
                    isVisibleBinding: SC.Binding.from(".parentView.content").notContentKind(Footprint.TreeItem)
                })
            })
        })
    })
});

