# SoccerTracker: Method for Tracking and Photographing a Soccer Player

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
dtoverlay=vc4-kms-v3d,cma-256
```

## Boot script

In order to make the device more user-friendly, a script to launch the program at boot should be created. In our case, the boot script `soccer-tracker.sh` looks like the following:

```shell
sudo pigpiod &
sleep 10
lxterminal --title="Soccer Tracker" -e "python3 /home/pi/EE4951W-Source-Code/main.py; read -n 1 -s" 
```

Add this script to the directory `/usr/local/bin`.

Next, use the following command to make this shell file an executable script:

```bash
> sudo chmod +x /usr/local/bin/soccer-tracker.sh
```

## Autostart

Since this project runs at startup in a terminal window, we are using LXDE-pi autostart to run our boot script after the graphical environment has been started. Add the following line to the file `/etc/xdg/lxsession/LXDE-pi/autostart` for the same results.

```
@bash /path-to-boot-script/soccer-tracker.sh
```
