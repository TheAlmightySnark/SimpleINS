import packet
import sevensegchars
import pyfirmata
import threading
import time


startup_sequence = {
12: '00000001', #shutdown mode, turn on
11: '00000111', #scan limit, digit 0 through 7 on
10: '00001111', #display intensity, set max 31/32
9: '00000000', #decode mode, no decode
15: '00000000', #display test, no data bit needed
10: '00000011', #display intensity, set to 7/32
}

class Display:
    __CS = None
    __DIN = None
    __CLK = None

    __board = None
    __ready = False
    __ID = None
    __amount = 1
    HIGH = 1
    LOW = 0

    target = 1
    characters = None

    def __init__(self, board, CS, DIN, CLK, amount=1):
        self.__CS = board.get_pin(('d:%s:o'%CS))
        self.__DIN = board.get_pin(('d:%s:o'%DIN))
        self.__CLK = board.get_pin(('d:%s:o'%CLK))
        self.__board = board
        self.__amount = amount
        self.characters = sevensegchars.Chars()

        self.initializeDisplay()

        print('[display.py] initiated with %s'%board)

    #sends the series of startup commands found in startup_sequence to the display
    def initializeDisplay(self):

        for key, value in startup_sequence.items():
            self.sendPacket(packet.Packet(key, value), 1)
            self.sendPacket(packet.Packet(key, value), 2)

        self.blankDisplay(2)
        self.blankDisplay(1)
        self.__ready = True


    #clears digit 0 through 7, writes a blank character to the MAX7219
    def blankDisplay(self, display=1):
        for i in range(8):
            self.sendPacket(packet.Packet(i+1, self.characters.getCharacter(' ')), display)


    def showString(self, string, display=1):
        string = string[::-1]
        decimalIdx = None
        for i in range(len(string)):
            if string[i] == '.':
                decimalIdx = i
                string = string[:i] + string[i+1:]
                break

        for i in range(len(string)):
            decimal = False
            if i == decimalIdx: decimal = True
            #print("sending %s to digit %s at dsp %s"%(string[i], i+1, display))
            self.sendPacket(packet.Packet(i+1, self.characters.getCharacter(string[i], decimal)), display)

    #sends a packet to the display by pulling ports low and HIGH
    #Chip Select(CS) goes low to allow wringin on Digital In(DIN)
    #Clock(CLK) goes low, we write the binary value(Low or high)
    #to DIN, then the MAX7218 reads this value on the rising edge
    #of the CLK pin. So when we set CLK to high DIN is read
    #when we've sent 16 bit we pull CS to high, this will set all
    #the internal registers on the MAX7219
    def sendPacket(self, packet, display=1):
        if display == 1: #left-pad with 16 NO-OP/zero bits.
            packet.zfill(32) #add 16 empty bits.
        if display == 2: #right pad with 16 NO-OP/zero bits.
            packet.ljust(32)

        self.__CS.write(self.LOW) #start taking in data
        for i in range(len(packet.packet)):
            self.__CLK.write(self.LOW)
            self.__DIN.write(int(packet.packet[i]))
            self.__CLK.write(self.HIGH)
        self.__CS.write(self.HIGH) #apply data in chip(adress and data)

    def ready(self):
        return self.__ready

    def setId(self, id):
        self.__ID = id

    #sets the brightness of the display, value range is 0 through 15.
    def brightness(self, value=0, display=1):
        if value not in range(0, 16):
            value = 0
        self.sendPacket(packet.Packet(10, str(bin(value))[2:].zfill(8)), display)


    #small animations, not really important but fun!
    def pulse(self, frequence):
        pass
