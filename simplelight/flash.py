import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)

for _ in range(10):
	GPIO.output(18,GPIO.HIGH)

	time.sleep(.25)

	GPIO.output(18,GPIO.LOW)

	time.sleep(.25)
