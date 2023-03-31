import serial
import time
import math
from statistics import mean

DWM = serial.Serial(port="/dev/ttyS0", baudrate=115200)
precision = 5

DWM.write("\r\r".encode())
time.sleep(1)
DWM.write("lec\r".encode())
time.sleep(1)

devices = {"DD1D": [0 for n in range(precision)], "CC83": [0 for n in range(precision)]}

i = 0
while True:
    try:
        line = DWM.readline()
        if(line):
            if len(line) >= 60:
                parse = line.decode().split(',')
                try:
                    devices[parse[3]][i%precision] = float(parse[7])
                    devices[parse[9]][i%precision] = float(parse[13].strip())
                except:
                    devices["CC83"][i%precision] = 0
                    devices["DD1D"][i%precision] = 0
                i += 1
    except Exception as ex:
        print(ex)
        break
    except KeyboardInterrupt:
        print("INTERRUPT")
        break

    distI = mean(devices["DD1D"])
    distA = mean(devices["CC83"])

    try:
        angI = math.acos((distI**2 + 2.1**2 - distA**2) / (2 * distI * 2.1))
        angA = math.acos((distA**2 + 2.1**2 - distI**2) / (2 * distA * 2.1))
    except:
        angI = 0.000
        angA = 0.000

    x = distI * math.cos(angI)
    y = distI * math.sin(angI)

    print(f"magI:{distI:.3f}  ", f"magA:{distA:.3f}      ", f"angI:{math.degrees(angI):.3f}  ", f"angA:{math.degrees(angA):.3f}      ", f"x:{x:.3f}  ", f"y:{y:.3f}")

DWM.write("lec\r".encode())
DWM.close()