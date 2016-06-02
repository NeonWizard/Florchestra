from wiringpi import *

wiringPiSetupGpio()

# -------------
#   Functions
# -------------
def resetMotor(pinset):
	dirPin, stepPin = pinset

	digitalWrite(dirPin, 0)
	for _ in range(20):
		digitalWrite(stepPin, 1)
		digitalWrite(stepPin, 0)
		delay(1)

	digitalWrite(dirPin, 1)
	for _ in range(10):
		digitalWrite(stepPin, 1)
		digitalWrite(stepPin, 0)
		delay(1)

	delay(400)

def generateSong():
	return []

def play(tracks, pinsets):
	while True:
		pass


def main():
	# --------
	#   Pins
	# --------
	# (direction pin, stepping pin)

	f1_pins = (17, 18)
	f2_pins = (13, 26)
	for pin in f1_pins + f2_pins:
		pinMode(pin, 1) # Set each pin to output mode
	
	# -------------------
	#   Frive resetting
	# -------------------
	resetMotor(f1_pins)
	resetMotor(f2_pins)

if __name__ == "__main__":
	main()