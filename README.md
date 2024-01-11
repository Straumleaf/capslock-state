# capslock-state
Waybar widget to show Caps Lock key status with some sound accessibility option like make key status change sound noticible.

## Widget setup

+ assuming that Python already installed.
+ please install evdev package to let application read input events from the system.
        
      pip install evdev

+ clone this repository and enter directory **capslock-state** 
+ copy **capslock-state.py** to the **./config/waybar/script** directory.
+ add below settings to the waybar cnfig file:

      "custom/keyboard-state": {
         "format": "{}",
         "interval": 1,
         "exec": "~/.config/waybar/scripts/capslock-state.py /dev/input/event17 sound-on"
      },

   - please change arguments as per your system properties namely device input events (for instance use below command to find out your keyboard and its event path):
            
         libinput list-devices | grep -e Device -e Kernel

   - you could also mentioned **sound-on** option there to hear a sound confirming Caps Lock switcing or remove it (it is sound-off by default).

