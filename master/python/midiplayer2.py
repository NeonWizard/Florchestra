import sys
import mido
mido.set_backend("mido.backends.pygame")

import serialcomm
import playertools

def handleRaw(msg, sd): # sd = song data
	if isinstance(msg, mido.MetaMessage) or not hasattr(msg, "note"): # Filter out meta messages
		return

	# Get the channel it's on and convert to floppy track
	if msg.channel not in sd["TRACK_KEY"]: return
	track = sd["TRACK_KEY"].index(msg.channel)

	# Determine if it's a NOTE_ON or NOTE_OFF
	state = msg.type=="note_on" and msg.velocity > 0

	# Convert the message to a floppy note then transpose
	note = msg.note-55
	note += sd["TRANSPOSE"] # Transposition

	# Capping on either side of the range
	if note > 63:
		note = 52+((note-64)%12)
	if note <= 0:
		# Fix this later
		note = note%12

	# If it isn't playable by the florchestra
	#if note <= 0 or note > 31: return
	if note <= 0: return
	if note > 63:
		print note
		return

	if state:
		serialcomm.sendNote2(note, track)
	else:
		serialcomm.sendNote2(0, track)

if len(sys.argv) != 2:
	print "Invalid argument count!"
	sys.exit()

print "Getting song info..."
songdata = playertools.readSongData("../songs/"+sys.argv[1])
print "Reading MIDI file into memory..."
songfile = mido.MidiFile("../songs/"+songdata["MIDI_NAME"]+".mid")

print "Ready to begin."

for message in songfile.play():
	handleRaw(message, songdata)

