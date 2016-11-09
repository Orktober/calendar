'''
Utilities for interacting with time.
'''
import pytz
import datetime

def utcnow():
    '''Helper that gets the current time, with timezone information'''
    return datetime.datetime.now(tz=pytz.utc)

def totz(t, tz):
    return t.aszimezone(tz)

def is_valid_timezone(tzname):
    return tzname in pytz.all_timezones
