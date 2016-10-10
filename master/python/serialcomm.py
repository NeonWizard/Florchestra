import serial

port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=None)

def infoToChar(note, frive):
	return chr((note << 3) | frive)

def sendChar(char):
	port.write(char)

def sendChars(note, frive):
	port.write(chr(note))
	port.write(chr(frive))

def sendNote(note, frive):
	sendChar(infoToChar(note, frive))
