import serial
import time 


from gpiozero import AngularServo
from gpiozero import Servo
from time import sleep
import math

servo = Servo(14)
 

DWM = serial.Serial(port="/dev/ttyACM0", baudrate=115200)

DWM.write("\r\r".encode())
time.sleep(1)
DWM.write("lec\r".encode())
time.sleep(1)

while True:
    try:
        line = DWM.readline()
        if(line):
            if len(line) >= 20:
                parse = line.decode().split(',')
                AN1_pos =  parse[-1].strip()
                AN2_pos =  parse[-7].strip()
                
                val = (AN1_pos,AN2_pos)
                print("AN1 =")
                print(AN1_pos)
                print("AN2 =")
                print(AN2_pos)
                
                if AN1_pos < AN2_pos:
                    
                    x = AN1_pos / AN2_pos
                    theta = math.atan(x)
                    
                    ntheta = int(4*theta/math.pi)
                    servo.value = ntheta
                    #sleep(1)
                    sleep(2)
                    
                elif AN1_pos > AN2_pos: 
                    x = AN2_pos / AN1_pos
                    theta = math.atan(x)
                    
                    ntheta = int(4*theta/math.pi)
                    servo.value = ntheta
                    #sleep(1)
                    sleep(2)
                
                
            # else:
            #     print("Position not calculated: ", line.decode().strip())
    except Exception as ex:
        print(ex)
        break
    except KeyboardInterrupt:
        print("INTERRUPT")
        break

DWM.write("lec\r".encode())
DWM.close()
