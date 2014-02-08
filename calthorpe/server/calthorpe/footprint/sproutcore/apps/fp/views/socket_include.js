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


(function() {

    // Override the SocketIO constructor to provide a default
    // value for the port, which is added to os.environ in the
    // runserver_socketio management command.
    var prototype = io.Socket.prototype;
    io.Socket = function(host, options) {
        options = options || {};
        options.port = options.port || 8000;
        return prototype.constructor.call(this, host, options);
    };

    // We need to reassign all members for the above to work.
    for (var name in prototype) {
        io.Socket.prototype[name] = prototype[name];
    }

    // Arrays are transferred as individual messages in Socket.IO,
    // so we put them into an object and check for the __array__
    // message on the server to handle them consistently.
    var send = io.Socket.prototype.send;
    io.Socket.prototype.send = function(data) {
        if (data.constructor == Array) {
            channel =  data[0] == '__subscribe__' || data[0] == '__unsubscribe__';
            if (!channel) {
                data = ['__array__', data];
            }
        }
        return send.call(this, data);
    };

    // Set up the subscription methods.
    io.Socket.prototype.subscribe = function(channel) {
        this.send(['__subscribe__', channel]);
        return this;
    };
    io.Socket.prototype.unsubscribe = function(channel) {
        this.send(['__unsubscribe__', channel]);
        return this;
    };

})();
