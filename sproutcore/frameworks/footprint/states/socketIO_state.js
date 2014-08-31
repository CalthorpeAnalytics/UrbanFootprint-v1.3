
/*
* UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
* 
* Copyright (C) 2014 Calthorpe Associates
* 
* This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
* 
* This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
* 
* You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
* 
* Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
*/

Footprint.resultLibraryUpdate = SC.ObjectController.create({
});

Footprint.SocketIOState = SC.State.design({

    initialSubstate: 'readyState',
    readyState: SC.State.design({
        enterState: function() {
            // Open communication to the socketIO server
            this.get('parentState').initSocketIO();
        }
    }),

    socket: null,
    /***
     * This initiallizes and reconnects the socket to the server.
     * If it fails then the observer will try to reconnect for tries times
     */
    initSocketIO: function() {
        var host = window.location.host.split(':')[0];
        this.set('socket', io.connect('http://' + host + ':8081'));
    },
    tries:5,
    _triesCount:5,

    socketReadyObserver: function() {
        var self = this;
        if (!this.socket) {
            this._triesCount--;
            if (this._triesCount > 0) {
                // Keep trying to connect
                setTimeout(function() {
                    self.initSocketIO();
                }, 1000);
            }
            else {
                logError("Giving up connection to socketIO after %@ tries".fmt(this.tries));
            }
        }
        else {
            // Reset the tries in case we get disconnected and have to reconnect
            this._triesCount = this.tries;

            // Set up the listeners
            if (!this.socket.$events || !this.socket.$events['serversays'] || this.socket.$events['serversays'].length == 0) {
                this.socket.on('serversays', function (msg) {
                    var message = $.evalJSON(msg);

                    // Send the event by its name
                    // message names are matched in states that are appropriate to handle them
                    // For instance showingScenariosState handled createScenarioCompleted and createScenarioFailed,
                    // whereas showingResultsState handles
                    SC.run(function() {
                        Footprint.statechart.sendEvent(message.event.camelize(), SC.Object.create(message));
                    });
                });
            }

            if (this.timer)
                timer.invalidate();
            // Ping the server every hundred seconds until our socket io is better set up in the future
            // This is just debugging info so we know we are still connected
            this.timer = SC.Timer.schedule({
              target: this,
              action: 'calthorpeAuth',
              interval: 100000,
              repeats: YES
            });
        }
    }.observes('.socket'),

    /***
     * Ping to the server
     */
    calthorpeAuth: function() {
        // send auth message
        this.socket.emit(
            'calthorpe_auth',
            $.toJSON({
                userid:F.userController.getPath('firstObject.id')
            }));
    },

    calthorpeAuthResult: function(message) {
        SC.Logger.debug("SocketIO authorization result: %@".fmt(message.msg.status));
    },

    /***
     * Run when an export completes. Fetches the url to commence download
     * @param message
     */
    layerExportCompleted: function(message) {
        var api_key = Footprint.userController.getPath('content.firstObject.api_key');
        var request_url = "%@%@/get_export_result/%@/".fmt(Footprint.isDevelopment ? 'footprint/' : '', api_key, message.job_id);
//        $('#download').attr()

        window.location.assign(request_url);
//        SC.Request.getUrl(request_url).send();
    },

    /***
     * Run when an instance clone or create completes. This tells the active saving_state to complete
     * @param message
     */
    scenarioCreationComplete: function(message) {
        Footprint.statechart.sendEvent('creationDidComplete', SC.Object.create(message));
    },
    scenarioCreationFailed: function(message) {
        SC.AlertPane.warn({
            message: "Could complete Scenario clone/create",
            description: "Something went wrong during the clone/creation process"
        });
    }
});
