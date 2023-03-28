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
                if parse[-5].strip() != "nan":
                    self.xbuf[self.bufIdx] = float(parse[-5].strip())
                    self.ybuf[self.bufIdx] = float(parse[-4].strip())
                    self.bufIdx = (self.bufIdx+1) % self.precision

                    # Update xy position of tag
                    self.x, self.y = (mean(self.xbuf),mean(self.ybuf))

                    # Update angle from new values of x and y
                    try:	
                        self.theta = int(math.atan(self.x/self.y)*-180/math.pi)
                    except ZeroDivisionError:
                        self.theta = 90
                    print(f"x={self.x:.3f} y={self.y:.3f} angle={self.theta}")
    
    def close(self):
        self.toggleDataFlow()
        self.DWM.close()