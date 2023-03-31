import UWB, servo, cam, shutter, time, threading

def servoThread():
    while True:
        serv.move(uwb.theta)
        time.sleep(0.05)
        
def cameraThread():
    while True:
        if btn.queue > 0:
            camera.takePhoto()
            print(f"Removing camera event from queue ({btn.queue-1} total)")
            btn.queue -= 1

def setup():
    global serv, uwb, camera, btn
    uwb = UWB.UWB("/dev/ttyACM0", 5)
    serv = servo.Servo(12)
    btn = shutter.Shutter()
    #camera = cam.ArducamHawkEye(res=(2312, 1736))
    camera = cam.ArducamHawkEye(res=(4624, 3472))
    
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
    
