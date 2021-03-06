#ifndef ENGINE_H
#define ENGINE_H

#include <stdint.h>

typedef uint8_t byte;

void setup();

void stepFrive_oscillating(byte frive);
void stepFrive_sliding(byte frive);
void STEPFRIVEF(byte frive);

void tick();
void commLoop(unsigned int currentPeriod[], const int notes[]);
void commLoop2(unsigned int currentPeriod[], const int notes[]);

void resetAll(bool method);

void onExit(int s);

#endif // ENGINE_H
