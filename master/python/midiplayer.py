import sys
import mido
mido.set_backend("mido.backends.pygame")

import serialcomm
import midiportnames

def getChannels(songfile):
	channels = []
	for message in mido.MidiFile(song):
		if isinstance(message, mido.MetaMessage): # Filter out meta messages
			continue

		if message.channel not in channels:
			channels.append(message.channel)

	return channels

def handleRaw(msg, tracklist):
	if isinstance(msg, mido.MetaMessage) or not hasattr(msg, "note"): # Filter out meta messages
		return

	# Get the channel it's on and convert to floppy track
	if msg.channel not in tracklist: return
	track = tracklist.index(msg.channel)
	# Determine if it's a NOTE_ON or NOTE_OFF
	state = msg.type=="note_on" and msg.velocity > 0
	# Convert the message to a floppy note
	note = msg.note-46+octavemod*12
	if note > 31:
		note = 20+((note-32)%12)
	if note <= 0:
		# Fix this later
		print "Jaspar"
		note = abs(note)%12

	# If it isn't playable by the florchestra
	#if note <= 0 or note > 31: return
	if note <= 0: return
	if note > 31: print note

	if state:
		serialcomm.sendNote(note, track)
	else:
		serialcomm.sendNote(0, track)

outPort = list(set(mido.get_output_names())&set(midiportnames.outs))[0]
out = mido.open_output(outPort)

if len(sys.argv) != 2:
	print "Invalid argument count!"
	sys.exit()

song ="../../midis/"+sys.argv[1]+".mid"

print "Getting track list..."
#tracklist = getChannels(song)

# Mayhem - The Sound
#tracklist = [-1, 0, 2, 4]
#tracklist = [-1, 2, 4, 0]
#octavemode = 2

# Eurythmics - Sweet dreams
#tracklist = [-1, 6, 2, 5]
#octavemod = 2

# TLT - FNAF
tracklist = [0, 3, 4, 6]
octavemod = 2

# Glaze - Beyond
#tracklist = [-1, 3, 4, 2]
#octavemod = 3

print tracklist
print "Ready to begin."
for message in mido.MidiFile(song).play():
	handleRaw(message, tracklist)
	#out.send(message)
out.close()
