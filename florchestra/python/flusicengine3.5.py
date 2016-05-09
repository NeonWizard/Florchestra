# ===========================
#   Written by Wes Miravete
#      Started: 4/12/16
# ===========================
import sys
from os.path import isfile
from wiringpi import *

class Frive:
	maxPosition = 158
	def __init__(self, manager, dirPin, stepPin, num):
		self._frivemanager = manager

		self.num = num
		self.dirPin, self.stepPin = dirPin, stepPin

		self.curState = [0, 0] # Direction, step

	def resetMotor(self):
		digitalWrite(self.dirPin, 1)
		for _ in range(self.maxPosition/2):
			digitalWrite(self.stepPin, 1)
			digitalWrite(self.stepPin, 0)
			delay(5)
		digitalWrite(self.dirPin, 0)

		self.curPos = 0

	# def rest(self, length):
	# 	endTime = millis() + length
	# 	while millis() < endTime:
	# 		delay(5)

	def armTick_oscillate(self):
		digitalWrite(self.dirPin, self.curState[0])
		self.curState[0] = not self.curState[0]

		# Record new head position
		if self.curState[0] == 1:
			self.curPos -= 1
		else:
			self.curPos += 1

		digitalWrite(self.stepPin, 1)
		digitalWrite(self.stepPin, 0)

	def armTick_slide(self):

	# def playNote(self, note, octave, length):
	# 	# Find the note delay
	# 	noteDelay = self._frivemanager.findDelay(note, octave)

	# 	direction = 1

	# 	endTime = millis() + (length*7/8.0)
	# 	while millis() < endTime:
	# 		digitalWrite(self.dirPin, direction)
	# 		if direction == 0:
	# 			direction = 1
	# 		else:
	# 			direction = 0

	# 		digitalWrite(self.stepPin, 1)
	# 		digitalWrite(self.stepPin, 0)
	# 		delayMicroseconds(noteDelay)
	# 	self.rest(length/8.0)

class FriveManager:
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
	noteCycle = [[note, octave, .25] for octave in range(3) for note in octave1[:-1]]
	# Frequency is converted to floppy delay using the formula:
	# 	314000/frequency
	# so middle A = 314000 / 440 = 714
	floppyConv = 31400000.0

	# Convert the frequences to floppy delays ahead of time
	floppyDelays = [[floppyConv/noteFreq*10 for noteFreq in octave] for octave in frequencies]

	def __init__(self):
		wiringPiSetupGpio()

		self.availablePins = range(2, 27)
		self._curId = 0 # Keeping track of what floppy drive we're on

		self.curSong = None

		self.frives = []
		self.friveTime = [[0, 0, 0] for _ in range(8)] # Frequencies, current ticks, and current note duration for each of the 8 possible drives

	def getId(self):
		self._curId += 1
		return self._curId-1

	def findDelay(self, note, octave):
		try:
			ind = self.octave1.index(note)
		except:
			ind = self.octave2.index(note)
		return int(self.floppyDelays[octave][ind]*10)

	def setupFrive(self, pinNums):
		# pinNums should be a two-item tuple: (direction pin number, step pin number)
		dirPin, stepPin = pinNums
		if not (dirPin in self.availablePins and stepPin in self.availablePins):
			raise Exception("Pins aren't available")
		self.availablePins.remove(dirPin)
		self.availablePins.remove(stepPin)

		# Setup the pins
		pinMode(dirPin, 1)
		pinMode(stepPin, 1)

		frive = Frive(self, dirPin, stepPin, self.getId())
		frive.resetMotor()
		self.frives.append(frive)

	def tick(self, delta):
		for index, frive in enumerate(self.frives):
			if self.friveTime[index][0]>0: # If this frive is active
				self.friveTime[index][1] += delta # Total time elapsed since last pin toggle
				if self.friveTime[index][1] >= self.friveTime[index][0]:
					frive.togglePin()
					self.friveTime[index][1] = 0

	def changeNote(self, friveID, noteinfo):
		name, octave, length = noteinfo

		frequency = self.findDelay(name, octave)

		self.friveTime[friveId][0] = frequency
		self.friveTime[friveId][2] = length

	def start(self, song):
		lastmicros = micros()
		while True:
			# Determine delta
			m = micros()
			delta = m-lastmicros
			lastmicros = m

			# Tick with the determined delta
			self.tick(delta)

			# Read the song and make adjustments to floppy note delays
#			song.getNotes()


class Song:
	def __init__(self, filename):
		self.tracks = {}
		with open(filename, 'r') as openFile:
			for line in openFile:
				line = line.rstrip("\n")
				if line == "": continue
				if line[:5] == "Tempo":
					self.tempo = int(line.split(" ")[1])
					self.noteLen = 60000.0/self.tempo
				elif line[:5] == "Track":
					curtrack = int(line.split(" ")[1])
					self.tracks[curtrack] = []
				else:
					name, octave, length = line.split(" ")
					self.tracks[curtrack].append([name, int(octave), int(length)])

	def playTrack(self, track, friveid):
		for note in track:
			length = note[2] * self.noteLen
			if note[0] == "Zz":
				self._frivemanager.frives[friveid].rest(length)
			else:
				self._frivemanager.frives[friveid].playNote(note[0], note[1], length)

	def getNotes(self):
		return [i[0]]



def main(argv):
	if len(argv) != 2:
		raise Exception("Flusic engine takes one parameter!")

	if not isfile(argv[1]): raise Exception("File doesn't exist.")

	FM = FriveManager()
	FM.setupFrive((17, 18))
	FM.setupFrive((13, 26))

	FM.friveTime[0][0] = FM.floppyDelays[1][0]
	FM.friveTime[1][0] = FM.floppyDelays[2][0]

#	s = Song(argv[1])

	FM.start("swag")

	# if argv[1]=="song1":
	# 	playSong(song1, song1_tempo)
	# elif argv[1]=="song2":
	# 	playSong(song2, song2_tempo)
	# elif argv[1]=="song3":
	# 	playSong(song3, song3_tempo)
	# elif argv[1]=="song4":
	# 	playSong(song4, song4_tempo)
	# elif argv[1]=="cycle":
	# 	playSong(notecycle, 120)

if __name__ == "__main__":
	main(sys.argv)
