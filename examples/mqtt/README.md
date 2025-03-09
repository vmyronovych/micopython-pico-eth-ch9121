# CH9121 - MQTT CONNECT

## This example shows:
- how to configure CH9121 TCP Client mode 
- enable DHCP so the chip can automatically obtain IP address from your router
- send MQTT CONNECT message to [Mosquitto](https://mosquitto.org/) running in [Docker](https://www.docker.com/) and read response

## Prerequisites
- [Docker](https://docs.docker.com/engine/install/ubuntu/) installed on your machine
- [Docker Compose](https://docs.docker.com/compose/install/linux/). You might have it after installing docker
- [`Visual Studio Code`](https://code.visualstudio.com/) installed on your machine. This is optional but with extension mentioned below it would be really easy to run the example.
- [MicroPico](vscode:extension/paulober.pico-w-go) extension for [`Visual Studio Code`](https://code.visualstudio.com/). This is optional but very handy!
- `python`. This example was tested on version `Python 3.10.12`
- [Raspbery Pi Pico H](https://www.raspberrypi.com/products/raspberry-pi-pico/) with a flashed [MicroPython](https://micropython.org/). Follow this documentation for the flashing instructions: [1.2. Installing MicroPython on Raspberry Pi Pico](https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-python-sdk.pdf?_gl=1*3uoue*_ga*NDYyNDYyODcwLjE3MDc0ODY5MTM.*_ga_22FD70LWDS*MTcwNzU5MDM2MC4xLjEuMTcwNzU5MDYyOS4wLjAuMA..)

## Start [Mosquitto](https://mosquitto.org/)
- Open terminal
- Navigate to folder for this example
- Execute following command:

```bash
docker compose up && docker compose rm -fsv
```

## Run example

Once the [Mosquitto](https://mosquitto.org/) is up and running you should change target ip in the example code to match the IP address of the [Mosquitto](https://mosquitto.org/)

```python
socket = TcpClientSocket("192.168.1.51", 8080) # Change ip here to the ip of your [Mosquitto](https://mosquitto.org/)
```

If you are on linux/ubuntu then one way to get IP address of your [Mosquitto](https://mosquitto.org/) is to run `ip addr` command, e.g.: `ip addr | grep "192"`

If you use `vscode` + [MicroPico](vscode:extension/paulober.pico-w-go) extension then all you need to run this example:
 - upload project to pico using [MicroPico](vscode:extension/paulober.pico-w-go) extension
 - Open [main.py](./main.py) file in `vscode` and press `run` (The button which is provided by [MicroPico](vscode:extension/paulober.pico-w-go) extension)
