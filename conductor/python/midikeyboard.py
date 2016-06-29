import mido
mido.set_backend("mido.backends.pygame")

import serialcomm
import midiportnames

class Handler:
	def __init__(self):
		self.frives = [0, 0, 0, 0]

		inPort = list(set(mido.get_input_names())&set(midiportnames.ins))[0]
		self.inp = mido.open_input(inPort)

	def listen(self):
		print("Now listening for MIDI signals.")
		for message in self.inp:
			self.parseNote(message)

	def sortAndSend(self):
		self.frives = sorted(self.frives)
		for i in range(len(self.frives)):
			serialcomm.sendNote(self.frives[i], i)

	def parseNote(self, msg):
		note = msg.note - 46
		if note < 0 or note > 31: return
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
				serialcomm.sendNote(0, i)
				# Putting a return statement here could reduce lag but also might help clear out bugged notes

if __name__ == "__main__":
	h = Handler()
	h.listen()
