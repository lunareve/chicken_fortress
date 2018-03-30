"""Turns switches on and off for raspberry pi according to time of day."""

import RPi.GPIO as GPIO
import datetime
import time
import pytz
from astral import Astral

# Globals and constants
a = Astral()
a.solar_depression = 'astronomical'
city = a['San Francisco']
door_status = ['open']
door_motor_forwards = 2
door_motor_backwards = 3

# Setup Rasberrry Pi
GPIO.setmode(GPIO.BCM)

# Functions
def open_door():
    #Turn on the switch
    GPIO.setup(door_motor_forwards, GPIO.OUT)
    GPIO.output(door_motor_forwards, GPIO.HIGH)
    time.sleep(6)
    #Turn off the switch
    GPIO.output(door_motor_forwards, GPIO.LOW)
    GPIO.cleanup()

def close_door():
    #Turn on the switch
    GPIO.setup(door_motor_backwards, GPIO.OUT)
    GPIO.output(door_motor_backwards, GPIO.HIGH)
    time.sleep(6)
    #Turn off the switch
    GPIO.output(door_motor_backwards, GPIO.LOW)
    GPIO.cleanup()

def is_day(t, sun):
    return t > sun['sunrise'] and t < sun['sunset']

def main():
    # check time every 15 min
    t = datetime.datetime.now(pytz.utc)
    today = datetime.date.today()
    sun = city.sun(date=today, local=True)
    global door_status
    # check if door is open or closed
    # if daylight and door is closed, open door
    # if daylight and door is open, do nothing
    if door_status == 'closed' and is_day(t, sun):
        time.sleep(3600)
        open_door()
        door_status = 'open'

    # if night time and door is open, close door
    # if night and door is closed, do nothing
    if door_status == 'open' and not is_day(t, sun):
        close_door()
        door_status = 'closed'

# Keep running every 15 min
while True:
    main()
    time.sleep(900)