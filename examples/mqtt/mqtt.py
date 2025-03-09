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

# 1.5.3 UTF-8 encoded strings
class Utf8EncStr:
    def encode(self, str):
        strBytes = bytes(str, "utf-8")
        lenBytes = len(strBytes).to_bytes(2, "big")
        return lenBytes + strBytes

# 3.1 CONNECT – Client requests a connection to a Server
class ConnectPacket:
    def __init__(self):

        # 3.1.2 Variable header
        self.__variable_header = [

            # 3.1.2.1 Protocol Name
            0b00000000, # Length MSB (0) 
            0b00000100, # Length LSB (4)
            0b01001101, # ‘M’
            0b01010001, # ‘Q’
            0b01010100, # ‘T’
            0b01010100, # ‘T’

            # 3.1.2.2 Protocol Level
            0b00000100, # Protocol Level

            # 3.1.2.3 Connect Flags
            # User Name Flag, Password Flag, Will Retain, Will QoS (2 bits), Will Flag, Clean Session, Reserved
            0b00001010,

            # 3.1.2.10 Keep Alive
            0b00000000, # Keep Alive MSB
            0b00000000, # Keep Alive LSB
        ]

        utf8_enc_str = Utf8EncStr()
        # 3.1.3 Payload
        self.__payload = [
            # Client Identifier
            # Will Topic
            # utf8_enc_str.encode("ch9121")
            # Will Message
            # utf8_enc_str.encode("hello")
            # User Name
            # Password
        ]
        self.__addFlat(self.__payload, utf8_enc_str.encode("TESTID"))

        self.__var_len = VeriableLenght()

        # 3.1.1 Fixed header
        self.__fixed_header = [
            0b00010000, # message type
        ]
        # remainig lenght
        for b in self.__var_len.encode(123):
            self.__fixed_header.append(b)

    def getBytes(self):
        result = []
        self.__addFlat(result, self.__fixed_header)
        self.__addFlat(result, self.__variable_header)
        self.__addFlat(result, self.__payload)
        return result

    def __addFlat(self, arr, data):
        for b in data:            
            arr.append(b)


if __name__ == '__main__':
    inp = 321121212
    print(f"Input: {inp}")

    vl = VeriableLenght()
    encodedBytes = vl.encode(inp)

    print("Encoded bytes: ", end="")
    for b in encodedBytes:
        print(bin(b), end=",")

    print(f"\nDecoded: {vl.decode(encodedBytes)}")

    utf8_enc_str = Utf8EncStr()
    for b in utf8_enc_str.encode("AB"):
        print(bin(b))