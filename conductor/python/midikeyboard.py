import mido
mido.set_backend("mido.backends.pygame")

import serialcomm

# print mido.get_input_names()
# out = mido.open_output("Microsoft MIDI Mapper")

currentNote = 0

def handleRaw(msg):
	global currentNote
	state = msg.type=="note_on" and msg.velocity > 0
	note = msg.note-46
	if note <= 0 or note > 31: return

	if state:
		serialcomm.sendNote(note, 0)
		currentNote = note
	elif currentNote == note:
		serialcomm.sendNote(0, 0)

		
inp = mido.open_input(mido.get_input_names()[1])
print "Ready to begin."
for message in inp:
	handleRaw(message)
inp.close()
