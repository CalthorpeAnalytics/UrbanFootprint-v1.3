var app = require('http').createServer(handler),
    io = require('socket.io').listen(app),
    fs = require('fs'),
    redis = require('redis');

io.set('transports', [
    'websocket'
  , 'flashsocket'
  , 'htmlfile'
  , 'jsonp-polling'
]);

app.listen(8081);

function handler(req, res) {
    // just return the index HTML used to test
    fs.readFile(__dirname + '/index.html',
    function (err, data) {
        if (err) {
            res.writeHead(500);
            return res.end('Error loading index.html');
        }

        res.writeHead(200);
        res.end(data);
    });
}

io.configure( function() {
    io.set('close timeout', 60*60*24); // 24h time out
});

function SessionController (userid) {
    // session controller class for managing redis connections

    this.sub = redis.createClient();
    this.pub = redis.createClient();
    this.userid = userid;
    this.channel = 'channel_' + userid;
}

SessionController.prototype.subscribe = function(socket) {


    this.sub.on('message', function(channel, message) {
        socket.emit('serversays', message);
    });

    this.sub.subscribe(this.channel);
};


SessionController.prototype.unsubscribe = function() {
    this.sub.unsubscribe(this.channel);
};

SessionController.prototype.publish = function(message) {
    this.pub.publish(this.channel, message);
};

SessionController.prototype.destroyRedis = function() {

    if (this.sub !== null)
        this.sub.quit();

    if (this.pub !== null)
        this.pub.quit();
};

io.sockets.on('connection', function (socket) {
    // the actual socket callback

    console.log('Connection from: ' + socket.id);

    // client asked to authenticate
    socket.on('calthorpe_auth', function(data) {

        var msg = JSON.parse(data);

        console.log('calthorpe_auth : ' + data);

        socket.get('sessionController', function(err, sessionController) {


            if (sessionController === null) {

                // here we have to implement authentication (just make call to django and check
                // that the session id we are given is valid), for now, assume msg.user is valid
                // however if we failed, we should emit:
                //
                // result = JSON.stringify({event: 'calthorpe_auth_result', msg: { status: 'bad_credentials' } });
                // socket.emit('serversays', result);


                var sessionController = new SessionController(msg.userid);
                socket.set('sessionController', sessionController);
                sessionController.subscribe(socket);
                var result = JSON.stringify({event: 'calthorpe_auth_result', msg: { status: 'ok' } });
                socket.emit('serversays', result);

            } else {

                // the user already logged in once and should disconnect and reconnect clear session
                // data

                var result = JSON.stringify({event: 'calthorpe_auth_result', msg: { status: 'reconnect' } });
                socket.emit('serversays', result);

                return;
            }
        });
    });

    // receiving events from client
    socket.on('event', function (data) {

        var msg = JSON.parse(data);

        socket.get('sessionController', function(err, sessionController) {

            if (sessionController === null) {

                var result = JSON.stringify({event: 'calthorpe_auth_result', msg: { status: 'need_authenticate' } });
                socket.emit('serversays', result);

                return;
            }

            // here we have to implement authorization of cookie to make
            // sure that this session id is valid and belongs to the user
            // if that is not correct, we should emit:
            //
            // result = JSON.stringify({event: 'calthorpe_auth_result', msg: { status: 'bad_session' } });
            // socket.emit('serversays', result);

            console.log(msg);

            // only send clientsays event
            if (msg.event === "clientsays")
            {
                //var reply = JSON.stringify(msg);
                sessionController.publish(data);
                console.log("clientsays sent");
            }
        });
    });


    socket.on('disconnect', function() { // disconnect from a socket - might happen quite frequently depending on network quality

        socket.get('sessionController', function(err, sessionController) {

            if (sessionController === null)
                return;

            sessionController.unsubscribe();
            sessionController.destroyRedis();

            socket.set('sessionController', null);
        });
    });
});
