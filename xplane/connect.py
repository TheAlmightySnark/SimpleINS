import struct
import socket
import threading


class Connect:

    #UDP connection variables
    sock = None
    xplaneIP = None
    xplanePort = None

    def __init__(self, xplaneIP, xplanePort):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.xplaneIP, self.xplanePort = xplaneIP, xplanePort
        print('[Connect.py] instantiated with %s'%self.sock)
    #the padstring is a little endian(<) 5 char(5s = 5 bytes), followed by however
    #many bytes there are in the given dataref. The command is always a fixed length(5)
    #we encode this all into a string of bytes that is then send off to X-plane.
    #data references can be read out in the simulator itself or found onlineself.
    #TODO: dref example line here
    #TODO: fully formated dref here
    def xplaneCommand(self, dref, dtype=b"CMND\x00"):
        padstring = '<5s{0:d}s'.format(len(dref)) # puts the length of dref in the padstring as a integer
        datareference = dref.encode() #convert string to bytes.
        message = struct.pack(padstring, dtype, dref) #pack according to the padstring arguments

        self.sendUDP(message)

    def xplaneDgram(self, dataref, datatype, datarate, id):
        padstring = '<5sii400s' #padding to 413 bytes according to the struct packing page(python)
        datatype = b"RREF\x00" #5 byte data type including null terminator
        datarate = 1 #send data 10 times a second
        dataId = id #ID X-plane will use to return data
        datareference = dataref.encode()

        UDPMessage = struct.pack(padstring, datatype, datarate, id, datareference)
        #print(UDPMessage)

        self.sendUDP(UDPMessage)


    def sendUDP(self, message):
        self.sock.sendto(message, (self.xplaneIP, self.xplanePort))

    #X-plane returns a whole lot of data in each single packet. This can be more then a
    #single DGRAM that we requisted.
    #this is done in 8 byte chunks, 4 byte int and a 4 byte floatself.
    #this is why we use the '<if' unpack.
    #Little endian, int for ID, and a float as value.
    def decodeData(self, source):
        #first 5 bytes tell us if it's X-plane data or not
        if source[0:5] != b'RREFO': return None

        decoded = {} #return data as ID/Value pair in decoded

        numValues = int( len(source[5:]) / 8 ) #how many values per 8 bytes

        idx = -1
        value = None
        #unpack the data in chuncks of 8 byte for as many values as there are supposed to be
        #<if = little endian, int for id of data, and a float for the data itself
        for i in range(0, numValues):
            idx, value = (struct.unpack("<if", source[5+8*i:5+8*(i+1)]))
            decoded[idx] = value
        return decoded
