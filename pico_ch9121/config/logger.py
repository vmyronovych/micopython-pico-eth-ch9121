class SerialLogger:
    def __init__(self) -> None:
        pass

    def logAll(self, config):
        self.uart.read() # flusing uart buffer before reading settings

        print("\nDevice Network")
        print("==============")

        print(f'IP:                      {self.__formatAsIpString(config.device.ip)}')

    def __formatAsIpString(self, ipBytes):
        return "{}.{}.{}.{}".format(ipBytes[0], ipBytes[1], ipBytes[2], ipBytes[3])