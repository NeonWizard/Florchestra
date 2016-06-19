import mido
mido.set_backend("mido.backends.pygame")

import serialcomm

# print mido.get_output_names()
# out = mido.open_output("Microsoft MIDI Mapper")

def handleRaw(msg):
	state = msg.type=="note_on" and msg.velocity > 0
	note = msg.note-46
	print str(note) + " - " + str(state)
	serialcomm.sendNote(note, 0)

with mido.open_input("USB2.0-MIDI") as inp:
	for message in inp:
		handleRaw(message)