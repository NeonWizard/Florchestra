// ======================
//    Wesley Miravete
//         2016
// ======================

// Notes:
// Try to use as small of types as you can for optimization purposes
// Avoid operations and conversions when possible
// (Frive == floppy drive)
// Toggling the pin is neccessary because the writing from 0 to 1 to 0 again sometimes overlooks the 1, especially on a crappy frive.

// Todo:
// Serial communication

#include <stdint.h>
#include <cstdio>
#include <iostream>
#include <wiringPi.h>
#include <wiringSerial.h>
#include "notes.h"
#include <thread>

#define STEPFRIVEF stepFrive_oscillating // stepFrive_oscillating or stepFrive_sliding

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
// Double it because of toggling
byte MAX_POSITIONS[]    = {144, 144};
byte currentPositions[] = {0, 0};
byte currentDirection[] = {0, 0};
bool currentVoltage[]   = {0, 0};

unsigned int currentPeriod[2] = {0, 0}; // Current period is how long until another step
unsigned int currentTick[2]   = {0, 0}; // Counts how long has passed since the frive has been stepped

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
		std::cout << "Could not open serial device." << std::endl;
		return 1;
	}
	return fd;
}

void stepFrive_oscillating(byte frive)
// Frive is a number that counts up from 0 based on what position the pins are in the frive array
{
	currentDirection[frive] = currentVoltage[frive] ? !currentDirection[frive] : currentDirection[frive];
	digitalWrite(pins[frive][0], currentDirection[frive]);

	currentVoltage[frive] = !currentVoltage[frive];
	digitalWrite(pins[frive][1], currentVoltage[frive]);
}

void stepFrive_sliding(byte frive)
// Frive is a number that counts up from 0 based on what position the pins are in the frive array
{
	if (currentPositions[frive] >= MAX_POSITIONS[frive])
	{
		currentDirection[frive] = 1;
		digitalWrite(pins[frive][0], 1);
	}
	else if (currentPositions[frive] <= 0)
	{
		currentDirection[frive] = 0;
		digitalWrite(pins[frive][0], 0);
	}
	currentVoltage[frive] = !currentVoltage[frive];
	digitalWrite(pins[frive][1], currentVoltage[frive]);

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
			STEPFRIVEF(0);
			currentTick[0]=0;
		}
	}
	if (currentPeriod[1]>0)
	{
		currentTick[1] += delta;
		if (currentTick[1] >= currentPeriod[1])
		{
			STEPFRIVEF(1);
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

		digitalWrite(pins[i][0], 0);
		for (int pos=0; pos<MAX_POSITIONS[i]; pos++)
		{
			digitalWrite(pins[i][1], 1);
			delay(1);
			digitalWrite(pins[i][1], 0);
			delay(1);
		}

		digitalWrite(pins[i][0], 1);
		for (int pos=0; pos<MAX_POSITIONS[i]-10; pos++)
		{
			digitalWrite(pins[i][1], 1);
			delay(1);
			digitalWrite(pins[i][1], 0);
			delay(1);
		}
		digitalWrite(pins[i][0], 0);
	}
}

void serialLoop(int fd, unsigned int currentPeriod[])
{
	signed char data;
	while(1)
	{
		// Read the serial pins hooked up to the other pi to set the notes
		data = serialGetchar(fd);
		if (data==-1) continue; // timeout catcher

		currentPeriod[data & 0b00000111] = notes[(data >> 3) & 0b00011111];
		//std::cout << "Note: " << +byte((data >> 3) & 0b00011111) << std::endl;
		//std::cout << "Frive: " << +byte(data & 0b00000111) << std::endl;
	}
}

int main()
{
	std::cout << "Setting up..." << std::endl;
	int fd = setup();
	std::cout << "All set up!\n" << std::endl;

	std::cout << "Resetting frives..." << std::endl;
	resetAll();
	std::cout << "Everything reset.\n" << std::endl;

	std::cout << "Starting serial thread loop..." << std::endl;
	std::thread sl(serialLoop, fd, std::ref(currentPeriod));
	std::cout << "Serial loop running.\n" << std::endl;

	std::cout << "Ready to begin." << std::endl;

	while(1)
	{
		tick();
	}

	return 0;
}
