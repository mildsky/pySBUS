def parsePacket(packet:bytes):
    channels = []
    raw = int.from_bytes(packet, "big")
    for i in range(16):
        channels.append((raw >> (i * 11)) & 0x7FF)
    channels.reverse()
    return channels

if __name__ == "__main__":
    testPacket = b'\xe0\x9b?\x83\x1d\xbf\xe0\xf1\x1f\x05\\\xc0\x01\x0b\xb0\x80\x13\xea\xe3\x01+\\'
    '''
    111 0000 0100 = 1792
    110 1100 1111
    111 0000 0110
    001 1101 1011
    111 1111 0000
    011 1100 0100
    011 1110 0000
    101 0101 1100
    110 0000 0000
    000 0100 0010
    111 0110 0001
    000 0000 0001
    001 1111 0101
    011 1000 1100
    000 0010 0101
    011 0101 1100
    '''
    testParse = parsePacket(testPacket)
    print(testParse)
    for b in testPacket:
        print(f"{b:08b}", end=" ")

