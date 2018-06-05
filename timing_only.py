"""Includes only timing related code since GPIO is difficult to test off the Pi."""

import datetime
import time
import pytz
from astral import Astral

# Globals and constants
a = Astral()
a.solar_depression = 'astronomical'
city = a['San Francisco']
door_status = 'open'

# Functions
def open_door(t):
    print('Opened: {:%Y-%m-%d %H:%M:%S %z}'.format(t))

def close_door(t):
    print('Closed: {:%Y-%m-%d %H:%M:%S %z}'.format(t))

def is_day(t, sun):
    return t > sun['sunrise'] and t < sun['sunset']

def main(t, today):
    sun = city.sun(date=today, local=True)
    global door_status
    # check if door is open or closed
    # if daylight and door is closed, open door
    # if daylight and door is open, do nothing
    if door_status == 'closed' and is_day(t, sun):
        open_door(t)
        print('Sunrise: %s' % str(sun['sunrise']))
        door_status = 'open'

    # if night time and door is open, close door
    # if night and door is closed, do nothing
    elif door_status == 'open' and not is_day(t, sun):
        close_door(t)
        print('Sunset:  %s' % str(sun['sunset']))
        door_status = 'closed'

    else:
        print('No action, Time: %s' % str(t), 'Sunrise: %s' % str(sun['sunrise']), 'Sunset:  %s' % str(sun['sunset']))

# Move time and date out of main function so we can change it during testing.


# Tests
pt = pytz.timezone('America/Los_Angeles')

l = [[datetime.datetime.now(pytz.utc), datetime.date.today()],
    # UTC With daylight savings, evening and morning
    [datetime.datetime(2018, 06, 23, 3, 0, 0, tzinfo=pytz.utc), datetime.date(2018, 06, 22)],
    [datetime.datetime(2018, 06, 23, 5, 0, 0, tzinfo=pytz.utc), datetime.date(2018, 06, 22)],
    [datetime.datetime(2018, 06, 23, 11, 0, 0, tzinfo=pytz.utc), datetime.date(2018, 06, 23)],
    [datetime.datetime(2018, 06, 23, 13, 0, 0, tzinfo=pytz.utc), datetime.date(2018, 06, 23)],
    # UTC Without daylight savings, evening and morning
    [datetime.datetime(2018, 12, 23, 0, 0, 0, tzinfo=pytz.utc), datetime.date(2018, 12, 22)],
    [datetime.datetime(2018, 12, 23, 2, 0, 0, tzinfo=pytz.utc), datetime.date(2018, 12, 22)],
    [datetime.datetime(2018, 12, 23, 14, 0, 0, tzinfo=pytz.utc), datetime.date(2018, 12, 23)],
    [datetime.datetime(2018, 12, 23, 16, 0, 0, tzinfo=pytz.utc), datetime.date(2018, 12, 23)],
    # Naive PT With daylight savings, morning and evening
    [datetime.datetime(2018, 06, 23, 5, 0, 0), datetime.date(2018, 06, 23)],
    [datetime.datetime(2018, 06, 23, 7, 0, 0), datetime.date(2018, 06, 23)],
    [datetime.datetime(2018, 06, 23, 19, 0, 0), datetime.date(2018, 06, 23)],
    [datetime.datetime(2018, 06, 23, 21, 0, 0), datetime.date(2018, 06, 23)],
    # Naive PT Without daylight savings, morning and evening
    [datetime.datetime(2018, 12, 23, 6, 0, 0), datetime.date(2018, 12, 23)],
    [datetime.datetime(2018, 12, 23, 8, 0, 0), datetime.date(2018, 12, 23)],
    [datetime.datetime(2018, 12, 23, 16, 0, 0), datetime.date(2018, 12, 23)],
    [datetime.datetime(2018, 12, 23, 18, 0, 0), datetime.date(2018, 12, 23)]
]


def test_timing(l):
    for dt in l:
        ut = dt[0]
        today = dt[1]
        if ut.tzinfo:
            t = ut.astimezone(pt)
        else:
            t = pt.localize(ut)
        main(t, today)

test_timing(l)
