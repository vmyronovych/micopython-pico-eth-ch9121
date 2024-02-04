class Config:
    def __init__(self) -> None:
        self.device = DeviceConfig()
        self.port1 = SerialPortConfig()
        self.port2 = SerialPortConfig()

class DeviceConfig:
    def __init__(self) -> None:
        self.ip
        self.subnetMask
        self.gateway

class SerialPortConfig:
    def __init__(self) -> None:
        pass