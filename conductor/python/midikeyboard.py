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

	if not state:
		frive = frives.index(note)
		serialcomm.sendNote(0, frive)
		frives[frive] = 0
	else:
		for i in range(len(frives)):
			if frives[i] != 0:
				serialcomm.sendNote(note, i)
				frives[i] = note

inPort = list(set(mido.get_input_names())&set(midiportnames.ins))[0]
inp = mido.open_input(inPort)

print "Ready to begin."
for message in inp:
	handleRaw(message)
inp.close()
