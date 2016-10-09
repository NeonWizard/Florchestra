middleC = 440
twelthRoot = 2**(1/12.0)

def HZ2MS(hz):
	period = 1.0/hz

	ms = period * 1000000

	return int(round(ms))


for i in range(-31, 32):
	note = middleC * twelthRoot**i
	
	print str(HZ2MS(note))
