import struct
import socket
import pyfirmata #make sure standardFirmataPlus sketch is uploaded to the arduino
import time

board = pyfirmata.Arduino("/dev/ttyUSB0")

DIO = board.get_pin('d:5:o')
CLK = board.get_pin('d:6:o')
STB = board.get_pin('d:7:o')

LOW = 0
HIGH = 1


CLK.write(HIGH)
DIO.write(LOW)
STB.write(HIGH)

def send(cmd):
    cmd = cmd[::-1]

    for i in range(len(cmd)):
        CLK.write(LOW)
        DIO.write(int(cmd[i]))
        CLK.write(HIGH)

def blankDisplay():
    for i in range(16 * 8):
        CLK.write(LOW)
        DIO.write(LOW)
        CLK.write(HIGH)


def sendCommand(cmd):
    STB.write(LOW)
    sendHex(cmd)
    STB.write(HIGH)

def sendHex(val):
    binary = bin(val)[2:].zfill(8)
    print('%s : [%s]'%(val, binary))
    send(binary)

sendCommand(0x8a) #turn on display
sendCommand(0x40) #auto adress increment mode
STB.write(LOW)
sendHex(0xc0) #send starting adress
vals = ['11101110', #a through G, without decimal points
        '11111110',
        '10011100',
        '11111100',
        '10011110',
        '10001110',
        '10111110',
        '01101110',
]

adjusted = []

#adjust vals as if they were a column.
for i in range(8):
    new = ''
    for j in range(8):
        new += vals[j][i]
    adjusted.append(new)
    print(new)



for i in range(8):
    send(adjusted[i])
    send(adjusted[i])

time.sleep(5)
#turning display on and off works fine...
STB.write(HIGH)
sendCommand(0x8a)
time.sleep(1)
sendCommand(0x80)
time.sleep(1)

#try and blank the display. works fine...
#turn on, set mode, set adress
sendCommand(0x8a)
time.sleep(1)
sendCommand(0x40)
sendCommand(0xc0)
STB.write(LOW)
blankDisplay()
STB.write(HIGH)
