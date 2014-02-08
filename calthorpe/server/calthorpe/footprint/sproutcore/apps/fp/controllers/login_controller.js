// ==========================================================================
// Project:   Footprint.loginController
// Copyright: @2012 My Company, Inc.
// ==========================================================================
/*globals Footprint */

/** @class

  (Document Your Controller Here)

  @extends SC.Object
*/

sc_require('models/identification_models')

Footprint.loginContent = Footprint.Login.create({
    username: null,
    password: null,
    api_key: null
});

Footprint.loginController = SC.ObjectController.create({
    allowsMultipleContent:NO
});
