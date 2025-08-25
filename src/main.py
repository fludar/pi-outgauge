import socket
import struct

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('127.0.0.1', 4444))

def value_to_pwm(value, maxvalue, inverted=False):
    return max(500, min(2500, (2500 - value * 2000 / maxvalue) if inverted else (500 + value * 2000 / maxvalue))) #this ensures the value is between 500 and 2500 us

maxrpm = 5000
maxspeed = 56 #m/s
while True:
    data = sock.recv(256)

    outgauge = struct.unpack('I4sHBBfffffffIIfff16s16sxxxx', data)
    if outgauge[6] > maxrpm:
        maxrpm = outgauge[6]
    if outgauge[5] > maxspeed:
        maxspeed = outgauge[5]

    print("RPM: ", outgauge[6])
    print("Speed: ", str(outgauge[5]))
    print(value_to_pwm(outgauge[6], maxrpm, True))

sock.close()