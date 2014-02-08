
// These need to load in the specified order
sc_require('resources/jquery_ui/jquery_ui_core');
sc_require('resources/jquery_ui/widget');
sc_require('resources/jquery_ui/colorpicker');
sc_require('resources/jquery_ui/mouse');
sc_require('states/test_states');

Footprint.main = function main() {
    Footprint.statechart.initStatechart();
    // The statechart is the deafultResponder. It will delegate actions throughout the hierarchy of active states
    // until a states responds to the action
    SC.RootResponder.responder.set('defaultResponder', Footprint.statechart);

    Footprint.DO_STATE_TESTS = NO;
    //
    // Skipping the login page for now to save time
    setUserContent();

    Footprint.statechart.gotoState('applicationReadyState');
};
function setUserContent() {
    if ((Footprint.store.dataSource.kindOf && Footprint.store.dataSource.kindOf(Footprint.DataSource)) || Footprint.store.dataSource == 'Footprint.DataSource') {
        // TODO this precooked username and password should be something always created on the server for testing
        var users = Footprint.store.createRecords(Footprint.User, [{id:1, username:'test', api_key:'TEST_API_KEY' + ''}]);
        Footprint.userController.set('content', users);
        Footprint.userController.set('userDefaults', SC.UserDefaults.create({ appDomain: "Footprint", userDomain:users.get('firstObject') }));
    }
}


function main() { Footprint.main(); }
