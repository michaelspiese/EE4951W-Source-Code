import serial
import time

# try:
#     ser = serial.Serial("COM7",115200,8,'N',1,100,0)
#     ser.write(b'\r\r')
#     time.sleep(1)
#     ser.write(b'lec\r')
#     data = b''
#     while data == b'':
#         data = ser.readline()
#         print(data)
#     ser.close()
# except Exception as e:
#     print(Exception)
#     exit()

# ser.open()

# for i in range(20):
#     temp = 0
#     while temp == 0:
#         data = ser.readline()
#         if data != b'':
#             print(data.decode(),end='')
#             temp = 1

# ser.close()

DWM = serial.Serial(port="COM7", baudrate=115200)

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
                pos = parse[-1].strip()
                print(pos)
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