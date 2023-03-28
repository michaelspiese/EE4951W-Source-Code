import pigpio
import time

pwm = pigpio.pi()
pwm.set_mode(12, pigpio.OUTPUT)

pwm.set_PWM_frequency(12, 50)

def move_servo(angle):
	dc = (angle / 180) * 2000 + 500
	pwm.set_servo_pulsewidth(12, dc)
	
if __name__ == "__main__":
	while 1:
		try:
			angle = int(input("Enter angle (0-180): "))
			if angle < 0:
				angle = 0
			elif angle > 180:
				angle = 180
				
			move_servo(angle)
		except KeyboardInterrupt:
			break
		
	pwm.set_PWM_dutycycle(12, 0)
	pwm.set_PWM_frequency(12, 0)

