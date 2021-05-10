# SPDX-FileCopyrightText: 2021 Shane Powell
#
# SPDX-License-Identifier: MIT

# Mini gaming keyboard software for situations when you do not have room for a full size keyboard.

# You'll need to connect Keybow 2040 to a computer, as you would with a regular
# USB keyboard.

# Drop the keybow2040.py file into your `lib` folder on your `CIRCUITPY` drive.

# NOTE! Requires the adafruit_hid CircuitPython library also!

import board
from keybow2040 import Keybow2040

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

# Set up Keybow
i2c = board.I2C()
keybow = Keybow2040(i2c)
keys = keybow.keys

# Set up the keyboard and layout
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

# A map of keycodes that will be mapped sequentially to each of the keys, 0-15
keymap = [
    Keycode.ONE,
    Keycode.TWO,
    Keycode.THREE,
    Keycode.FOUR,
    Keycode.FIVE,
    Keycode.Q,
    Keycode.UP_ARROW,
    Keycode.F,
    Keycode.LEFT_SHIFT,
    Keycode.LEFT_ARROW,
    Keycode.DOWN_ARROW,
    Keycode.RIGHT_ARROW,
    Keycode.LEFT_CONTROL,
    Keycode.SPACEBAR,
    Keycode.SPACEBAR,
    Keycode.SPACEBAR,
]

# The colour to set the keys when pressed, yellow.
rgb = (0, 0, 255)

click_rgb = (255,255,255)

arrow_rgb = (0, 255, 0)
wsad_rgb = (255, 0, 0)
space_bar_rgb = (255,0,255)

def set_leds():

    for key in keys:
        set_led_from_config(key)

def set_led_from_config(key):
    keycode = keymap[key.number]
    if keycode == Keycode.SPACEBAR:
        key.set_led(*space_bar_rgb)
    elif any(x == keycode for x in (Keycode.UP_ARROW, Keycode.LEFT_ARROW,
        Keycode.DOWN_ARROW,
        Keycode.RIGHT_ARROW)):
        key.set_led(*arrow_rgb)
    elif any(x == keycode for x in (Keycode.W, Keycode.S,
        Keycode.A,
        Keycode.D)):
        key.set_led(*wsad_rgb)
    else:
        key.set_led(*rgb)

# Attach handler functions to all of the keys
for key in keys:
    # A press handler that sends the keycode and turns on the LED
    
    keycode = keymap[key.number]

    set_led_from_config(key)

    @keybow.on_press(key)
    def press_handler(key):
        keycode = keymap[key.number]
        print("press", keycode)
        keyboard.press(keycode)
        prev_rgb = key.rgb
        key.set_led(*click_rgb)
        key.rgb = prev_rgb
        print(key.number)
        # key.last_state = False
        # key.press_func_fired = False

    # @keybow.on_hold(key)
    # def press_handler(key):
    #     keycode = keymap[key.number]
    #     keyboard.send(keycode)
    #     prev_rgb = key.rgb
    #     key.set_led(*click_rgb)
    #     key.rgb = prev_rgb
    #     print(key.number)

    # A release handler that turns off the LED
    @keybow.on_release(key)
    def release_handler(key):
        keycode = keymap[key.number]
        print("release", keycode)
        keyboard.release(keycode)
        key.set_led(*key.rgb)
keybow.rotate(90)
set_leds()
while True:
    # Always remember to call keybow.update()!
    keybow.update()


