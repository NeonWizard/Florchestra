// Some general information first of all:
// According to the frequencies page on musical notes, B8 is at a frequency of 7902.13 hz
// The arduino program I found has a resolution of 40 uS, or 25k Hz.
// ???
// So far I find that absolutely pointless and unachievable on a pi.
// So I'm going to set the base resolution at 120 uS (achievable?? maybe?? get ready for ultimate speed saving code)
// Also, if I on-off the step pin at the same time I don't have to toggle it and can double the resolution

// Notes:
// Try to use as small of types as you can for optimization purposes
// Avoid operations and conversions when possible
// (Frive == floppy drive)

// Temporary note:
// Toggling the pin might be neccessary because if the program runs too fast the writing might be overlooked

#include <stdint.h>
#include <iostream>
#include <wiringPi.h>

typedef uint8_t byte;

// =============================
//  Glooooobbbbaaallllss *hiss*
// =============================
// -----------
//  Constants
// -----------
const byte RESOLUTION = 120;

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
// Subtract two to add a bit of padding
byte MAX_POSITIONS[] = {74, 74};
byte currentPositions[] = {0, 0};
byte currentDirection[] = {0, 0};
// Current period is multiplied by resolution. So a note is held for currentPeriod[x] cycles
static unsigned int currentPeriod[2] = {0, 0};
unsigned int currentTick[2] = {0, 0};

// =============
//   Functions
// =============
void setup()
{
	wiringPiSetupGpio();
	for (byte i = 0; i < friveCount; i++)
	{
		pinMode(pins[i][0], OUTPUT); // Direction pin
		pinMode(pins[i][1], OUTPUT); // Step pin
	}
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
	delayMicroseconds(5);
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

void readSerial()
{
	// Read the serial pins hooked up to the other pi to set the notes
}

int main()
{
	setup();
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
	}

	return 0;
}