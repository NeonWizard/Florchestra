import time

import pigpio

square = []	

#                          ON       OFF    MICROS
square.append(pigpio.pulse(1<<4, 0,       4))
square.append(pigpio.pulse(0,       1<<4, 4))

pi = pigpio.pi() # connect to local Pi

pi.set_mode(GPIO, pigpio.OUTPUT)

pi.wave_add_generic(square)

wid = pi.wave_create()

if wid >= 0:
   pi.wave_send_repeat(wid)
   time.sleep(60)
   pi.wave_tx_stop()
   pi.wave_delete(wid)

pi.stop()