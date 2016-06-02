import pigpio

def wave(pi, gpio, hz, secs, on=1, offset=0):
   """
   Generate a hz cycles per second square wave on gpio for
   secs seconds.  The first transition is to level on at
   offset microseconds from the start.
   """
   micros_left = int(secs * 1000000)
   transitions = int(2 * hz * secs)
   micros = micros_left / transitions

   if (offset < 0) or (offset > micros):
      print("Illegal offset {} for hz {}".format(offset, hz))
      exit()

   pi.set_mode(gpio, pigpio.OUTPUT)

   wf = [] # Empty waveform.

   if offset:
      wf.append(pigpio.pulse(0, 0, offset))
      micros_left -= micros
      last_micros = micros - offset
      transitions -= 1

   for t in range(transitions, 0, -1):
      micros = micros_left / t
      if (t & 1) == (on & 1):
         wf.append(pigpio.pulse(0, 1<<gpio, micros))
      else:
         wf.append(pigpio.pulse(1<<gpio, 0, micros))
      micros_left -= micros

   if offset:
      if on:
         wf.append(pigpio.pulse(1<<gpio, 0, last_micros))
      else:
         wf.append(pigpio.pulse(0, 1<<gpio, last_micros))

   pi.wave_add_generic(wf)
   pi.wave_send_repeat(pi.wave_create())

pi = pigpio.pi()
pi.set_mode(17, pigpio.OUTPUT)
pi.wave_clear()

pi.write(17, 1)

wave(pi, 18, 260, 8)

pi.write(17, 0)

pi.stop()