from time import sleep
from serialcomm import *

waittime = .2

try:
	for _ in range(2):
		# C minor arpeggio
		for _ in range(4):
			sendInfo(14, 0)
			sleep(waittime)
			sendInfo(0, 0)
			sendInfo(17, 0)
			sleep(waittime)
			sendInfo(0, 0)
			sendInfo(21, 0)
			sleep(waittime)
			sendInfo(0, 0)
			sendInfo(9, 0)
			sleep(waittime)
			sendInfo(0, 0)

		# B arpeggio
		for _ in range(4):
			sendInfo(19, 0)
			sleep(waittime)
			sendInfo(0, 0)
			sendInfo(16, 0)
			sleep(waittime)
			sendInfo(0, 0)
			sendInfo(13, 0)
			sleep(waittime)
			sendInfo(0, 0)
			sendInfo(9, 0)
			sleep(waittime)
			sendInfo(0, 0)

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