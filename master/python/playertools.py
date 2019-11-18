import mido

def getChannels(songfile):
	channels = []
	for message in songfile:
		if isinstance(message, mido.MetaMessage): # Filter out meta messages
			continue

		if message.channel not in channels:
			channels.append(message.channel)

	return channels

def readSongData(name):
	songdata = {}

	with open(name+".dat", 'r') as openFile:
		for line in openFile:
			line = line.rstrip("\n").rstrip("\r")
			data = line.split(":")
			songdata[data[0]] = data[1][1:] # [1:] is to remove the space in the beginning

	# Cleaning up the raw data
	songdata["TRANSPOSE"] = int(songdata["TRANSPOSE"])
	songdata["TRACK_KEY"] = [int(i) for i in songdata["TRACK_KEY"].replace(" ", "").split(",")]

	print(songdata)
	return songdata
