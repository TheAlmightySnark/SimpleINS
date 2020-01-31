class Packet:


    packet = None

    def __init__(self, adress, data):

        binary_adress = str(bin(adress))[2:].zfill(4) #zero padded string, adress as binary value
        self.packet = str(binary_adress + data).zfill(16) #returns a 16 bit string

    #put zeroes in front of packet or behind packet to adress specific display
    def zfill(self, length):
        self.packet = self.packet.zfill(length)

    def ljust(self, length):
        self.packet = self.packet.ljust(length, '0')
