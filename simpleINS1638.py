#standard modules
import pyfirmata
import threading
import queue
import time

#display imports
import TM1638.sevensegchars as sevensegchars
import TM1638.display as display

#xplane imports
import xplane.connect
import xplane.commands

#dcs imports
import dcs.connect
import dcs.commands

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

class SimpleINS:
    __board = None
    __display = None

    connection = None

    _display_string = ''
    __left = True

    def __init__(self, arduino=None, display_pins=[]):
        self.data = []

        if(arduino):
            self.__board = pyfirmata.Arduino(arduino)

        self.__display = display.Display(self.__board, display_pins[0], display_pins[1], display_pins[2])

        print("[simpleINS.py] initiated with %s and display %s"%(self.__board, self.__display))

        self.connection = xplane.connect.Connect('192.168.178.79', 49000)
        # self.connection = dcs.connect.Connect('192.168.178.79', 7778)
        print(self.connection)

        # DCS command test
        # self.connection.dcsCommand('UFC_CLEAR', 1)
        # time.sleep(0.5)
        # self.connection.dcsCommand('UFC_CLEAR', 0)

        for dgram in xplane.commands.datarefs:
            self.connection.xplane_dgram(dgram[0], xplane.commands.RREF, dgram[1], dgram[1])

        threading.Thread(target=self.recv_XP_UDP, args=()).start()
        threading.Thread(target=self.readKeys, args=()).start()
        # threading.Thread(target=self.readInput, args=()).start()

        # while True:
            #self.__display.showString(str(time.time())[2:10])

            # read = self.__display.readKeys()
            # if read: self.__display.showString('BTN %s'%(read))

            # time.sleep(1)

    def readInput(self):
        read = self.__display.readKeys()
        if read: self.__display.showString('BTN %s'%(read))

        threading.Thread(target=self.readInput, args=()).start()


    #listens to the default XP10/11 UDP protocol, send to specified IP on port
    # 49000, X-plane accepts commands on 490001 IIRC.
    def recv_XP_UDP(self):
        data, adress = self.connection.sock.recvfrom(1024)


        decoded = self.connection.decode_data(data)
        decoded_string = ''

        for key, value in decoded.items():
            decoded_string += (chr(int(value)))

        if self.__left: self._display_string = decoded_string[7:]
        if not self.__left: self._display_string = decoded_string[:7]

        threading.Thread(target=self.recv_XP_UDP, args=()).start()

    def readKeys(self):
        read = self.__display.readKeys()

        if read is not None: print(read)

        if read == 1:
            self.__left = not self.__left

        if read in xplane.commands.commandDict.keys():
            self.connection.xplane_cmd(xplane.commands.commandDict[read])

        if self._display_string != self.__display.displayed():
            self.__display.showString(self._display_string)

        threading.Thread(target=self.readKeys, args=()).start()

    #listens to the DCS-BIOS multicaster protocol by default on
    # IP/Port 239.255.50.10:5010
    def receiveDCSUDP(self):
        pass


#Launch application
if __name__ == "__main__":

    app = SimpleINS("/dev/ttyUSB0",[5,6,7])
