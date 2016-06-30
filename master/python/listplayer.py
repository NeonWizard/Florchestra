from time import sleep, time
from songs import *
from serialcomm import *
import thread

# Octave with naturals and sharps (Zz = rest)
octave1 = ["Cn", "Cs", "Dn", "Ds", "En", "Fn", "Fs", "Gn", "Gs", "An", "As", "Bn"]
# Octave with flats and the remaining sharps
octave2 = ["Bs", "Df", "Dn2", "Ef", "En2", "Es", "Gf", "Gn2", "Af", "An2", "Bf", "Bn2"]

def findIndex(note):
	try:
		ind = octave1.index(note)
	except:
		ind = octave2.index(note)
	return ind

myepoch = int(round(time()*1000))

def millis():
	return int(round(time()*1000)) - myepoch

def playNote(note, frive, duration):
	duration = duration/1000.0
	sendNote(note, frive)
	sleep(duration*7/8.0)
	sendNote(0, frive)
	sleep(duration/8.0)

try:
	# for note in song4:
	# 	if note[0] == "Zz" or note[0] == "Zz2":
	# 		ind = 0
	# 	else:
	# 		ind = ((findIndex(note[0])+2)%13)+(note[1]-2)*12
	# 	print note[0]
	# 	sendNote(ind, 1)
	# 	delay = 60.0/song4_tempo*note[2]
	# 	sleep(delay*7/8.0)
	# 	sendNote(0, 1)
	# 	sleep(delay/8.0)
	
	playing = True

	tmp = millis()
	#  Index, lastplay, songlist
	friveinfo = [
		[0, int(tmp), song5],
		[0, int(tmp), song4]
	]

	basedelay = 60000.0/tempo

	while playing:
		tmp = millis()

		for i in range(len(friveinfo)):
			frive = friveinfo[i]

			if (tmp-frive[1]) >= frive[2][frive[0]][2]*basedelay:
				frive[0] += 1
				frive[1] = millis()
				note = frive[2][frive[0]][0]
				octave = frive[2][frive[0]][1]

				if note == "Zz" or note == "Zz2":
					ind = 0
				else:
					ind = ((findIndex(note)+2)%13)+(octave-2)*12

				thread.start_new_thread(playNote, (ind, i, basedelay*frive[2][frive[0]][2]))

except:
 	# Reset on early termination/crash
 	sendNote(0, 0)
 	sendNote(0, 1)
