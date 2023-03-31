import pigpio, time
	
def stop_pwm():
	pwm.set_PWM_dutycycle(12, 0)
	pwm.set_PWM_frequency(12, 0)
	
def move(angle):
	dc = (angle / 180) * 2000 + 500 
	pwm.set_servo_pulsewidth(12, dc)
			
if __name__ == "__main__":
	pwm = pigpio.pi()
	pwm.set_mode(12, pigpio.OUTPUT)
	pwm.set_PWM_frequency(12, 50)	
	
	while True:
		try:
			angle = int(input("Enter angle (0-180): "))
			move(angle) 
		except KeyboardInterrupt:
			break
	
	stop_pwm()		
