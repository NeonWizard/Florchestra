import sys
import mido
mido.set_backend("mido.backends.pygame")

# import serialcomm as comm
import enginecomm as comm
import playertools

class Handler:
	def __init__(self):
		self.frives = [0, 0, 0, 0, 0, 0]

		self.resetFrives()

	def resetFrives(self):
		for i in range(len(self.frives)):
			comm.sendNote2(0, i)
			self.frives[i] = 0


	def sortAndSend(self):
		self.frives = sorted(self.frives, reverse=True)
		for i in range(len(self.frives)):
			comm.sendNote2(self.frives[i], i)

	def parseNote(self, msg, sd):
		if isinstance(msg, mido.MetaMessage) or not hasattr(msg, "note"): # Filter out meta messages
			return

		note = msg.note - 55
		note += sd["TRANSPOSE"]

		while note > 41:
			note -= 12
		while note <= 0:
			note += 12

		if msg.type == "note_on" and msg.velocity > 0:
			self.playNote(note)
		else:
			self.stopNote(note)

	def playNote(self, note):
		for i in range(len(self.frives)):
			if self.frives[i]: continue # If this frive is already playing a note

			self.frives[i] = note # Document the note playing
			self.sortAndSend()
			return

	def stopNote(self, note):
		for i in range(len(self.frives)):
			if self.frives[i] == note:
				self.frives[i] = 0
				comm.sendNote2(0, i)
				# Putting a return statement here could reduce lag but also might help clear out bugged notes


if len(sys.argv) != 2:
	print("Invalid argument count!")
	sys.exit()

print("Getting song info...")
songdata = playertools.readSongData("../songs/"+sys.argv[1])
print("Reading MIDI file into memory...")
songfile = mido.MidiFile("../songs/"+songdata["MIDI_NAME"]+".mid")

h = Handler()

print("Ready to begin.")

for message in songfile.play():
	h.parseNote(message, songdata)
