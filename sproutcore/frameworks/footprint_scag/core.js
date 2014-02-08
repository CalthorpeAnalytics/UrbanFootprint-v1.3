// ==========================================================================
// Project:   FootprintScag
// Copyright: @2013 My Company, Inc.
// ==========================================================================
/*globals FootprintScag */

/** @namespace

  My cool new framework.  Describe your framework.

  @extends SC.Object
*/
window.FootprintScag = SC.Object.create(
  /** @scope FootprintScag.prototype */ {

  NAMESPACE: 'FootprintScag',
  VERSION: '0.1.0',

  logoPath: sc_static('images/logo.png'),

  STATIC: sc_static('images/logo.png').replace('images/logo.png', '%@')

});
