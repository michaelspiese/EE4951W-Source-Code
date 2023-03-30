import pigpio, time

class Servo:
	def __init__(self, pin):
		self.pin = pin
		self.pwm = pigpio.pi()
		self.pwm.set_mode(self.pin, pigpio.OUTPUT)
		self.pwm.set_PWM_frequency(self.pin, 50)
		
	def move(self, angle):
		dc = (angle / 180) * 2000 + 500  # Updating duty cycle written to servo to range of 500 - 2500 (pigpio)
		self.pwm.set_servo_pulsewidth(self.pin, dc)
			
	def stop_pwm(self):
		self.pwm.set_PWM_dutycycle(self.pin, 0)
		self.pwm.set_PWM_frequency(self.pin, 0)
