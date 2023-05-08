import UWB, servo, cam, shutter, time, threading

def servoThread():
    temp = 0
    #direc = 10
    while True:
        serv.move(uwb.theta)
        time.sleep(0.1)
        #temp += direc
        #if temp > 180 or temp < 0:
        #    direc *= -1
        #    temp = 2*direc+temp
        
def cameraThread():
    lp = 0.0
    while True:
        # REMOVE?
        time.sleep(0.5)
        if btn.queue > 0:
            if uwb.dist == 0 or 1/uwb.dist > 10.0:
                lp = 10.0
            else:
                lp = 1/uwb.dist
            # Steps up the focus from 0 to 10 by 0.5
            #camera.set_focus(lp)
            #time.sleep(0.1)
            #print(lp)
            #lp += 0.5
            #if lp == 10.5:
            #    lp = 0.0
            camera.takePhoto()
            print(f"Removing camera event from queue ({btn.queue-1} total)")
            btn.queue -= 1

def setup():
    global serv, uwb, camera, btn
    uwb = UWB.UWB("/dev/ttyACM0", 1)
    serv = servo.Servo(12)
    btn = shutter.Shutter()
    #camera = cam.ArducamHawkEye(res=(1920, 1080))
    camera = cam.ArducamHawkEye(res=(2312, 1736))
    #camera = cam.ArducamHawkEye(res=(4624, 3472))
    
    servThread = threading.Thread(target=servoThread, daemon=True).start()
    shutterThread = threading.Thread(target=btn.btn_loop, daemon=True).start()
    camThread = threading.Thread(target=cameraThread, daemon=True).start()

def cleanup():
    uwb.close()
    serv.stop_pwm()

if __name__ == "__main__":
    setup()

    uwb.toggleDataFlow()
    while 1:
        # Read position from sensors, write angle to servo, magnification and focus to camera?
        try:
            uwb.update_pos()
        except Exception as ex:
            print(ex)
            break
        except KeyboardInterrupt:
            break

    cleanup()
    
