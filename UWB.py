import serial, time, math
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

    # Toggling the data flow from the gateway by sending the "lec" command to the DWM1001 in shell mode.
    def toggleDataFlow(self):
        self.DWM.write("lec\r".encode())
        time.sleep(1)

    # Updating the position of the tag by reading a new line of positional data from the gateway.
    def update_pos(self):
        line = self.DWM.readline()

        # Make sure the line is long enough to be cosidered
        if(len(line) >= 20):

            # Parse data to store new values of x and y in buffer ONLY IF these values are valid
            parse = line.decode().split(',')
            if len(parse) > 4:
                if parse[3].strip() != "nan":
                    
                    # Store new values of x and y in buffers
                    self.xbuf[self.bufIdx] = float(parse[3].strip())
                    self.ybuf[self.bufIdx] = float(parse[4].strip())
                    self.bufIdx = (self.bufIdx+1) % self.precision

                    # Update xy position of tag
                    self.x, self.y = (mean(self.xbuf),mean(self.ybuf))
                    
                    # Calculating the distance of the direct path to the tag from the camera
                    self.dist = math.sqrt(self.x**2 + self.y**2)

                    # Update angle from new values of x and y
                    try:	
                        self.theta = int(math.atan(self.x/self.y)*-180/math.pi) + 90
                    except ZeroDivisionError:
                        pass # Ignore very specific case where y=0 exactly
  
            print(f"x={self.x:.3f} y={self.y:.3f} distance={self.dist:.3f} angle={self.theta:.3f}")
    
    # Turn off positional data flow and close serial connection to gateway
    def close(self):
        self.toggleDataFlow()
        self.DWM.close()

# For testing purposes. Setup sensor network and run this file to see if the UWB class works as intended. 
# Displays tag position, distance, and angle until keyboard interrupt is received.
if __name__ == "__main__":
    u = UWB("/dev/ttyACM0", 1)
    u.toggleDataFlow()
    while True:
        try:
            u.update_pos()
        except KeyboardInterrupt:
            break
    u.close()
