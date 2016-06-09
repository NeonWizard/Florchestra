import serial
from time import sleep

port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=None)

while 1:
	pin = raw_input("Send message: ").strip("\r\n")
	port.write(pin)
	sleep(0.1)