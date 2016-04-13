# ===========================
#   Written by Wes Miravete
#      Started: 4/12/16
# ===========================
import RPi.GPIO as GPIO
import time

startTime = int(round(time.time()*1000))
def millis():
	return int(round(time.time()*1000))-startTime

# Octave with naturals and sharps (Zz = rest)
octave1 = ["Cn", "Cs", "Dn", "Ds", "En", "Fn", "Fs", "Gn", "Gs", "An", "As", "Bn", "Zz"]
# Octave with flats and the remaining sharps
octave2 = ["Bs", "Df", "Dn2", "Ef", "En2", "Es", "Gf", "Gn2", "Af", "An2", "Bf", "Bn2", "Zz2"]

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
floppyDelays = [[round(floppyConv/noteFreq) for noteFreq in octave] for octave in frequencies]



# ----------
#   Songs
# ----------
# Song format: Note, octave, length

# C major scale
song1_tempo = 220
song1 = [
	["Cn", 2, 1],
	["Dn", 2, 1],
	["En", 2, 1],
	["Fn", 2, 1],
	["Gn", 2, 1],
	["An", 2, 1],
	["Bn", 2, 1],
	["Cn", 3, 1],
	["Bn", 2, 1],
	["An", 2, 1],
	["Gn", 2, 1],
	["Fn", 2, 1],
	["En", 2, 1],
	["Dn", 2, 1],
	["Cn", 2, 1]
]

# --------------
#   GPIO Setup
# --------------
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# PI Pins
stepPin = 18 # Step (floppy pin 20)
dirPin = 23 # Direction (floppy pin 18)
writePin = 24 # Write (floppy pin 22)

GPIO.setup(stepPin, GPIO.OUT)
GPIO.setup(dirPin, GPIO.OUT)
GPIO.setup(writePin, GPIO.OUT)

# -------------------
#    Functionality
# -------------------

# Easy of pin toggling, gets painstaking to type the entire thing :P
def pOn(num):
	GPIO.output(num, GPIO.HIGH)
	time.sleep(.005)
def pOff(num):
	GPIO.output(num, GPIO.LOW)
	time.sleep(.005)

def resetMotor():
	# To reset, move all the way in one direction then halfway back the other
	pOff(dirPin)
	for _ in range(75): # 75 tends to be the magic number for the distance of the drive
		pOn(stepPin)
		pOff(stepPin)
	pOn(dirPin)
	for _ in range(37):
		pOn(stepPin)
		pOff(stepPin)
	time.sleep(.5)

def playNote(note, octave, length):
	# Find the note delay
	try:
		ind = octave1.index(note)
	except:
		ind = octave2.index(note)
	noteDelay = floppyDelays[octave][ind]*10

	direction = 1

	endTime = millis() + length
	while millis() < endTime:
		if direction == 0:
			pOff(dirPin)
			direction = 1
		else:
			pOn(dirPin)
			direction = 0
		pOn(stepPin)
		pOff(stepPin)
		time.sleep(noteDelay/1000.0/1000.0) # Convert to microseconds lel

def rest(length):
	endTime = millis() + length
	while millis() < endTime:
		time.sleep(0.005)

def playSong(song, tempo):
	noteLen = 60000.0/tempo

	for note in song:
		length = note[2] * noteLen
		if note == "Zz":
			rest(length)
		else:
			playNote(note[0], note[1], length)

def main():
	print("Reseting motor")
	#resetMotor()

	while True:
		print("Playing the C Major Scale")
		playSong(song1, song1_tempo)

if __name__ == "__main__":
	main()
