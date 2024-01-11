#!/usr/bin/env python3

import os
import sys                                     # to work with arguments
import pickle                                  # to work with serealizing/de-serealizing
#import evdev                                  # to work with input devices
from evdev import InputDevice, ecodes

# file name and path to temporary store Caps Lock state
TMP_PATH = '/tmp/'
CAPS_STATE_FILE = '_caps_led.state'

# defining sound to play and sound player
SND_PLAYER = 'paplay'
SND_FILE_BELL = '/usr/share/sounds/freedesktop/stereo/bell.oga'

# list of app standard messages
ERROR = 'Error!'
CAPS_ON = 'Aa '
CAPS_OFF = 'Aa '

# Sound switch (by default - Off)  
sound_sw = 'sound-off'

# initializing Caps Lock state variables
previous_caps_state = 0
current_caps_state = 0

# function to work with file were ops variable should have
# such values as 'rb' - read, 'wb' - write and 'xb' - create only
def file_ops(ops, caps_state = None):
    try:
        file = open(TMP_PATH + CAPS_STATE_FILE, ops)
        match ops:
            case 'rb':
               caps_state = pickle.load(file)
            case 'wb':
               pickle.dump(caps_state, file)

    except FileNotFoundError:
        file = open(TMP_PATH + CAPS_STATE_FILE, 'xb')
        caps_state = 0
   
    file.close()
    return caps_state

# function to play sound if Caps Lock state were changed
def making_beep():
   if previous_caps_state != current_caps_state:
      os.system(SND_PLAYER + ' ' + SND_FILE_BELL)
   
# MAIN -------------------------------------------

# reading args 
# argv1 - device event path; argv2 - sound On/Off (default: Off)
args_numb = len(sys.argv)
match args_numb:
    case 1:
        state_msg = ERROR
    case 2:
        device_event_number = sys.argv[1]
    case 3:
        device_event_number = sys.argv[1]
        sound_sw = sys.argv[2]

# keyboard descriptor
keyboard = InputDevice(device_event_number)

# loading previous Caps Lock state if available
previous_caps_state = file_ops('rb')

# reading current Caps Lock state from keyboard
current_caps_state = keyboard.leds()

# determine and printing Caps Lock state
if current_caps_state == [1]:
    state_msg = CAPS_ON
else:
    state_msg = CAPS_OFF

print (state_msg)
# in case of changing states making a sound
if sound_sw == 'sound-on':
    making_beep()   
# storing Caps Lock state in file and exit
file_ops('wb', current_caps_state)
