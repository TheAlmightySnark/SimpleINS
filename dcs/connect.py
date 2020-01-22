import struct
import socket
import threading


class Connect:

    #UDP connection variables
    sock = None
    dcsIP = None
    dcsPort = None

    def __init__(self, dcsIP, dcsPort):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dcsIP, self.dcsPort = dcsIP, dcsPort
        print(dcsIP, dcsPort)
        print('[Connect.py] instantiated with %s'%self.sock)

    def dcsCommand(self, command, state):

        message = bytes("%s %s\n"%(command, state), 'utf-8')
        message = ('%s %s\n'%(command, state)).encode()
        print(message)
        self.sendUDP(message)

    def sendUDP(self, message):
        self.sock.sendto(message, (self.dcsIP, self.dcsPort))
