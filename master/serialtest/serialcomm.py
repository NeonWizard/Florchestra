import serial
from time import sleep

port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=None)

while 1:
	#data = chr(int(raw_input("Send a binary value: ").strip("\r\n"), 2))
	data = chr((int(raw_input("What note on the octave: ")) << 3) | int(raw_input("What frive (0-1): ")))
	port.write(data)
	sleep(0.1)