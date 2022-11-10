var http = require('http');
var dt = require('./date_time');

http.createServer(function (req, res) {
  res.writeHead(200, {'Content-Type': 'text/html'});
  res.write("Hello!\n");
  res.write("The date and time are currently: " + dt.myDateTime() + "\n");
  res.write("Plant Name: \n");
  res.write("Temperature and Weather: \n");
  res.write("Amount of Water Used: \n");
  res.end();
}).listen(8080);