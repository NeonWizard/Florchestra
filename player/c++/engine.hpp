#ifndef ENGINE_H
#define ENGINE_H

#include <stdint.h>

typedef uint8_t byte;

int setup();

void stepFrive_oscillating(byte frive);
void stepFrive_sliding(byte frive);
void STEPFRIVEF(byte frive);

void tick();
void serialLoop(int fd, unsigned int currentPeriod[]);

void resetAll(bool method);

void onExit(int s);

#endif // ENGINE_H