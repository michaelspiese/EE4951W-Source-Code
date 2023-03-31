from picamera2 import Picamera2, Preview
from libcamera import Transform
#import time

class ArducamHawkEye:
	def __init__(self, res):
		self.pIdx = 0;
		self.cam = Picamera2()
		self.config = self.cam.create_preview_configuration(main={"size": res},transform=Transform(hflip=True, vflip=True))
		self.cam.configure(self.config)
		self.cam.start_preview(Preview.QT)
		self.cam.start()

	def takePhoto(self):
		self.cam.capture_file(f"{self.pIdx}.jpg")
		self.pIdx+=1
					
