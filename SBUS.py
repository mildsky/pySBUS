import serial
import threading
import time

# SBUS footer alternates in a repeating sequence: 0x04 → 0x14 → 0x24 → 0x34 → 0x04 → ... (only for FUTABA series)

PORT = "/dev/tty.SLAB_USBtoUART"
class SBUS:
    packet = [0]*25
    def __init__(self) -> None:
        self.thread = threading.Thread(target=self.__sbusThread)
        self.thread.daemon = True
    def start(self):
        self.thread.start()
    def __sbusThread(self):
        it = 0
        with serial.Serial(PORT, 100_000, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_TWO) as ser:
            ser.reset_input_buffer()
            while True:
                b = int.from_bytes(ser.read())
                if b == 0x0F:
                    self.packet[0] = b
                    for i in range(24):
                        b = int.from_bytes(ser.read())
                        self.packet[i+1] = b
                    ch = self.parsePacket(self.packet)
                    print(ch)
    def getPacket(self):
        return self.packet
    def parsePacket(self, packet):
        channel = [-1]*18
        channel[0] = (packet[2] << 8 & 0b0111_0000_0000) | packet[1]
        channel[1] = (packet[3] << 5 & 0b0111_1110_0000) | (packet[2] >> 3)
        channel[2] = (packet[5] << 10 & 0b0100_0000_0000) | (packet[4] << 2) | (packet[3] >> 6)
        channel[3] = (packet[6] << 7 & 0b0111_1000_0000) | (packet[5] >> 1)
        channel[4] = (packet[7] << 4 & 0b0111_1111_0000) | (packet[6] >> 4)
        channel[5] = (packet[9] << 9 & 0b0110_0000_0000) | (packet[8] << 1) | (packet[7] >> 7)
        channel[6] = (packet[10] << 6 & 0b0111_1100_0000) | (packet[9] >> 2)
        channel[7] = (packet[11] << 3) | (packet[10] >> 5)
        channel[8] = (packet[13] << 8 & 0b0111_0000_0000) | packet[12]
        channel[9] = (packet[14] << 5 & 0b0111_1110_0000) | (packet[13] >> 3)
        channel[10] = (packet[16] << 10 & 0b0100_0000_0000) | (packet[15] << 2) | (packet[14] >> 6)
        channel[11] = (packet[17] << 7 & 0b0111_1000_0000) | (packet[16] >> 1)
        channel[12] = (packet[18] << 4 & 0b0111_1111_0000) | (packet[17] >> 4)
        channel[13] = (packet[20] << 9 & 0b0110_0000_0000) | (packet[19] << 1) | (packet[18] >> 7)
        channel[14] = (packet[21] << 6 & 0b0111_1100_0000) | (packet[20] >> 2)
        channel[15] = (packet[22] << 3) | (packet[21] >> 5)
        channel[16] = packet[23] & 0b0000_0001
        channel[17] = packet[23] & 0b0000_0010
        __footer = packet[24]
        return channel

if __name__ == "__main__":
    sbus = SBUS()
    sbus.start()
    while True:
        packet = sbus.getPacket()
        # print(sbus.parsePacket(packet))
        time.sleep(0.1)