# CH9121 Tcp Client Mode

## This example shows:
- how to configure CH9121 TCP Client mode 
- enable DHCP so the chip can automatically obtain IP address from your router
- send simple message to TCP Server and read reply

## Prerequisites
- [Node.js](https://nodejs.org) installed on your machine

For Ubuntu
```bash
sudo apt install nodejs
```

- [`Visual Studio Code`](https://code.visualstudio.com/) installed on your machine. THis is optional but with extension mentioned below it would be really easy to run the example.
- [MicroPico](vscode:extension/paulober.pico-w-go) extension for [`Visual Studio Code`](https://code.visualstudio.com/). This is optional but very handy!
- `python`. This example was tested on version `Python 3.10.12`
- [Raspbery Pi Pico H](https://www.raspberrypi.com/products/raspberry-pi-pico/) with a flashed [MicroPython](https://micropython.org/). Follow this documentation for the flashing instructions: [1.2. Installing MicroPython on Raspberry Pi Pico](https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-python-sdk.pdf?_gl=1*3uoue*_ga*NDYyNDYyODcwLjE3MDc0ODY5MTM.*_ga_22FD70LWDS*MTcwNzU5MDM2MC4xLjEuMTcwNzU5MDYyOS4wLjAuMA..)

In order to run this example you should have TCP server up and running.
You can find simple [Node.js](https://nodejs.org) TCP server in this repo: [./tools/tcp-server/server.js](/tools/tcp-server/server.js)

## Start TCP Server
- Open terminal
- Navigate to folder for this example
- Start server

```bash
node tcp-server.js
```

## Run example

Once the tcp server is up and running you should change target ip in the example code to match the IP address of your tcp server

```python
socket = TcpClientSocket("192.168.1.51", 6969) # Change ip and port here to the ip and port of your TCP Server
```

If you are on linux/ubuntu then one way to get IP address of your TCP server is to run `ip addr` command, e.g.: `ip addr | grep "192"`

If you use `vscode` + [MicroPico](vscode:extension/paulober.pico-w-go) extension then all you need to run this example:
 - upload project to pico using [MicroPico](vscode:extension/paulober.pico-w-go) extension
 - Open [main.py](./main.py) file in `vscode` and press `run` (The button which is provided by [MicroPico](vscode:extension/paulober.pico-w-go) extension)
