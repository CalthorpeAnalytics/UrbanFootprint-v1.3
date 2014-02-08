/*
 * urbanfootprint-california (v1.0), land use scenario development and modeling system.
 * 
 * copyright (c) 2012 calthorpe associates
 * 
 * this program is free software: you can redistribute it and/or modify it under the terms of the gnu general public license as published by the free software foundation, version 3 of the license.
 * 
 * this program is distributed in the hope that it will be useful, but without any warranty; without even the implied warranty of merchantability or fitness for a particular purpose.  see the gnu general public license for more details.
 * 
 * you should have received a copy of the gnu general public license along with this program.  if not, see <http://www.gnu.org/licenses/>.
 * 
 * contact: joe distefano (joed@calthorpe.com), calthorpe associates. firm contact: 2095 rose street suite 201, berkeley ca 94709. phone: (510) 548-6800. web: www.calthorpe.com
 */
sc_require('views/builtformsview');
var pane, view;

module("footprint.builtformsview", {
    setup: function () {
        pane = viewSetup({
            contentSetup: function () {
            },
            views: function () {
                return [Footprint.BuiltFormsView.extend({
                    layout: { top: 0, width: .25 }
                })];
            }
        });
        view = pane.childViews[0];
    },

    teardown: function () {
        viewTeardown();
    }
});

test("Check the tree view bound to the BuiltForm data", function () {

    // Make sure the controller has content
    stop(1500000); // delay main thread up to a second to allow breakpoints to work

    throw "die so we can interact";
    var contentViewPath = 'listView.contentView';
    var params = {
        controllers: Footprint.builtFormControllers,
        controllersPath: 'Footprint.builtFormControllers',
        contentView: view.getPath(contentViewPath),
        contentViewPath: 'Footprint.BuiltFormsView.' + contentViewPath,
        editbarView: view.toolbarView.editbarView
    };
    treeViewValidation(pane, params);
});