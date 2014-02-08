// ==========================================================================
// Project:   FootprintSacog
// Copyright: @2013 My Company, Inc.
// ==========================================================================
/*globals FootprintSacog */

/** @namespace

  My cool new framework.  Describe your framework.

  @extends SC.Object
*/
window.FootprintSacog = SC.Object.create(
  /** @scope FootprintSacog.prototype */ {

  NAMESPACE: 'FootprintSacog',
  VERSION: '0.1.0',

  logoPath: sc_static('images/logo.png'),

  STATIC: sc_static('images/logo.png').replace('images/logo.png', '%@')

});
