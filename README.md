# Serial communication
The pi that controls the notes to be played and sends them over the serial link will be called rpi1.

The pi that makes the frives play the notes will be rpi2.

rpi1 will need to send every note needed to rpi2 and rpi2 will need to handle them on time.

**Information that needs to be sent:**

* Note - 32 possible - 5 bits
* Which frive - Up to 8 - 3 bits

# Notes
| Index | Note | Frequency(Hz) | Duration(µs) |
|----|----|----|----|
| 0 | Zz | 0 | 0 |
| 1 | B2 | 123.47  | 8099 |
| 2 | C3 | 130.81  | 7645 |
| 3 | C#3/Db3  | 138.59  | 7216 |
| 4 | D3 | 146.83  | 6811 |
| 5 | D#3/Eb3  | 155.56  | 6428 |
| 6 | E3 | 164.81  | 6068 |
| 7 | F3 | 174.61  | 5727 |
| 8 | F#3/Gb3  | 185.00  | 5405 |
| 9 | G3 | 196.00  | 5102 |
| 10 | G#3/Ab3  | 207.65  | 4816 |
| 11 | A3 | 220.00  | 4545 |
| 12 | A#3/Bb3  | 233.08  | 4290 |
| 13 | B3 | 246.94  | 4050 |
| 14 | C4 | 261.63  | 3822 |
| 15 | C#4/Db4  | 277.18  | 3608 |
| 16 | D4 | 293.66  | 3405 |
| 17 | D#4/Eb4  | 311.13  | 3214 |
| 18 | E4 | 329.63  | 3034 |
| 19 | F4 | 349.23  | 2863 |
| 20 | F#4/Gb4  | 369.99  | 2703 |
| 21 | G4 | 392.00  | 2551 |
| 22 | G#4/Ab4  | 415.30  | 2408 |
| 23 | A4  | 440.00 | 2273 |
| 24 | A#4/Bb4  | 466.16 | 2145 |
| 25 | B4  | 493.88 | 2025 |
| 26 | C5  | 523.25 | 1911 |
| 27 | C#5/Db5  | 554.37 | 1820 |
| 28 | D5  | 587.33 | 1703 |
| 29 | D#5/Eb5  | 622.25 | 1607 |
| 30 | E5  | 659.25 | 1517 |
| 31 | F5  | 698.46 | 1432 |

# Ideas
Using PWM: https://www.raspberrypi.org/forums/viewtopic.php?f=63&t=113916<br>
Using wiringPi: http://wiringpi.com/reference/core-functions/
