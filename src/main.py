import socket
import struct

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('127.0.0.1', 4444))

while True:
    data = sock.recv(256)

    outgauge = struct.unpack('I4sHBBfffffffIIfff16s16sxxxx', data)

    print("RPM: ", str(outgauge[6]))
    print("Speed: ", str(outgauge[5]))

sock.close()