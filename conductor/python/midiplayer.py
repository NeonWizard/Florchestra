import mido
mido.set_backend("mido.backends.pygame")
import midiportnames

currentNote = 0
onlyfrive = 0

def handleRaw(msg):
	global currentNote
	state = msg.type=="note_on" and msg.velocity > 0
	note = msg.note-46
	if note <= 0 or note > 31: return

	if state:
		serialcomm.sendNote(note, onlyfrive)
		currentNote = note
	elif currentNote == note:
		serialcomm.sendNote(0, onlyfrive)

outPort = list(set(mido.get_output_names())&set(midiportnames.outs))[0]
out = mido.open_output(outPort)

print "Ready to begin."
for message in mido.MidiFile("../../midis/test.mid").play():
	#handleRaw(message)
	out.send(message)
out.close()
