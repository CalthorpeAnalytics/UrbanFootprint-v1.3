
/*
* UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
* 
* Copyright (C) 2013 Calthorpe Associates
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

Footprint.socketIO = SC.Object.create({

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
            this.socket.on('serversays', function (msg) {
                var message = $.evalJSON(msg);
                var event = message.event;

                // mess with message as json here
                // append to container and scroll
                var listener =  self[event];
                if (listener) {
                    listener.apply(self, [message]);
                }
                else
                    alert("Unknown SocketIO message: %@".fmt(event));
            });

            // send auth message
            this.socket.emit('calthorpe_auth', $.toJSON({ userid: 1 }));
        }

    }.observes('.socket'),

    calthorpe_auth_result: function(message) {
        SC.Logger.debug("SocketIO authorization result: %@".fmt(message.msg.status));
    },
    /***
     * Run when the core analytic module completes
     * @param message contains a config_entity_id to indicate the completed scenario
     */
    core_complete: function(message) {
        SC.RunLoop.begin();
        SC.Logger.debug('Core Complete for Scenario: %@'.fmt(message))
        Footprint.statechart.sendEvent('analysisDidComplete', SC.Object.create(message));
        SC.RunLoop.end();
    },
    /***
     * Run when the base module completes
     * @param message contains a config_entity_id to indicate the completed project
     */
    base_complete: function(message) {
        var project = Footprint.store.find(Footprint.Project, message.config_entity_id);
        SC.Logger.debug('Base Complete for Project: %@'.fmt(project))
    },
    /***
     * Run when an export completes. Fetches the url to commence download
     * @param message
     */
    export_complete: function(message) {
        var api_key = Footprint.userController.getPath('content.firstObject.api_key');
        var request_url = "%@/get_export_result/%@/".fmt(api_key, message.job_id);
        window.location.assign(request_url);
//        SC.Request.getUrl(request_url).send();
    },

    /***
     * Run when an instance clone or create completes. This tells the active saving_state to complete
     * @param message
     */
    config_entity_creation_complete: function(message) {
        Footprint.statechart.sendEvent('creationDidComplete', SC.Object.create(message));
    },
    config_entity_creation_failed: function(message) {
        SC.AlertPane.warn({
            message: "Could complete Scenario clone/create",
            description: "Something went wrong during the clone/creation process"
        });
    }
});
