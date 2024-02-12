class VeriableLenght:

    def encode(self, intVal):
        output = []
        while True:
            digit = intVal % 128
            intVal = intVal // 128
            # if there are more digits to encode, set the top bit of this digit
            if intVal > 0:
                digit = digit | 0x80
            output.append(digit)
            if intVal <= 0:
                return output

    def decode(self, bytesVal):
        indx = 0
        multiplier = 1
        value = 0
        while True:
            digit = bytesVal[indx]
            value += (digit & 127) * multiplier
            multiplier *= 128
            indx = indx + 1
            if (digit & 128) == 0:
                return value

# 3.1 CONNECT – Client requests a connection to a Server
class ConnectPacket:
    def __init__(self):

        self.__var_len = VeriableLenght()

        # 3.1.1 Fixed header
        self.__fixed_header = [
            b"00010000", # message type
            self.__var_len.encode(123) # remainig lenght
        ]

        # 3.1.2 Variable header
        self.__variable_header = [

            # 3.1.2.1 Protocol Name
            b"00000000", # Length MSB (0) 
            b"00000100", # Length LSB (4)
            b"01001101", # ‘M’
            b"01010001", # ‘Q’
            b"01010100", # ‘T’
            b"01010100", # ‘T’

            # 3.1.2.2 Protocol Level
            b"00000100", # Protocol Level

            # 3.1.2.3 Connect Flags
            # User Name Flag, Password Flag, Will Retain, Will QoS (2 bits), Will Flag, Clean Session, Reserved
            [0, 0, 0, 0, 1, 1, 1, 0],

            # 3.1.2.10 Keep Alive
            b"00000000", # Keep Alive MSB
            b"00000000", # Keep Alive LSB
        ]

        # 3.1.3 Payload
        self.__payload = [

        ]

if __name__ == '__main__':
    inp = 321121212
    print(f"Input: {inp}")

    vl = VeriableLenght()
    encodedBytes = vl.encode(inp)

    print("Encoded bytes: ", end="")
    for b in encodedBytes:
        print(bin(b), end=",")

    print(f"\nDecoded: {vl.decode(encodedBytes)}")