# ===========================
#   Written by Wes Miravete
#      Started: 4/12/16
# ===========================
import sys
from wiringpi import *
from songs import *

# Octave with naturals and sharps (Zz = rest)
octave1 = ["Cn", "Cs", "Dn", "Ds", "En", "Fn", "Fs", "Gn", "Gs", "An", "As", "Bn", "Zz"]
# Octave with flats and the remaining sharps
octave2 = ["Bs", "Df", "Dn2", "Ef", "En2", "Es", "Gf", "Gn2", "Af", "An2", "Bf", "Bn2", "Zz2"]

notecycle = [[note, octave, 1] for octave in range(4) for note in octave1[:-1]]

# Frequencies of notes in hundredths of Hertz
# Each set is an octave, C to B (including black notes)
frequencies = [
	[13081,13859,14683,15556,16481,17461,18500,19600,20765,22000,23308,24694], # Octave 3
	[26163,27718,29366,31113,32963,34923,36999,39200,41530,44000,46616,49388], # Octave 4
	[52325,55437,58733,62225,65925,69846,73999,78399,83061,88000,93233,98777], # Octave 5
	[104650,110873,117466,124451,131851,139691,147998,156798,166122,176000,186466,197553] # Octave 6
]

# Frequency is converted to floppy delay using the formula:
# 	314000/frequency
# so middle A = 314000 / 440 = 714
floppyConv = 31400000.0

# Convert the frequences to floppy delays ahead of time
floppyDelays = [[floppyConv/noteFreq for noteFreq in octave] for octave in frequencies]


# ------------------
#   Wiringpi setup
# ------------------
wiringPiSetupGpio()

# PI Pins
dirPin = 17 # Direction (floppy pin 18)
stepPin = 18 # Step (floppy pin 20)
# writePin = 24 # Write (floppy pin 22)

pinMode(stepPin, 1)
pinMode(dirPin, 1)
# pinMode(writePin, 1)

# -------------------
#    Functionality
# -------------------
def resetMotor():
	digitalWrite(dirPin, 0)
	for _ in range(10):
		digitalWrite(stepPin, 1)
		digitalWrite(stepPin, 0)
		delay(1)

	digitalWrite(dirPin, 1)
	for _ in range(5):
		digitalWrite(stepPin, 1)
		digitalWrite(stepPin, 0)
		delay(1)

	delay(400)

def playNote(note, octave, length):
	# Find the note delay
	try:
		ind = octave1.index(note)
	except:
		ind = octave2.index(note)
	noteDelay = int(floppyDelays[octave][ind]*10)

	direction = 1

	endTime = millis() + length
	while millis() < endTime:
		digitalWrite(dirPin, direction)
		if direction == 0:
			direction = 1
		else:
			direction = 0

		digitalWrite(stepPin, 1)
		digitalWrite(stepPin, 0)
		delayMicroseconds(noteDelay)

def rest(length):
	endTime = millis() + length
	while millis() < endTime:
		delay(5)

def playSong(song, tempo):
	noteLen = 60000.0/tempo

	print "Note | Octave | Value | Duration\n"

	for note in song:
		length = note[2] * noteLen
		if note[0] == "Zz":
			print "REST"
			rest(length)
		else:
			n_length = (length*7)/8.0 # So that the note isn't dragged out for the whole count
			r_length = length/8.0

			print note[0] + "\t" + str(note[1]) + "\t" + str(note[2]) + "\t%.2f" % n_length
			playNote(note[0], note[1], n_length)
			rest(r_length)

def main(argv):
	if len(argv) != 2:
		print("Flusic engine takes one parameter!")
		return 1

	print("Reseting motor")
	resetMotor()

	if argv[1]=="song1":
		playSong(song1, song1_tempo)
	elif argv[1]=="song2":
		playSong(song2, song2_tempo)
	elif argv[1]=="song3":
		playSong(song3, song3_tempo)
	elif argv[1]=="song4":
		playSong(song4, song4_tempo)
	elif argv[1]=="cycle":
		playSong(notecycle, 120)

if __name__ == "__main__":
	main(sys.argv)
