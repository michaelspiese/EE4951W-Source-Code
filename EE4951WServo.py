#from gpiozero import AngularServo
from gpiozero import Servo
from time import sleep
import math
from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()
servo = Servo(12, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory, )
#servo = Servo(12)

try:
	while True:
		
		for i in range(0, 360):
			servo.value = math.sin(math.radians(i))
			sleep(0.01)

except KeyboardInterrupt:
	print("Program stopped")
