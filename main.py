import UWB, servo, cam, shutter, time, threading

# Thread to move servo to angle of tag
def servoThread():
    while True:
        serv.move(uwb.theta)
        time.sleep(0.1)
        
# Thread to take a photo when the shutter button is pressed
def cameraThread():
    while True:
        time.sleep(0.5)
        if btn.queue > 0:
            camera.takePhoto()
            print(f"Removing camera event from queue ({btn.queue-1} total)")
            btn.queue -= 1

# Setup function to initialize all sensors, devices, and threads
def setup():
    global serv, uwb, camera, btn
    
    uwb = UWB.UWB("/dev/ttyACM0", 1)                # Open serial connection to gateway with USB port /dev/ttyACM0
    serv = servo.Servo(12)                          # Initialize servo on GPIO pin 12
    btn = shutter.Shutter()                         # Initialize shutter button
    camera = cam.ArducamHawkEye(res=(2312, 1736))   # Initialize camera with resolution 2312x1736
    
    # Start threads for each asynchronous task
    threading.Thread(target=servoThread, daemon=True).start()
    threading.Thread(target=btn.btn_loop, daemon=True).start()
    threading.Thread(target=cameraThread, daemon=True).start()

# Cleanup function to safely exit program
def cleanup():
    uwb.close()
    serv.stop_pwm()

# Main function to run program. Setup -> Run -> Cleanup
if __name__ == "__main__":
    setup()

    uwb.toggleDataFlow()
    while 1:
        # Update position of tag as fast as possible until keyboard interrupt is received.
        try:
            uwb.update_pos()
        except Exception as ex:
            print(ex)
            break
        except KeyboardInterrupt:
            break
    
    # Cleanup and exit
    cleanup()
