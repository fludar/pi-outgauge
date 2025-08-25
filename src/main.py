import socket
import struct
import pigpio
import subprocess
import time 

PORT = 4444
maxrpm = 5000
maxspeed = 56 #m/s
servopins = [17, 18]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', PORT))

print("[Server] Started on port ", PORT)

try:
    subprocess.check_output(["pgrep", "pigpiod"])
except subprocess.CalledProcessError:
    print("[Daemon] PIGPIOD isn't running. Trying to start it now.")
    subprocess.Popen(["sudo", "pigpiod"])
    time.sleep(1)

def value_to_pwm(value, maxvalue, inverted=False):
    return max(500, min(2500, (2500 - value * 2000 / maxvalue) if inverted else (500 + value * 2000 / maxvalue))) #this ensures the value is between 500 and 2500 us

gpio = pigpio.pi()

try:
    while True:
        data = sock.recv(256)
        outgauge = struct.unpack('I4sHBBfffffffIIfff16s16sxxxx', data)
        if outgauge[6] > maxrpm:
            maxrpm = outgauge[6]
        if outgauge[5] > maxspeed:
            maxspeed = outgauge[5]
        gpio.set_servo_pulsewidth(servopins[0], value_to_pwm(outgauge[5], maxspeed, False)) 
        gpio.set_servo_pulsewidth(servopins[1], value_to_pwm(outgauge[6], maxrpm, False))
finally:
    sock.close()
    gpio.stop()