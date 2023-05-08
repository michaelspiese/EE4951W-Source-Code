from picamera2 import Picamera2, Preview
from libcamera import Transform, controls
import time

class ArducamHawkEye:
	def __init__(self, res):
		# Initialize camera with resolution specified in main's setup function. Set focus to 6 (hard-coded, unsure why this value works).
		self.pIdx = 0
		self.cam = Picamera2()
		self.config = self.cam.create_preview_configuration(main={"size": res})
		self.cam.configure(self.config)
		self.cam.start()
		self.set_focus(6)

	# Function to take a photo and save it to the specified directory. Increment photo index by 1.
	def takePhoto(self):
		self.cam.capture_file(f"/media/ee4951w/BLASCYK/Pictures/{self.pIdx}.jpg")
		self.pIdx+=1
	
	# Function to set focus of camera.
	def set_focus(self, focus):
		self.cam.set_controls({"AfMode": 0, "LensPosition": focus})

# For testing purposes. Run this file to see if the ArducamHawkEye class works as intended. Takes a ful-resolution photo (Raspberry Pi Model 3B) after 2 seconds.				
if __name__ == "__main__":
	c = ArducamHawkEye((4624, 3472))
	time.sleep(2)
	c.takePhoto()
