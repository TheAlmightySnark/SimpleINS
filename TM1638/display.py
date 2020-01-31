import packet
import sevensegchars
import pyfirmata
import threading
import time


startup_sequence = {
    0x8F, #set display to max brightness and turn it on
}

class Display:
    __CS = None
    __DIN = None
    __CLK = None

    __board = None
    __ready = False
    __ID = None

    HIGH = 1
    LOW = 0

    characters = None

    def __init__(self, board, CLK, DIO, STB):
        self.__CLK = board.get_pin(('d:%s:o'%CLK))
        self.__DIO = board.get_pin(('d:%s:o'%DIO))
        self.__STB = board.get_pin(('d:%s:o'%STB))

        self.__board = board

        self.characters = sevensegchars.Chars()

        self.initializeDisplay()

        print('[display.py] initiated with %s'%board)

    #sends the series of startup commands found in startup_sequence to the display
    def initializeDisplay(self):

        self.__ready = True
        self.__CLK.write(self.HIGH)
        self.__DIO.write(self.LOW)
        self.__STB.write(self.HIGH)


    #clear the display of the TM1638 using fixed adress mode
    def blankDisplay(self):
        self.__STB.write(self.LOW)
        for i in range(16):
            self.co

    def showString(self, string):
        pass
        
    def sendPacket(self, packet):
        for i in range(len(packet.packet)):
            self.__CLK(self.LOW)
            self.__DIN(packet.packet[i])
            self.__CLK(self.HIGH)

    def sendHex(self, data):
        self.send(packet.Packet(data).packet)

    def send(self, data):
        for i in range(len(data)):
            self.__CLK(self.LOW)
            self.__DIN(data[i])
            self.__CLK(self.HIGH)

    def ready(self):
        return self.__ready

    def setId(self, id):
        self.__ID = id

    #sets the brightness, value is between 1001000(0x8A) and 10001111(0x8F)
    def brightness(self, value=7):
        if(value > 0 and value < 8):
            0x8A + value
        else: return

    #small animations, not really important but fun!
    def pulse(self, frequence):
        pass
