import mido
mido.set_backend("mido.backends.pygame")

import serialcomm
import midiportnames

frives = [0, 0, 0]

def handleRaw(msg):
	global frives
	state = msg.type=="note_on" and msg.velocity > 0
	note = msg.note-46
	if note <= 0 or note > 31: return

	for i in range(len(frives)):
		frive = frives[i]
		if frive != 0: continue # If already playing a note

		if state:
			serialcomm.sendNote(note, frive)
			currentNote = note
		elif currentNote == note:
			serialcomm.sendNote(0, frive)

inPort = list(set(mido.get_input_names())&set(midiportnames.ins))[0]
inp = mido.open_input(inPort)

print "Ready to begin."
for message in inp:
	handleRaw(message)
inp.close()
