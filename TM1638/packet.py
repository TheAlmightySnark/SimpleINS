
class Packet:


    packet = None

    def __init__(self, data, hex=True):
        self.packet = bin(data)[2:].zfill(8)
    
    #put zeroes in front of packet or behind packet to adress specific display
    def zfill(self, length):
        self.packet = self.packet.zfill(length)

    def ljust(self, length):
        self.packet = self.packet.ljust(length, '0')
