/* 
 * UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
 * 
 * Copyright (C) 2012 Calthorpe Associates
 * 
 * This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
 * 
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * 
 * Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
 */

// Modified based on http://broadcastingadam.com/2011/04/sproutcore_login_tutorial/
// The login page should only show up when the user hasn't logged in before. We'll store a cookie with the username and apiKey afterward
Footprint.loginPage = SC.Page.design({
    mainPane: SC.MainPane.design({
        defaultResponder: 'Footprint.statechart',
        childViews: 'loginForm'.w(),

        loginForm: SC.View.design({
            layout: { width: 200, height: 160, centerX: 0, centerY: 0 },
            childViews: 'header userName password loginButton'.w(),

            header: SC.LabelView.design({
                layout: { width: 200, height: 24, top: 0, centerX: 0 },
                controlSize: SC.LARGE_CONTROL_SIZE,
                value: 'Login Required',
                textAlign: SC.ALIGN_CENTER
            }),

            userName: SC.TextFieldView.design({
                layout: { width: 150, height: 30, top: 30, centerX: 0},
                hint: 'Username',
                valueBinding: 'Footprint.loginController.content.username'
            }),

            password: SC.TextFieldView.design({
                layout: {  width: 150, height: 30, top: 80, centerX: 0 },
                hint: 'Password',
                type: 'password',
                valueBinding: 'Footprint.loginController.content.password'
            }),

            loginButton: SC.ButtonView.design({
                layout: { width: 100, height: 30, top: 120, centerX: 0 },
                controlSize: SC.HUGE_CONTROL_SIZE,
                title: 'Login',
                action: 'doAuthenticate'
            })
        })
    })
});