// Notes:
// Try to use as small of types as you can for optimization purposes
// Avoid operations and conversions when possible
// (Frive == floppy drive)

// Temporary note:
// Toggling the pin might be neccessary because if the program runs too fast the writing might be overlooked

// Todo:
// Add duration to notes

#include <stdint.h>
#include <iostream>
#include <wiringPi.h>
#include <wiringSerial.h>

typedef uint8_t byte;

// =========
//  Globals
// =========
// ------------------------------
//  Individual frive information
// ------------------------------
// The array positions are numbered based on position in the Frive array
byte pins[2][2] = {
	// Dir, step
	{17, 18},
	{13, 26}
};
byte friveCount = 2;

// 3.5" frives have 80 tracks and 5.25" have 50
// Subtract 8 to add a bit of padding
byte MAX_POSITIONS[]    = {72, 72};
byte currentPositions[] = {0, 0};
byte currentDirection[] = {0, 0};

unsigned int currentPeriod[2]   = {0, 0}; // Current period is how long until another step
unsigned int currentDuration[2] = {0, 0}; // Current duration is how long the note is held
unsigned int currentTick[2]     = {0, 0}; // Counts how long has passed since the frive has been stepped

// =============
//   Functions
// =============
int setup()
{
	wiringPiSetupGpio();
	for (byte i = 0; i < friveCount; i++)
	{
		pinMode(pins[i][0], OUTPUT); // Direction pin
		pinMode(pins[i][1], OUTPUT); // Step pin
	}

	// Starting the serial device and returning file descriptor
	int fd;
	if ((fd = serialOpen ("/dev/ttyAMA0", 115200)) < 0)
	{
		fprintf (stderr, "Unable to open serial device: %s\n", strerror (errno)) ;
		return 1;
	}
	return fd;
}

void stepFrive(byte frive)
// Frive is a number that counts up from 0 based on what position the pins are in the frive array
{
	if (currentPositions[frive] >= MAX_POSITIONS[frive])
	{
		currentDirection[frive] = 1;
		digitalWrite(pins[frive][0], 1);
		std::cout << "Switched 1" << std::endl;
	}
	else if (currentPositions[frive] <= 0)
	{
		currentDirection[frive] = 0;
		digitalWrite(pins[frive][0], 0);
		std::cout << "Switched 0" << std::endl;
	}

	digitalWrite(pins[frive][1], 1);
	digitalWrite(pins[frive][1], 0);

	if (currentDirection[frive] == 1)
	{
		currentPositions[frive] -= 1;
	}
	else
	{
		currentPositions[frive] += 1;
	}

}

void tick()
{
	static unsigned int time = 0;
	static unsigned int lasttime = 0;
	time = micros();
	unsigned int delta = time-lasttime;
	lasttime = time;
	if (currentPeriod[0]>0)
	{
		currentTick[0] += delta;
		if (currentTick[0] >= currentPeriod[0])
		{
			stepFrive(0);
			currentTick[0]=0;
		}
	}
	if (currentPeriod[1]>0)
	{
		currentTick[1] += delta;
		if (currentTick[1] >= currentPeriod[1])
		{
			stepFrive(1);
			currentTick[1]=0;
		}
	}
	delayMicroseconds(5); // Prevent the loop from going too fast and giving itself a bad time
	// if (currentPeriod[2]>0)
	// {
	// 	currentTick[2]++;
	// 	if (currentTick[2] >= currentPeriod[2])
	// 	{
	// 		stepFrive(2);
	// 		currentTick[2]=0;
	// 	}
	// }
}

void resetAll()
{
	for (byte i = 0; i < friveCount; i++)
	{
		currentPeriod[i] = 0; // Stop playing any notes

		digitalWrite(pins[i][0], 1);
		for (int pos=0; pos<MAX_POSITIONS[i]; pos++)
		{
			digitalWrite(pins[i][1], 1);
			digitalWrite(pins[i][1], 0);
			delay(1);
		}
	}
}

void readSerial(int fd)
{
	// Read the serial pins hooked up to the other pi to set the notes
	if (int toRead = serialDataAvail(fd) > 0)
	{
		for (int i=0; i<toRead; i++)
		{
			std::cout << serialGetchar(fd) << std::endl;
		}
	}
}

int main()
{
	int fd = setup();
	std::cout << "All set up!" << std::endl;
	resetAll();
	delay(2000);
	std::cout << "Everything reset." << std::endl;

	std::cout << "Setting the note frequencies...\n";
	currentPeriod[0] = 10000;
	currentPeriod[1] = 10000;
	std::cout << "Done." << std::endl;

	while(1)
	{
		tick();
		// readSerial(fd);
	}

	return 0;
}