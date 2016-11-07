'''
Utilities for interacting with time.

The main goal of this class is to abstract away timezone issues as much as
possible.

All times are in UTC, until they must be displayed to the end user.
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
