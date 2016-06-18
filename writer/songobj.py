import random

class Song:
	def __init__(self, tempo):
		self.tempo = tempo

		self.tracks = {}

	def setTempo(self, tempo):
		self.tempo = tempo

	def addTrack(self, num):
		if num in self.tracks:
			return -1

		self.tracks[num] = []

	def getTracks(self):
		return self.tracks

	def removeTrack(self, num):
		if num not in self.tracks:
			return -1

		del self.tracks[num]

class Track:
	def __init__(self):
		# note = (note, octave, duration)
		self.stream = []

	def addNote(self, note, octave, duration):
		self.stream.append((note, octave, duration))

	def getNotes(self):
		return self.stream

	def removeNote(self, index):
		del self.stream[index]