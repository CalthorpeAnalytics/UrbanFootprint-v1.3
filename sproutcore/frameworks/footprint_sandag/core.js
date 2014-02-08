// ==========================================================================
// Project:   FootprintSandag
// Copyright: @2013 My Company, Inc.
// ==========================================================================
/*globals FootprintSandag */

/** @namespace

  My cool new framework.  Describe your framework.

  @extends SC.Object
*/
window.FootprintSandag = SC.Object.create(
  /** @scope FootprintSandag.prototype */ {

  NAMESPACE: 'FootprintSandag',
  VERSION: '0.1.0',

  logoPath: sc_static('images/logo.png'),

  STATIC: sc_static('images/logo.png').replace('images/logo.png', '%@')

});
