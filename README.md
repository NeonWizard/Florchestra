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
