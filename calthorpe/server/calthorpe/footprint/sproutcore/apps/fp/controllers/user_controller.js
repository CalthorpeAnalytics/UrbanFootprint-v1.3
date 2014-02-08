// ==========================================================================
// Project:   Footprint.loginController
// Copyright: @2012 My Company, Inc.
// ==========================================================================
/*globals Footprint */

/** @class

  (Document Your Controller Here)

  @extends SC.Object
*/

sc_require('models/identification_models');

/***
 * User controller expects a single item list or single Footprint.User record set to its content property
 * @type {SC.Object}
 */
Footprint.userController = SC.ArrayController.create( Footprint.ArrayContentSupport, {
    setCookie: function(duration) {
        var cookie = this.findCookie() ||
            SC.Cookie.create({
            name: 'user.api_key',
            value: Footprint.userController.getPath('firstObject.api_key')
        });
        if (duration) {
            var d = new Date();
            d.setTime(d.getTime() + duration);
            cookie.expires = d;
        }
        else
            cookie.expires = null;
        cookie.write();
    },
    destroyCookie: function() {
        var cookie = this.findCookie();
        if (cookie)
            cookie.destroy()
    },
    findCookie: function() {
        return SC.Cookie.find('user.api_key');
    }
});
