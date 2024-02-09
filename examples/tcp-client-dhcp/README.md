# CH9121 Tcp Client Mode

This example shows:
- how to configure CH9121 TCP Client mode 
- enable DHCP so the chip can automatically obtain IP address from your router
- send simple message to TCP Server and read reply

In order to run this example you should have TCP server up and running.
You can find simple [Node.js](https://nodejs.org) TCP server in this repo: [./tools/tcp-server/server.js](/tools/tcp-server/server.js)

To run server:
- Open terminal
- Navigate to [./tools/tcp-server/](/tools/tcp-server/) folder
- Start server

```bash
node server.js
```

You will need to have [Node.js](https://nodejs.org) installed on your machine.
Server starts by default on port `6969`
Once the server is up and running you should change target ip in the example code to match the IP address of your tcp server

```python
socket = ClientSocket("192.168.1.51", 6969) #"192.168.1.51" - mast be IP address of your TCP server
```

If you are on linux/ubuntu then one way to get IP address of your TCP server is to run `ip addr` command, e.g.: `ip addr | grep "192"`

If you use `vscode` + [MicroPico](vscode:extension/paulober.pico-w-go) extension the all you need to run this example:
 - upload project to pico using [MicroPico](vscode:extension/paulober.pico-w-go) extension
 - Open [main.py](./main.py) file in `vscode` and press `run` (The button which is provided by [MicroPico](vscode:extension/paulober.pico-w-go) extension)
