import sys
import subprocess
import time

command = ["../player/c++/engine", "0", "1"]
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
