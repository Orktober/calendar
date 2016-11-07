'''
This class contains utilities for interacting with the calendar object
'''
import calendar
from settings import availability_coll
from models.base_document import BaseDocument


class CalendarDay(object):
    '''Represents a single month of a coach's calendar'''

    def __init__(self, coach_id, year, month, day):

        query = {'coach_id': coach_id, 'month': month, 'year': year, 'day': day}
        print(query)
        data = availability_coll.find_one(query)

        if not data:
            data = self.create_day(coach_id, year, month, day)

        self._id = data.get('_id')
        self.year     = year
        self.month    = month
        self.day      = day
        self.coach_id = coach_id
        self.slots    = data['slots']

    def create_day(self, coach_id, year, month, day):
        # Returns the starting day, and number of days of of the year,month
        # combo - this method correctly accounts for leap years

        month_start, num_days = calendar.monthrange(year, month)

        # Set the id ourselves, why not
        _id = '%s_%s_%s_%s' % (coach_id, year, month, day)
        print(_id)
        data = {
            '_id': _id,
            'year': year,
            'month': month,
            'day': day,
            'coach_id': coach_id,
            'slots': [None] * 8,
            'locked': False

        }
        availability_coll.insert(data)
        return data

    def book(self, user_id, slot):
        query = {'_id': self._id}
        status = self.slots[slot] = user_id
        field = 'slots.%d' % slot
        data = self.lock()
        if data['slots'][slot] is None:
            update = {'$set': {field: user_id, 'locked': False}}
            availability_coll.update_one(query,  update)
            return True
        else:
            update = {'$set': {'locked': False}}
            availability_coll.update_one(query,  update)
            return False

    def unbook(self, user_id, slot):

        status = self.slots[slot] = user_id
        field = 'slots.%d' % slot
        update = {'$unset': {field:None}}
        print(availability_coll.find_one_and_update({'_id':self._id}, update))
        return True

    def lock(self):
        ''' Waits until the document is available before updating it'''
        query = {'$set': {'locked': True}}
        data = availability_coll.find_one_and_update({'_id': self._id}, query)
        print(data)
        while data['locked'] is True:
            data = availability_coll.find_one_and_update({'_id': self._id}, query)
        return data


