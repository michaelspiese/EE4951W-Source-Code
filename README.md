# EE4951W-Source-Code

## AUTOSTART

This project runs at startup using the LXDE-pi autostart script.
Add the line "@bash /path-to-boot-script/soccer-tracker.sh" for the same results

## Boot script

The boot script soccer-tracker.sh looks like the following:
```console
sudo pigpiod &
sleep 10
lxterminal --title="Soccer Tracker" -e "python3 /project-directory/main.py; read -n 1 -s"" 
```
