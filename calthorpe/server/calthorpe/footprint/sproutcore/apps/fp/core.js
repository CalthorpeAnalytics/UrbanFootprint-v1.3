// ==========================================================================
// Project:   Footprint
// Copyright: @2012 My Company, Inc.
// ==========================================================================
/*globals Footprint */
sc_require('controllers/controller_extensions');
sc_require('system/autonomous_store');

/** @namespace

  My cool new app.  Describe your application.
  
  @extends SC.Object
*/
//SC.LOG_OBSERVERS = YES;
F = Footprint = SC.Application.create(
  /** @scope Footprint.prototype */ {

  NAMESPACE: 'Footprint',
  VERSION: '0.1.0',

  // We do this primitive check to flag the development mode. There might be a built-in flag.
  isDevelopment:window.location.port==4020,

  // This is your application store.  You will use this store to access all
  // of your model data.  You can also set a data source on this store to
  // connect to a backend server.  The default setup below connects the store
  // to any fixtures you define.
  //store: SC.Store.create().from('Footprint.FixturesDataSource')

        // Here is the server connector that replaces the fixtures connector
  store: SC.Store.create({
      commitRecordsAutomatically: NO
  }).from('Footprint.DataSource')
});
