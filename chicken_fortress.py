"""Turns relay switches on and off using raspberry pi according to time of day."""

import RPi.GPIO as GPIO
import datetime
import time
import pytz
from astral import Astral

# Globals and constants
a = Astral()
a.solar_depression = 'astronomical'
city = a['San Francisco']
pt = pytz.timezone('America/Los_Angeles')
door_status = 'open'
door_motor_forwards = 2
door_motor_backwards = 3

# Setup Raspberry Pi
GPIO.setmode(GPIO.BCM)

# Functions
def open_door():
    #Setup the switch
    GPIO.setup(door_motor_forwards, GPIO.OUT)
    GPIO.output(door_motor_forwards, GPIO.HIGH)
    time.sleep(2)
    #Switch activated by low voltage
    GPIO.output(door_motor_forwards, GPIO.LOW)
    #Let motor run to winch up door
    time.sleep(6)
    GPIO.cleanup()
    print('Opened: {:%Y-%m-%d %H:%M:%S %z}'.format(datetime.datetime.now(pytz.utc)))

def close_door():
    #Setup the switch
    GPIO.setup(door_motor_backwards, GPIO.OUT)
    GPIO.output(door_motor_backwards, GPIO.HIGH)
    time.sleep(2)
    #Switch activated by low voltage
    GPIO.output(door_motor_backwards, GPIO.LOW)
    #Let motor run to winch down door
    time.sleep(6)
    GPIO.cleanup()
    print('Closed: {:%Y-%m-%d %H:%M:%S %z}'.format(datetime.datetime.now(pytz.utc)))

def is_day(t, sun):
    return t > sun['sunrise'] and t < sun['sunset']

def main():
    # check time every 15 min
    t = pt.localize(datetime.datetime.now())
    today = datetime.date.today()
    sun = city.sun(date=today, local=True)
    global door_status
    # check if door is open or closed
    # if daylight and door is closed, open door
    # if daylight and door is open, do nothing
    if door_status == 'closed' and is_day(t, sun):
        time.sleep(3600)
        open_door()
        print('Sunrise: %s' % str(sun['sunrise']))
        door_status = 'open'

    # if night time and door is open, close door
    # if night and door is closed, do nothing
    if door_status == 'open' and not is_day(t, sun):
        close_door()
        print('Sunset:  %s' % str(sun['sunset']))
        door_status = 'closed'

# Keep running every 15 min
while True:
    main()
    time.sleep(900)