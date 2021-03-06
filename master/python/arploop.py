from time import sleep
from serialcomm import *

waittime = .2

try:
	while True:
		# C minor arpeggio
		for _ in range(4):
			sendNote(14, 0)
			sendNote(17, 1)
			sleep(waittime)
			sendNote(17, 0)
			sendNote(21, 1)
			sleep(waittime)
			sendNote(21, 0)
			sendNote(14, 1)
			sleep(waittime)
			sendNote(9, 0)
			sendNote(21, 1)
			sleep(waittime)

		# B arpeggio
		for _ in range(4):
			sendNote(13, 0)
			sendNote(16, 1)
			sleep(waittime)
			sendNote(16, 0)
			sendNote(19, 1)
			sleep(waittime)
			sendNote(19, 0)
			sendNote(13, 1)
			sleep(waittime)
			sendNote(9, 0)
			sendNote(19, 1)
			sleep(waittime)

	# End chord
	sendNote(14, 0)
	sendNote(17, 1)
	sleep(waittime*4)
	sendNote(0, 0)
	sendNote(0, 1)

except:
	# Reset on early termination/crash
	sendNote(0, 0)
	sendNote(0, 1)
