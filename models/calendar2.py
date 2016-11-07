'''
Second build of the calendar

Taking advantage of the fact that collection updates are atomic will reduce
concurrency issues.

Breaking the months into days isn't anticipated to put too much extra load on
the database.
'''
from settings import availability_coll

# Map ints into day shortnames - uses calendar's convention that monday is a 0
daynames = {
        0: 'mon',
        1: 'tue',
        2: 'wed',
        3: 'thur',
        4: 'fri',
        5: 'sat',
        6: 'sun'
}


def availablity_for(coach_id, start, end):


class CalendarDay(object):

    def __init__(self, coach_id, year, month, day):
        if availability_coll.findOne

