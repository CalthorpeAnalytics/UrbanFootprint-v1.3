// ==========================================================================
// Project:   Footprint
// Copyright: @2012 My Company, Inc.
// ==========================================================================
/*globals Footprint */
sc_require('system/autonomous_store');
sc_require('system/object_extensions');
sc_require('system/state_extensions');
sc_require('system/many_array_extensions');
sc_require('system/child_array_extensions');
sc_require('system/store_extensions');
sc_require('system/binding_extensions');
sc_require('system/controller_extensions');
//sc_require('resources/ZeroClipboard');

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

// Create a path to static content with a wildcard in it. socket.io.js is just used because it's in the resources
// For some reason SC doesn't just offer the path
Footprint.STATIC_FW = sc_static('socket.io.js').replace('socket.io.js','%@');
Footprint.VISIBLE = 'visible';
Footprint.HIDDEN = 'hidden';
Footprint.SOLO = 'solo';

// For copying to the browser copy/paste buffer
// TODO figure out how to load swf files!!
/*
Footprint.clip = new ZeroClipboard({
    moviePath: Footprint.STATIC_FW.fmt('ZeroClipboardFlash.swf')
});
*/
