import TM1638.packet as packet
import TM1638.sevensegchars as sevensegchars
import pyfirmata
import threading
import time

import pyfirmata.util as util

startup_sequence = {
    0x8F, #set display to max brightness and turn it on
}

keys = {
    '00000000000000000000000000000000': 0, #no key
    '00100000000000000000000000000000': 1, #1
    '00000010000000000000000000000000': 2, #2
    '00000000001000000000000000000000': 3, #3
    '00000000000000100000000000000000': 4, #4
    '00000000000000000010000000000000': 5, #5
    '00000000000000000000001000000000': 6, #6
    '00000000000000000000000000100000': 7, #7
    '00000000000000000000000000000010': 8, #8
    '01000000000000000000000000000000': 9, #9
    '00000100000000000000000000000000': 10, #10
    '00000000010000000000000000000000': 11, #11
    '00000000000001000000000000000000': 12, #12
    '00000000000000000100000000000000': 13, #13
    '00000000000000000000010000000000': 14, #14
    '00000000000000000000000001000000': 15, #15
    '00000000000000000000000000000100': 16, #16
}

class Display:
    __DIO = None
    __CLK = None
    __STB = None

    __board = None
    __pins = []
    __ready = False
    __ID = None

    __displayed = None
    __prevread = ''

    HIGH = 1
    LOW = 0

    characters = None


    def __init__(self, board, DIO, CLK, STB):
        self.__DIO = board.get_pin(('d:%s:o'%DIO))
        self.__CLK = board.get_pin(('d:%s:o'%CLK))
        self.__STB = board.get_pin(('d:%s:o'%STB))

        self.__board = board
        self.__pins = [DIO, CLK, STB]

        self.__prevread = '0'

        self.characters = sevensegchars.Chars()

        self.initializeDisplay()

        print('[display.py] initiated with %s'%board)

    #sends the series of startup commands found in startup_sequence to the display
    def initializeDisplay(self):
        self.sendCommand(0x8F) #turn on display, maximum brightness
        self.__CLK.write(self.HIGH)
        self.__DIO.write(self.LOW)
        self.__STB.write(self.HIGH)

        self.blankDisplay()

        #update the board without overflowing the serial connection.
        thread =  util.Iterator(self.__board)
        thread.start()

        self.__ready = True

    #clear the display of the TM1638 using fixed adress mode. loop through the 16 adresses
    def blankDisplay(self):
        self.showString('        ')

    #use fixed adress mode(0x40) to set a full string from left to right.
    def showString(self, string):

        if string == self.__displayed: return
        #pad or limit string to 8 characters minimum.
        if len(string) < 8:
            string = string.ljust(8, ' ')
        if len(string) > 8:
            string = string[:8]

        coded = self.characters.stringToBin(string)

        adjusted = []
        for i in range(len(coded)):
            new = ''
            for j in range(8): #only accept 2 byte strings max
                new += coded[j][i]
            adjusted.append(new)

        #start sending characters to the display in fixed adress mode
        self.sendCommand(0x40)

        #send 16 digits of data
        self.__STB.write(self.LOW)
        self.send(packet.Packet(0xc0).packet) #starting adress
        for cmd in adjusted:
            self.send(cmd)
            self.send(cmd)
        self.__STB.write(self.HIGH)

        self.__displayed = string

        #small pause after displaying something before going back to reading keys.
        time.sleep(0.1)
        
    #set a single digit to input char at position idx
    def setChar(self, char, idx):
        pass

    def sendCommand(self, data):
        self.__STB.write(self.LOW)
        self.send(packet.Packet(data).packet)
        self.__STB.write(self.HIGH)

    def sendHex(self, val):
        self.send(packet.Packet(val).packet)

    #clock data out, invert data order to clock our MSB first.
    def send(self, data):
        data = data[::-1]
        for i in range(len(data)):
            self.__CLK.write(self.LOW)
            self.__DIO.write(int(data[i]))
            self.__CLK.write(self.HIGH)

    def ready(self):
        return self.__ready

    def setId(self, id):
        self.__ID = id

    def busy(self):
        return self._busy

    def readKeys(self):
        read = ''
        self.__STB.write(self.LOW)
        self.sendHex(0x42) #send read data command

        self.__DIO.mode = pyfirmata.INPUT

        #read 4 byte of input data
        for i in range(8 * 4):
            self.__CLK.write(self.LOW)
            time.sleep(0.01) #slight delay after going low to avoid noise.
            read += str(int(self.__DIO.read()))
            self.__CLK.write(self.HIGH)

        self.__STB.write(self.HIGH)

        self.__DIO.mode = pyfirmata.OUTPUT

        # print("prevread[%s] read[%s]"%(hex(int(self.__prevread)), hex(int(read))))

        if read == self.__prevread:
            self.__prevread = read
            return None
        else:
            self.__prevread = read
            return keys[read]

    #sets the brightness, value is between 1001000(0x8A) and 10001111(0x8F)
    def brightness(self, value=7):
        if(value > 0 and value < 8):
            self.sendCommand(0x8A + value)
        else: return

    def displayed(self):
        return self.__displayed

    #small animations, not really important but fun!
    def pulse(self, frequence):
        pass
