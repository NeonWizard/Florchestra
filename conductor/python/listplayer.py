from time import sleep
from serialcomm import *

try:
	pass

except:
	# Reset on early termination/crash
	sendInfo(0, 0)
	sendInfo(0, 1)