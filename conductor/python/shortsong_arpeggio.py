from time import sleep
from serialcomm import *

waittime = .2

try:
	for _ in range(2):
		# C minor arpeggio
		for _ in range(4):
			sendInfo(14, 0)
			sendInfo(17, 1)
			sleep(waittime)
			sendInfo(0, 0)
			sendInfo(0, 1)
			sendInfo(17, 0)
			sendInfo(21, 1)
			sleep(waittime)
			sendInfo(0, 0)
			sendInfo(0, 1)
			sendInfo(21, 0)
			sendInfo(14, 1)
			sleep(waittime)
			sendInfo(0, 0)
			sendInfo(0, 1)
			sendInfo(9, 0)
			sendInfo(21, 1)
			sleep(waittime)
			sendInfo(0, 0)
			sendInfo(0, 1)

		# B arpeggio
		for _ in range(4):
			sendInfo(19, 0)
			sendInfo(9, 1)
			sleep(waittime)
			sendInfo(0, 0)
			sendInfo(0, 1)
			sendInfo(16, 0)
			sendInfo(13, 1)
			sleep(waittime)
			sendInfo(0, 0)
			sendInfo(0, 1)
			sendInfo(13, 0)
			sendInfo(16, 1)
			sleep(waittime)
			sendInfo(0, 0)
			sendInfo(0, 1)
			sendInfo(9, 0)
			sendInfo(19, 1)
			sleep(waittime)
			sendInfo(0, 0)
			sendInfo(0, 1)

	# End chord
	sendInfo(14, 0)
	sendInfo(17, 1)
	sleep(waittime*4)
	sendInfo(0, 0)
	sendInfo(0, 1)

except:
	# Reset on early termination/crash
	sendInfo(0, 0)
	sendInfo(0, 1)
