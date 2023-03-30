import UWB, servo, time, threading
from evdev import InputDevice, categorize, ecodes, list_devices

def servoThread():
    while True:
        serv.move(uwb.theta)
        time.sleep(1)
        print(f"temp {uwb.theta}")
        
def cameraThread():
    device = None
    EV_VAL_PRESSED = 1
    EV_VAL_RELEASED = 0
    BTN_SHUTTER = 115
    
    while True:
        while device == None:
            devices = [InputDevice(path) for path in list_devices()]
            for d in devices:
                if d.name == "AB Shutter3 Consumer Control":
                    device = d
        
        for event in device.read_loop():
            if event.type == ecodes.EV_KEY and event.value == EV_VAL_PRESSED and event.code == BTN_SHUTTER:
                    print("Camera event")
    
        

def setup():
    global serv, uwb
    uwb = UWB.UWB("/dev/ttyS0", 5)
    serv = servo.Servo(12)
    t = threading.Thread(target=servoThread, daemon=True).start()
    t2 = threading.Thread(target=cameraThread, daemon=True).start()
    #init_camera?

def cleanup():
    uwb.close()
    s.stop_pwm()

if __name__ == "__main__":
    setup()

    uwb.toggleDataFlow()
    while 1:
        # Read position from sensors, write angle to servo, magnification and focus to camera?
        try:
            uwb.update_pos()
        except Exception as ex:
            pass
            #print(ex)
            #break
        except KeyboardInterrupt:
            break

    cleanup()
    
