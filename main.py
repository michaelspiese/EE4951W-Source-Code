import UWB, servo, sys, time, threading

def servoThread():
    while not stopThread:
        s.move(uwb.theta)
        time.sleep(0.1)

def setup():
    global s, uwb, stopThread
    stopThread = False
    uwb = UWB.UWB("/dev/ttyS0", 5)
    s = servo.Servo(12)
    sThread = threading.Thread(target=servoThread)
    sThread.start()
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
            print(ex)
        except KeyboardInterrupt:
            stopThread = True
            break

    cleanup()
    sys.exit(0)