var net = require('net');

var HOST = '0.0.0.0';
var PORT = 6969;

net.createServer(function(socket) {

    logDevice("CONNECTED");
    response("OK")
    
    socket.on("data", function(data) {
        logDeviceRequest(data);
        response("OK")
    });

    socket.on("close", function(data) {
        logDevice("DISCONNECTED")
    });
    
    function response(msg) {
        socket.write(msg);
        logDeviceResponse(msg)
    }

    function logDeviceRequest(msg) {
        var deviceName = `${socket.remoteAddress}:${socket.remotePort}`;
        console.log(`DEVICE[${deviceName}]: >> ${msg}`);
    }

    function logDeviceResponse(msg) {
        var deviceName = `${socket.remoteAddress}:${socket.remotePort}`;
        console.log(`DEVICE[${deviceName}]: << ${msg}`);
    }

    function logDevice(msg) {
        var deviceName = `${socket.remoteAddress}:${socket.remotePort}`;
        console.log(`DEVICE[${deviceName}]: ${msg}`);
    }

    

}).listen(PORT, HOST);


console.log(`Server listening on ${HOST}:${PORT}`);