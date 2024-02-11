const http = require('http');

const hostname = '0.0.0.0';
const port = 8080;

const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'application');

  logDeviceRequest(req.client, req.url);

  var resBody = `${req.url}`;
  res.end(`${resBody}\n`);
  logDeviceResponse(req.client, resBody);
});

function logDeviceRequest(socket, msg) {
  var deviceName = `${socket.remoteAddress}:${socket.remotePort}`;
  console.log(`[${now()}][${deviceName}]: >> ${msg}`);
}

function logDeviceResponse(socket, msg) {
  var deviceName = `${socket.remoteAddress}:${socket.remotePort}`;
  console.log(`[${now()}][${deviceName}]: << ${msg}`);
}

function now() {
  var now = new Date(),
    hh = (now.getHours()<10?'0':'') + now.getHours(),
    mm = (now.getMinutes()<10?'0':'') + now.getMinutes(),
    ss = (now.getSeconds()<10?'0':'') + now.getSeconds();
  return hh + ':' + mm + ':' + ss;
}

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});