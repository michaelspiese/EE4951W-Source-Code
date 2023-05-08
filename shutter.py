from evdev import InputDevice, categorize, ecodes, list_devices
import time

# Bluetooth button constants
EV_VAL_PRESSED = 1
EV_VAL_RELEASED = 0
BTN_SHUTTER = 115

class Shutter:
	def __init__(self):
		# Initialize shutter button. Initially set to None until connected, and initialize photo queue to 0
		self.shutter = None
		self.queue = 0
	
	# Function to connect to AB Shutter3 button. Called in btn_loop() until successful.
	def connect(self):
		while self.shutter == None:
			devices = [InputDevice(path) for path in list_devices()]
			for device in devices:
				if device.name == "AB Shutter3 Consumer Control":
					print(f"Shutter connected as {device.path}")
					self.shutter = device
    
	# Function to loop until button is pressed. When pressed, add a camera event to the queue.
	def btn_loop(self):
		self.connect()
		while True:
			for event in self.shutter.read_loop():
				time.sleep(0.5)
				if event.type == ecodes.EV_KEY and event.value == EV_VAL_PRESSED and event.code == BTN_SHUTTER:
					print(f"Adding camera event to queue ({self.queue+1} total)")
					self.queue += 1

# For testing purposes. Run this file to see if the Shutter class works as intended.			
if __name__ == "__main__":
	s = Shutter()
	s.connect()
	s.btn_loop()
