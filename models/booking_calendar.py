'''
This class contains utilities for interacting with the calendar object
'''
import calendar
from settings import calendar_coll
from models.base_document import BaseDocument


class CalendarMonth(object):
    '''Represents a single month of a coach's calendar'''
    fields = ('month_start', 'num_days', 'month', 'year', 'coach_id')
    coll   = calendar_coll

    def __init__(self, coach_id, month, year):

        query = {'coach_id': coach_id, 'month': month, 'year': year}
        data = calendar_coll.find_one(query)

        if not data:
            data = self.create_calendar_month(coach_id, month, year)

        self._id = data.get('_id')
        self.bookable_days     = data.get('bookable_days')
        self.month_start = data.get('month_start')
        self.num_days = data.get('num_days')
        self.month    = month
        self.year     = year
        self.coach_id = coach_id


    def create_calendar_month(self, coach_id, month, year):
        # Returns the starting day, and number of days of of the year,month
        # combo - this method correctly accounts for leap years

        month_start, num_days = calendar.monthrange(year, month)

        # Set the id ourselves, why not
        _id = '%s_%s_%s' % (coach_id, month, year)
        print(_id)
        data = {
            '_id': _id,
            'month': month,
            'year': year,
            'coach_id': coach_id,
            'month_start': month_start,
            'num_days': num_days,
            'bookable_days': {str(d): [None] * 8 for d in range(num_days)}
        }
        calendar_coll.insert(data)
        return data

    def make_appointment(self, user_id, day,slot):

        status = self['appointments'][day][slot] = user_id
        self.save()
        return True

