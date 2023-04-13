import serial, time, math, random
from statistics import mean

class UWB:
    def __init__(self, port, precision):
        # Containers to hold positional/tracking data
        self.precision = precision
        self.xbuf = [0 for n in range(self.precision)]
        self.ybuf = [0 for n in range(self.precision)]
        self.bufIdx = 0
        self.x = 0.0
        self.y = 0.0
        self.dist = 0.0
        self.theta = 0

        # Opening a serial connection with the gateway
        self.port = port
        self.DWM = serial.Serial(port, 115200)

        # Entering Shell Mode on the DWM1001
        self.DWM.write("\r\r".encode())
        time.sleep(1)

    def toggleDataFlow(self):
        # Write the command to toggle reading positional data from the gateway
        self.DWM.write("lec\r".encode())
        time.sleep(1)

    def update_pos(self):
        # Read a new line of positional data
        line = self.DWM.readline()
        # Make sure the line is long enough to be cosidered
        if(len(line) >= 20):
            # Parse data to store new values of x and y in buffer ONLY IF these values are valid
            parse = line.decode().split(',')
            try:
                if parse[-5].strip() != "nan":
                    self.xbuf[self.bufIdx] = float(parse[-5].strip())
                    self.ybuf[self.bufIdx] = float(parse[-4].strip())
                    self.bufIdx = (self.bufIdx+1) % self.precision
            except:
                print("Ignoring out of range error from parsing line")
                return

                # Update xy position of tag
                self.x, self.y = (mean(self.xbuf),mean(self.ybuf))
                
                # Calculating the distance of the direct path to the tag from the camera
                self.dist = math.sqrt(self.x**2 + self.y**2)

                # Update angle from new values of x and y
                try:	
                    self.theta = int(math.atan(self.x/self.y)*-180/math.pi) + 90
                except ZeroDivisionError:
                    pass # Ignore very specific case where y=0 exactly
                    
                print(f"x={self.x:.3f} y={self.y:.3f} distance={self.dist} angle={self.theta}")
    
    def close(self):
        self.toggleDataFlow()
        self.DWM.close()
        
if __name__ == "__main__":
    u = UWB("/dev/ttyACM0", 5)
    u.toggleDataFlow()
    while True:
        try:
            u.update_pos()
            time.sleep(5)
            print(f"x: {u.x}, y: {u.y}, angle: {u.theta}")
        except KeyboardInterrupt:
            break
    u.close()
