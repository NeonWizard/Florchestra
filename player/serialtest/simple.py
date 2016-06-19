import serial
from time import sleep

port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=None)

while 1:
	try:
		data_chunk = port.read()         
		sleep(0.1)         
		remaining_bytes = port.inWaiting() 
		data_chunk += port.read(remaining_bytes)
		print data_chunk
	except Exception, e:
		print str(e)
		pass