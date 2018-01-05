"""Turns switches on and off for raspberry pi according to time of day."""

import datetime
import time
import pytz
from astral import Astral

# Globals and constants
a = Astral()
a.solar_depression = 'astronomical'
city = a['San Francisco']
door_status = 'open'

def open_door():
    #Turn on the Switch
    GPIO.output(2, GPIO.LOW)
    #Turn off the switch
    GPIO.cleanup()

def close_door():
    pass

def is_day(t, sun):
    return t > sun['sunrise'] and t < sun['sunset']

def main():
    # check time every 15 min
    t = datetime.datetime.now(pytz.utc)
    today = datetime.date.today()
    sun = city.sun(date=today, local=True)

    # check if door is open or closed
    # if daylight and door is closed, open door
    # if daylight and door is open, do nothing
    if door_status == 'closed' and is_day(t, sun):
        open_door()
        door_status = 'open'

    # if night time and door is open, close door
    # if night and door is closed, do nothing
    if door_status == 'open' and not is_day(t, sun):
        close_door()
        door_status = 'closed'

while True:
    main()
    time.sleep(900)