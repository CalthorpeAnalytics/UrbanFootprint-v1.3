// ==========================================================================
// Project:   MyApp.CustomListView
// Copyright: @2013 My Company, Inc.
// ==========================================================================
/*globals MyApp */

/** @class

  (Document Your View Here)

  @extends SC.View
*/
MyApp.CustomListView = SC.ListView.extend({

  visibleTitleItems: null,

  visibleTitleItemsBindingDefault: SC.Binding.oneWay(),

  visibleTitleItemsDidChange: function() {

      this.reload(null);
  }.observes('*visibleTitleItems.[]'),

  createItemView: function(exampleClass, idx, attrs) {
      var visibleTitleItems = this.get('visibleTitleItems');

      if (visibleTitleItems) {
        attrs.isTitleVisible = visibleTitleItems.indexOf(attrs.content) > -1 ? YES : NO;
      }
      var view = exampleClass.create(attrs);

      delete attrs.isTitleVisible;

      return view;
  }

});
