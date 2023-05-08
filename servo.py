import pigpio, time

class Servo:
	def __init__(self, pin):
		# Initializing servo on GPIO pin specified in main's setup function
		self.pin = pin
		self.pwm = pigpio.pi()
		self.pwm.set_mode(self.pin, pigpio.OUTPUT)
		self.pwm.set_PWM_frequency(self.pin, 50)
		
	# Function to move servo to specified angle
	# Updating duty cycle written to servo to range of 500 - 2500 (pigpio specification for 0 - 180 degrees)
	def move(self, angle):
		dc = (angle / 180) * 2000 + 500  
		self.pwm.set_servo_pulsewidth(self.pin, dc)
	
	# Function to stop sending PWM signal to servo. Disengages servo.
	def stop_pwm(self):
		self.pwm.set_PWM_dutycycle(self.pin, 0)
		self.pwm.set_PWM_frequency(self.pin, 0)

# For testing purposes. Run this file to see if the Servo class works as intended.
# Initializes servo on GPIO pin 12 and moves it to angle specified by user input.
if __name__ == "__main__":
	s = Servo(12)
	while True:
		try:
			angle = int(input("Enter angle (0-180): "))
			s.move(angle) 
		except KeyboardInterrupt:
			break
	s.stop_pwm()
