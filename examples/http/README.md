# CH9121 - Sipmle HTTP GET request

## This example shows:
- how to configure CH9121 TCP Client mode 
- enable DHCP so the chip can automatically obtain IP address from your router
- send simple HTTP GET request to HTTP server and read response

## Prerequisites
- [Node.js](https://nodejs.org) installed on your machine

For Ubuntu
```bash
sudo apt install nodejs
```

- [`Visual Studio Code`](https://code.visualstudio.com/) installed on your machine. This is optional but with extension mentioned below it would be really easy to run the example.
- [MicroPico](vscode:extension/paulober.pico-w-go) extension for [`Visual Studio Code`](https://code.visualstudio.com/). This is optional but very handy!
- `python`. This example was tested on version `Python 3.10.12`
- [Raspbery Pi Pico H](https://www.raspberrypi.com/products/raspberry-pi-pico/) with a flashed [MicroPython](https://micropython.org/). Follow this documentation for the flashing instructions: [1.2. Installing MicroPython on Raspberry Pi Pico](https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-python-sdk.pdf?_gl=1*3uoue*_ga*NDYyNDYyODcwLjE3MDc0ODY5MTM.*_ga_22FD70LWDS*MTcwNzU5MDM2MC4xLjEuMTcwNzU5MDYyOS4wLjAuMA..)

## Start HTTP Server
- Open terminal
- Navigate to folder for this example
- Start server

```bash
node http-server.js
```

## Run example

Once the http server is up and running you should change target ip in the example code to match the IP address of your http server

```python
socket = TcpClientSocket("192.168.1.51", 8080) # Change ip here to the ip of your HTTP Server
```

If you are on linux/ubuntu then one way to get IP address of your HTTP server is to run `ip addr` command, e.g.: `ip addr | grep "192"`

If you use `vscode` + [MicroPico](vscode:extension/paulober.pico-w-go) extension then all you need to run this example:
 - upload project to pico using [MicroPico](vscode:extension/paulober.pico-w-go) extension
 - Open [main.py](./main.py) file in `vscode` and press `run` (The button which is provided by [MicroPico](vscode:extension/paulober.pico-w-go) extension)
