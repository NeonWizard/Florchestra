import sys
import subprocess
import time

process = None
def init(sliding, b):
	global process
	command = ["../../player/c++/engine", sliding, b]
	process = subprocess.Popen(command, stdin=subprocess.PIPE)

def infoToChar(note, frive):
	return chr((note << 3) | frive)

def sendNote(note, frive):
	process.stdin.write(infoToChar(note, frive))
def sendNote2(note, frive):
	process.stdin.write(chr(note))
	process.stdin.write(chr(frive))

# process.stdin.write("hello world!".encode("utf-8"))
# process.communicate()
