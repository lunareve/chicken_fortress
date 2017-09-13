"""Turns switches on and off on raspberry pi according to time of day."""

import datetime
from astral import Astral

def on_off():
    """toggles the switch"""
    pass

def timer(city_name):
    """determines when sunrise and sunset are"""
    a = Astral()
    a.solar_depression = 'nautical'
    city = a[city_name]
    sun = city.sun()
    print('Sunrise: %s' % str(sun['sunrise']))
    print('Sunset:  %s' % str(sun['sunset']))
    print('Dusk: %s' % str(sun['dusk']))

timer('San Francisco')