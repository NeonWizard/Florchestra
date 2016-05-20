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
byte pins[] = {
	// Dir, step
	{17, 18},
	{13, 26}
};
byte friveCount = sizeof(Frives); // Not sure if needed

// 3.5" frives have 80 tracks and 5.25" have 50
// Subtract two to add a bit of padding
byte MAX_POSITIONS[] = {78, 78};
byte currentPositions[] = {0, 0};
byte currentDirection[] = {0, 0};
// Current period is multiplied by resolution. So a note is held for currentPeriod[x] cycles
unsigned int currentPeriod[] = {
	0, 0
};
unsigned int currentTick[] = {
	0, 0
};

// =============
//   Functions
// =============
void setup()
{
	wiringPiSetup();
	for (byte i = 0; i < friveCount; i++)
	{
		pinMode(pins[i][0], OUTPUT); // Direction pin
		pinMode(pins[i][1], OUTPUT); // Step pin
	}
}

void tick()
{
	if (currentPeriod[0]>0)
	{
		currentTick[0]++;
		if (currentTick[0] >= currentPeriod[0])
		{
			stepFrive(0);
			currentTick[0]=0;
		}
	}
	if (currentPeriod[1]>0)
	{
		currentTick[1]++;
		if (currentTick[1] >= currentPeriod[1])
		{
			stepFrive(1);
			currentTick[1]=0;
		}
	}
	if (currentPeriod[2]>0)
	{
		currentTick[2]++;
		if (currentTick[2] >= currentPeriod[2])
		{
			stepFrive(2);
			currentTick[2]=0;
		}
	}
}

void stepFrive(byte frive)
// Frive is a number that counts up from 0 based on what position the pins are in the frive array
{
	if (currentPositions[frive] >= MAX_POSITIONS[frive])
	{
		currentDirection[frive][0] = 1;
		digitalWrite(pins[frive][0], 1);

		--currentPositions[frive]
	}
	else if (currentPositions[frive] <= 0)
	{
		currentDirection[frive][0] = 0;
		digitalWrite(pins[frive][0], 0)

		++currentPositions[frive]
	}

	digitalWrite(pins[frive][1], 1)
	digitalWrite(pins[frive][1], 0)
}

void resetAll()
{
	for (byte i = 0; i < friveCount; i++)
	{
		currentPeriod[i] = 0; // Stop playing any notes

		digitalWrite(pins[i][0], 1);
		for (byte pos=0; pos<MAX_POSITIONS[i]; pos++)
		{
			digitalWrite(pins[i][1], 1);
			digitalWrite(pins[i][1], 0);
			delayMicroseconds(10);
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
	resetAll();

	return 0;
}