# SoccerTracker: Method for Tracking and Photographing a Soccer Player

## Motive

If one wished to photograph a soccer player and take "action shots" while they were playing the game, most of their focus would be on making sure the photos turned out and not on the game itself. This project aims to solve this problem by automating the camera's position, focus, and magnification; reducing the user's role in taking photos to providing an input of when the photos should be taken.

## Method

An Ultra-Wideband sensor network is used to track the player. Three anchors are set an static positions on the field, and the tag calculates its xyz-position based on it's distance from the anchors. A fifth sensor is used as a passive anchor gateway node, to which the tag can directly send its position. The gateway node is connected to a Raspberry Pi Model 3B via the gpio pins, and UART is used to send and receive data between the Pi and gateway. From the position of the tag, the angle and distance from the camera at the origin to the tag can be calculated and used to control other systems. The loop in `main.py` runs forever and exists to update the position recognized by the program as fast as data is sent from the sensor.

The angle of the camera is controlled by a servo in a separate daemon thread from the main thread that is updating the position. This servo simply takes the angle to the tag, writes it to the Pi's PWM pin, and delays for 0.1 seconds (the speed data is written from the sensor).

The camera shutter button is a bluetooth button. In yet another daemon thread, the program waits for the button to connect and then polls all events from the button for presses in a loop that runs forever. Whenever a press is detected, an integer "queue" is incremented signaling that a picture should be taken.

The camera is implemented in one final daemon thread that is separate from the main thread. First, the queue from the button must be greater than 0. If there is a camera event expected, the camera simply reads the distance to the tag, updates the camera settings to the required focus and magnification, saves a picture, and decrements the queue.

With more time/resources, there are a few ways to expand on the functionality of this system in the future. First, we would like to create a more robust sensor network for more accurate positional data. Also, using the cloud to be able to access the pictures that were taken remotely would remove the need for the user to retrieve these photos themselves.

This program is configured to run when the Raspberry Pi boots. The section "Configuring the Raspberry Pi" section below details how this is done and also how to install the necessary dependencies.

## Hardware

Tracking: DWM1001-Dev x 5

Camera: ArduCam Hawk Eye 64MP

Camera movement: SG90 Servo

Camera button: AB Shutter 3

Microcontroller: Raspberry Pi Model 3B

# Configuring the Raspberry Pi

## Installing Dependencies

Before running the program, the python modules `pigpio`, `evdev`, and proprietary flavors of `libcamera` and `picamera2` must be installed. 

### Installing python modules from apt

Below is the commands to install `pigpio` and `evdev`:

```shell
> sudo apt update
> sudo apt upgrage
> sudo apt-get install pigpio
> sudo apt-get install python3-evdev
```

### Installing ArduCam modules and drivers

`Libcamera` and `picamera2` are installed by default on newer builds of Raspbian. However, ArduCam has their own proprietary flavors of these programs that must be installed before the ArduCam Hawk Eye camera can be used.

```shell
> sudo wget -O install_pivariety_pkgs.sh https://github.com/ArduCAM/Arducam-Pivariety-V4L2-Driver/releases/download/install_script/install_pivariety_pkgs.sh
> sudo chmod +x install_pivariety_pkgs.sh
> ./install_pivariety_pkgs.sh -p libcamera
> ./install_pivariety_pkgs.sh -p libcamera_apps
> ./install_pivariety_pkgs.sh -p 64mp_pi_hawk_eye_kernel_driver
```

It is also necessary to add the following lines to `/boot/config.txt` under [All]:

```
dtoverlay=arducam-64mp
dtoverlay=vc4-kms-v3d,cma-512
```

## Boot script

In order to make the device more user-friendly, a script to launch the program at boot should be created. In our case, the boot script `soccer-tracker.sh` looks like the following:

```shell
#!/bin/bash
sudo pigpiod &
sleep 10
lxterminal --title="Soccer Tracker" -e "python3 /home/ee4951w/src/main.py; read -n 1 -s" 
```

Make sure to change the location to the main python file, and add this script to the directory `/usr/local/bin`.

Next, use the following command to make this shell file an executable script:

```bash
> sudo chmod +x /usr/local/bin/soccer-tracker.sh
```

## Autostart

Since this project runs at startup in a terminal window, we are using LXDE-pi autostart to run our boot script after the graphical environment has been started. Add the following line to the end of the file `/etc/xdg/lxsession/LXDE-pi/autostart` for the same results.

```
@bash /path-to-boot-script/soccer-tracker.sh
```
