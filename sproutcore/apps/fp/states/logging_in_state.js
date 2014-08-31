
Footprint.LoggingInState = SC.State.extend({

    /***
     * Transitions from logging in to loading the application
     */
    didCompleteLogin: function() {
        this.gotoState('loadingAppState');
    },

    enterState: function() {
        var cookie = Footprint.userController.findCookie();
        if (cookie && cookie.get('value')) {
            Footprint.loginController.set('api_key', cookie.get('value'));
            this.gotoState('loadingUserState');
            return;
        }
        Footprint.loginPage.get('mainPane').append();
    },

    exitState: function() {
        Footprint.getPath('loginPage.mainPane').remove();
        Footprint.loginController.set('username', null);
        Footprint.loginController.set('password', null);
        Footprint.loginController.set('api_key', null);
    },

    doAuthenticate: function() {
        if (Footprint.loginController.get('username') && Footprint.loginController.get('password')) {
            this.gotoState('loadingUserState')
        }
    },

    initialSubstate: 'loginReadyState',
    loginReadyState: SC.State,

    loadingUserState: Footprint.LoadingState.extend({

        loadingController:Footprint.userController,
        didLoadEvent:'didLoadUser',
        didFailEvent:'didFailToLoadUser',

        enterState: function() {
            Footprint.loginPage.get('loginBypassPane').append();
            sc_super();
        },

        /**
         * Queries for all the scenarios of the ConfigEntity
         * @returns {*}
         */
        recordArray:function() {
            var params = {},
                username = Footprint.loginController.get('username'),
                password = Footprint.loginController.get('password'),
                apiKey = Footprint.loginController.get('api_key');
            if (username && password) {
                params.username = username;
                params.password = password;
            }
            if (apiKey) params.api_key = apiKey;
            return Footprint.store.find(SC.Query.create({
                recordType: Footprint.User,
                location:SC.Query.REMOTE,
                parameters: params
            }));
        },

        exitState: function() {
            Footprint.getPath('loginPage.loginBypassPane').remove();
            sc_super();
        }
    }),

    didLoadUser: function(){
        if (Footprint.userController.get('status') & Footprint.Record.READY) {
            if (Footprint.userController.get('length') == 1) {
                // Put the user apiKey in the cache
                Footprint.userController.setCookie(24*60*60*1000);
                // All good, go to the loading page
                Footprint.statechart.sendEvent("didCompleteLogin");
            } else {
                SC.AlertPane.error("A login error occurred");
                Footprint.userController.set('content', null);
                Footprint.loginController.set('password', null);
                this.gotoState('loginReadyState');
            }
        }
    },

    didFailToLoadUser: function() {
        SC.AlertPane.error("Authentication Failed");
        Footprint.userController.destroyCookie();
        this.gotoState(this.get('parentState'));
    }
});

