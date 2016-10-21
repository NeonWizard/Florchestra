# The Florchestra
The florchestra is a project I've worked on over the last year. It's my attempt to make a set of musical floppy drives from scratch like you see on YouTube. There are two main components to the Florchestra: the engine (or player), and the conductor (or master). The engine harnesses 100% of one of a Raspberry Pi's CPU cores to send out rapid electrical oscillations to each floppy drives. The frequency of the oscillation determines what musical note can be heard. The conductor can read several different types of musical input, including MIDI files and real-time MIDI, which is sent to the engine to be played.

# Serial communication
The pi that controls the notes to be played and sends them over the serial link is called the master.

The pi that makes the frives play the notes is called the player.

The master chip sends every note needed to the player and the player handles them on time, delivering an electric oscillation to the appropriate floppy drive.

**Information sent with one byte communication:**

* Note - 32 possible - 5 bits
* Which frive - Up to 8 - 3 bits

**Information sent with two byte communication:**

* Note - 64 possible - 6 bits
* Which frive - Up to 8 - 3 bits
