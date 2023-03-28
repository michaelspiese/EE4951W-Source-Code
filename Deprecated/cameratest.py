import serial
import time 
from statistics import mean

from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import AngularServo, Servo
from time import sleep
import math


precision = 10
servo = Servo(14)
x = [0 for n in range(precision)]
y = [0 for n in range(precision)]

DWM = serial.Serial(port="/dev/ttyACM0", baudrate=115200)

factory = PiGPIOFactory()
servo = Servo(12, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory, )

DWM.write("\r\r".encode())
time.sleep(1)
DWM.write("lec\r".encode())
time.sleep(1)

i = 0
z = 0
while True:
	try:
		line = DWM.readline()
		if(line):
			if len(line) >= 20:
				#print(line.decode())
				parse = line.decode().split(',')
				if parse[-5].strip() != "nan":
					x[i] = float(parse[-5].strip())
					y[i] = float(parse[-4].strip())
					x_mean, y_mean = (mean(x),mean(y))
					print(f"x={x_mean:.3f} y={y_mean:.3f}", end=" ")
                
	except Exception as ex:
		print(ex)
	except KeyboardInterrupt:
		print("INTERRUPT")
		break
        
	i = (i+1)%precision
	
	try:	
		theta = int(math.atan(mean(x)/mean(y))*180/math.pi)
	except ZeroDivisionError:
		theta = 90
		
	print(f"angle={theta}")
	
	for j in range(z, theta+1):
			servo.value = math.sin(math.radians(j))
			sleep(0.001)
	
	z = theta

DWM.write("lec\r".encode())
DWM.close()
