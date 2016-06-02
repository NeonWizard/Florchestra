import pigpio, time

G1=17 # Direction
G2=18 # Step

pi = pigpio.pi()

pi.set_mode(G1, pigpio.OUTPUT)
pi.set_mode(G2, pigpio.OUTPUT)

frequencies = [
		[26163,27718,29366,31113,32963,34923,36999,39200,41530,44000,46616,49388], # Octave 4
		[52325,55437,58733,62225,65925,69846,73999,78399,83061,88000,93233,98777], # Octave 5
		[104650,110873,117466,124451,131851,139691,147998,156798,166122,176000,186466,197553], # Octave 6
		[209300,221746, 234932] # Octave 7
]

# Frequency is converted to floppy delay using the formula:
# 	314000/frequency
# so middle A = 314000 / 440 = 714
floppyConv = 31400000.0

# Convert the frequences to floppy delays ahead of time
floppyDelays = [[floppyConv/noteFreq*10 for noteFreq in octave] for octave in frequencies]
waves = []

pi.wave_clear() # clear any existing waveforms

for frequency in floppyDelays[2]:
	wave = []
	#                           ON   OFF  DELAY
	wave.append(pigpio.pulse(1<<G2, 0, frequency))
	wave.append(pigpio.pulse(1<<G1, 1<<G2, frequency))
	wave.append(pigpio.pulse(1<<G2, 0, frequency))
	wave.append(pigpio.pulse(0, (1<<G2)|(1<<G1), frequency))

	pi.wave_add_generic(wave)

	waves.append(pi.wave_create()) # create and save id

for wave in waves:
	pi.wave_send_repeat(wave)
	time.sleep(1)
	pi.wave_tx_stop() # stop waveform

pi.wave_clear() # clear all waveforms