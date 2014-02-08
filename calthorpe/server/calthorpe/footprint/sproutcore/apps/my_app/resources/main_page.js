// ==========================================================================
// Project:   MyApp - mainPage
// Copyright: @2013 My Company, Inc.
// ==========================================================================
/*globals MyApp */

// This page describes the main user interface for your application.
MyApp.mainPage = SC.Page.design({

  mainPane: SC.MainPane.design({
    childViews: 'list toolbar'.w(),

    list: SC.ScrollView.design({
      layout: { top: 10, bottom: 30, left: 10, right: 10 },
      contentView: MyApp.CustomListView.design({
        layout: { top: 0, bottom: 0, left: 0, right: 0 },
        contentBinding: 'MyApp.testController',
        selectionBinding: 'MyApp.testController.selection',
        visibleTitleItemsBinding: 'MyApp.testController.visibleTitleItems',
        exampleView: MyApp.CustomListItemView,
        rowHeight: 54,
        rowSpacing: 0,
        allowDeselectAll: YES
      })
    }),

    toolbar: SC.View.design({
      layout: { bottom: 0, left: 0, right: 0, height: 30 },
      classNames: ['toolbar'],
      childViews: 'titleVisibleCheckbox'.w(),

      titleVisibleCheckbox: SC.CheckboxView.design({
        layout: { height: 20, width: 200, left: 10, centerY: 0 },
        title: 'Title Visible',
        isEnabled: NO,
        isEnabledBinding: SC.Binding.oneWay().bool('MyApp.mainPage.list*selection.firstObject'),
        valueBinding: 'MyApp.testController.itemTitleVisible'
      })
    })
  }),

  list: SC.outlet('mainPane.list.contentView')
});
