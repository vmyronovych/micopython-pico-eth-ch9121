class ConfigFormatter:
    def __init__(self) -> None:
        pass

    def ip(self, ipBytes):
        return "{}.{}.{}.{}".format(ipBytes[0], ipBytes[1], ipBytes[2], ipBytes[3])