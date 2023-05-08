from picamera2 import Picamera2, Preview
from libcamera import Transform, controls
import time

alp = "abcdefghijklmnopqrstuvwxyz"

class ArducamHawkEye:
	def __init__(self, res):
		self.pIdx = 0;
		self.cam = Picamera2()
		self.config = self.cam.create_preview_configuration(main={"size": res})
		#self.config = self.cam.create_preview_configuration(main={"size": res},transform=Transform(hflip=True, vflip=True))
		self.cam.configure(self.config)
		#self.cam.start_preview(Preview.QTGL)
		self.cam.start()
		self.set_focus(6)

	def takePhoto(self):
		#self.cam.capture_file(f"/home/ee4951w/Pictures/{alp[self.pIdx%26]}.jpg")
		self.cam.capture_file(f"/media/ee4951w/BLASCYK/Pictures/{self.pIdx}.jpg")
		self.pIdx+=1
		
	def set_focus(self, focus):
		self.cam.set_controls({"AfMode": 0, "LensPosition": focus})
					
if __name__ == "__main__":
	c = ArducamHawkEye((2048, 2048))
	time.sleep(2)
	c.takePhoto()
