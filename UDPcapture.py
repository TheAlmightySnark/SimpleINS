import socket
import struct

MCAST_GRP = '239.255.50.10'
MCAST_PORT = 5010


#multicast test to capture DCS-BIOS
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((MCAST_GRP, MCAST_PORT))
mreq = struct.pack('4sl', socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

data, adress = sock.recvfrom(1024)

print("Data: [%s] \n Adress: %s"%(data, adress))
print("len(data): %s"%len(data))
print("len(data)/4: %s"%(len(data)-4))
#4 floats, UUUU, start of DCS-BIOS data stream
#1 unsigned int(H), start adress.
unpacked = struct.unpack("<4fHH%ss"%(len(data)/4-20), data)
# unpacked = struct.unpack("<4fHHs", data)
print(unpacked)


# 0000   01 00 5e 7f 32 0a c8 60 00 c2 35 8d 08 00 45 00   ..^.2.È`.Â5...E.
# 0010   00 52 39 e4 00 00 01 11 ea b5 c0 a8 b2 4f ef ff   .R9ä....êµÀ¨²Oïÿ
# 0020   32 0a c5 3b 13 92 00 3e 22 98 55 55 55 55 12 00   2.Å;...>".UUUU..
# 0030   02 00 20 20 00 04 02 00 4e 65 22 04 02 00 8b bc   ..  ....Ne"....¼
# 0040   fa 78 04 00 00 00 00 00 16 79 02 00 4e 15 3c 79   úx.......y..N.<y
# 0050   08 00 b2 7f 55 2b 07 08 c9 e1 fe ff 02 00 0d 00   ..².U+..Éáþÿ....
# 0020 55 55 55 55: FFFF, stream start identifier from DCS BIOS, 2 byte
# 0020 12 00 02 00 - 18. 2 byte start adress(18)
# 0030 20 20 00 04 - 32. 2 byte data length
