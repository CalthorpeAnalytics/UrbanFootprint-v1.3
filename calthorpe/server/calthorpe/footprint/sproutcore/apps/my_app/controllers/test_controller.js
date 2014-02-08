// ==========================================================================
// Project:   MyApp.testController
// Copyright: @2013 My Company, Inc.
// ==========================================================================
/*globals MyApp */

/** @class

  (Document Your Controller Here)

  @extends SC.ArrayController
*/
MyApp.testController = SC.ArrayController.create(
/** @scope MyApp.testController.prototype */ {
         selection: null,

  visibleTitleItems: [],

  itemTitleVisible: function(key, value)  {
    var sel = this.getPath('selection.firstObject');
    if (!sel) return NO;

    var visibleTitles = this.get('visibleTitleItems');

    if (value !== undefined) {
      if (value === YES) {
        if (visibleTitles.indexOf(sel) === -1) visibleTitles.pushObject(sel);
        return YES;
      }
      else if (value === NO) {
        if (visibleTitles.indexOf(sel) > -1) visibleTitles.removeObject(sel);
        return NO;
      }
    }

    return visibleTitles.indexOf(sel) > -1 ? YES : NO;
  }.property('selection').cacheable()

});

