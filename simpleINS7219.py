#standard modules
import pyfirmata
import threading
import time

#display imports
import MAX7219.sevensegchars as sevensegchars
import MAX7219.display as display

#xplane imports
import xplane.connect
import xplane.commands

#dcs imports
import dcs.connect
import dcs.commands

class SimpleINS(Object):
    __board = None
    __displays = []

    connection = None

    #keep track of what we are currently displaying on either screen
    display_left = None
    display_right = None

    def __init__(self, arduino=None, displays=None):
        self.data = []

        if(arduino):
            self.__board = pyfirmata.Arduino(arduino)

        if(displays):
            for idx, dp in enumerate(displays):
                new_display = display.Display(self.__board, dp[0], dp[1], dp[2], 2)
                new_display.set_ID(idx+1)
                self.__displays.append(new_display)

        print("[simpleINS.py] initiated with %s and displays %s"%(self.__board, self.__displays))

        for display_object in self.__displays:
            display_object.showString('XPLANE ', display=1)
            display_object.showString(' DCS   ', display=2)

        #self.connection = xplane.connect.Connect('192.168.178.79', 49000)
        self.connection = dcs.connect.Connect('192.168.178.79', 7778)
        print(self.connection)

        self.connection.dcsCommand('UFC_CLEAR', 1)
        time.sleep(0.5)
        self.connection.dcsCommand('UFC_CLEAR', 0)
        #for dgram in xplane.commands.datarefs:
        #    self.connection.xplane_dgram(dgram[0], xplane.commands.RREF, dgram[1], dgram[1])

        #threading.Thread(target=self.recv_XP_UDP, args=()).start()
        print("active threads: ", threading.active_count)

    #listens to the default XP10/11 UDP protocol, send to specified IP on port
    # 49000, X-plane accepts commands on 490001 IIRC.
    def recv_XP_UDP(self):
        data, adress = self.connection.sock.recvfrom(1024)

        decoded = self.connection.decode_data(data)
        decoded_string = ''
        for key, value in decoded.items():
            decoded_string += (chr(int(value)))


        self.__displays[0].showString(decoded_string[0:7], 2)
        self.__displays[0].showString(decoded_string[7:], 1)

        threading.Thread(target=self.recv_XP_UDP, args=()).start()

    #listens to the DCS-BIOS multicaster protocol by default on
    # IP/Port 239.255.50.10:5010
    def recv_DCS_UDP(self):
        pass


#Launch application
if __name__ == "__main__":

    app = SimpleINS("/dev/ttyUSB0",[[10,8,9],])
