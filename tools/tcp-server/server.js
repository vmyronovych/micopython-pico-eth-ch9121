var net = require('net');

var HOST = '0.0.0.0';
var PORT = 6969;

net.createServer(function(socket) {
    logDevice("CONNECTED");
    
    socket.on("data", function(data) {
        logDevice(data);
    });

    socket.on("close", function(data) {
        logDevice("DISCONNECTED")
    });

    socket.write(`HELLO ${socket.remoteAddress}:${socket.remotePort}`);

    function logDevice(msg) {
        var deviceName = `${socket.remoteAddress}:${socket.remotePort}`;
        console.log(`DEVICE[${deviceName}]: ${msg}`);
    }

}).listen(PORT, HOST);


console.log(`Server listening on ${HOST}:${PORT}`);