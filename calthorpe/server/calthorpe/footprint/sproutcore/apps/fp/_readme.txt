MODELS
------
See the models/ and fixtures/ directories.

The Scenario model, for example:

   ScenarioCategory:  (models/scenario_model.js)
     name
     scenarios
  
   Scenario:  (models/scenario_model.js)
     name
     population
     category

These models have fixtures with dummy data:
     
   ScenarioCategory.FIXTURES  (fixtures/config_entity_fixtures.js)
   Scenario.FIXTURES  (fixtures/config_entity_fixtures.js)



CONTROLLERS
-----------
See the controllers/ directory.

The controllers mediate between the model and the view.

In main.js, we set the content for the scenarioController:

    // main.js
    MainApp.scenariosController.set('content', MainApp.scenariosContent);

The controller and its content are defined in controllers/scenarios_controller.js.

The controller is a tree view controller:

    // controllers/scenarios_controller.js
    MainApp.scenariosController = SC.TreeController.create();

The content represents the root node of the tree view (SourceListView), and provides its children
by performing a query for every ScenarioCategory:

    // controllers/scenarios_controller.js
    MainApp.scenariosContent = SC.Object.create({
        name: "root",
        treeItemChildren: function(){
            return MainApp.store.find(SC.Query.local(MainApp.ScenarioCategory, { orderBy: 'guid' }));
        }.property(),
    });

The tree view finds this content by binding its "content" property to the controller's "arrangedObjects" property:

    // views/top_half_view.js
    scenariosView: SC.ScrollView.extend({
        contentView: SC.SourceListView.extend({
            contentBinding: SC.Binding.oneWay('MainApp.scenariosController.arrangedObjects'),
            contentValueKey: 'name',
        })
    })



VIEWS
-----
See the views/ directory.

The UI is broken down into a views hierarchy like so:

 - MainPane (views/MainPain.js)

   - ProjectTitlebarView (views/project_section_view.js)

   - splitView

     - UpperView (views/top_half_view.js)

       - titlebarsView
         - scenarioTitlebar  [ToolbarView]
         - populationTitlebar  [ToolbarView]

       - scenariosView  [Scrollview]
         - contentView  [SourceListView]
           - exampleView  [ListItemView]
             - populationView
               - barView
               - labelView
           
     - LowerView (views/bottom_half_view.js)
     
       - sidebarView
         - layersView
         - toolsView
         - placetypesView

       - MapView (views/map_section_view)

       - settingsView
       

Caveat:  In a number of place (search for "hack", child views are appended to ListItemViews.  This appears to not
work as intended (the child views disappear upon selection).  Some other approach is needed, perhaps using standard
Views for the list items.



     