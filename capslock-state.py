#!/usr/bin/env python3

import os                                      # to run sound player and work with arguments
import sys                                     # to work with arguments
import pickle                                  # to work with serealizing/de-serealizing variable
from evdev import InputDevice, ecodes

# file name and path to temporary store Caps Lock state
TMP_PATH = '/tmp/'
CAPS_STATE_FILE = '_caps_led.state'

# defining sound player and sets of sounds to choose from
SND_PLAYER = 'paplay'
SND_FILE_BELL = '/usr/share/sounds/freedesktop/stereo/bell.oga'
SND_FILE_MSG = '/usr/share/sounds/freedesktop/stereo/message.oga'
SND_FILE_DLG_INF = '/usr/share/sounds/freedesktop/stereo/dialog-information.oga'
SND_FILE_DLG_ERR = '/usr/share/sounds/freedesktop/stereo/dialog-error.oga'

# list of app standard messages
ERROR = 'Error!'
CAPS_ON = 'Aa '
CAPS_OFF = 'Aa '

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
def making_beep(prv_state, curr_state):
   if prv_state != curr_state:
      os.system(SND_PLAYER + ' ' + SND_FILE_BELL)
   
# MAIN -------------------------------------------

def main(args):
    # reading args 
    # argv1 - device event path; argv2 - sound On/Off (default: Off)
    args_numb = len(sys.argv)

    # Sound switch (by default - Off)  
    sound_sw = 'sound-off'

    match args_numb:
        case 1:
            state_msg = ERROR
        case 2:
            device_event_number = args[1]
        case 3:
            device_event_number = args[1]
            sound_sw = args[2]

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

    print(state_msg)
    # in case of changing states making a sound
    if sound_sw == 'sound-on':
        making_beep(previous_caps_state, current_caps_state)   
    # storing Caps Lock state in file and exit
    file_ops('wb', current_caps_state)

if __name__ == '__main__':
    main(sys.argv)
