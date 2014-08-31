/**
 *
 * Created by calthorpe on 2/19/14.
 */
sc_require('views/info_view/info_pane_crud_buttons_view');

Footprint.BuiltFormButtonsView = Footprint.InfoPaneCrudButtonsView.extend({
    closeButtonLayout: {bottom: 5, left: 20, height:24, width:80},
    revertButtonLayout: {bottom: 5, left: 260, height:24, width:80},
    saveButtonLayout: {bottom: 5, left: 170, height:24, width:80}
});
