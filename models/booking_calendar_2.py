import calendar

from utils import to_display_month
from settings import availability_coll
from models.base_document import BaseDocument

# The maximum number of appointments per day that a coach can handle
MAX_SLOTS = 8

class CalendarDay(object):
    '''Represents a single day of a coach's calendar'''

    def __init__(self, coach_id, year, month, day):

        query = {
            'coach_id': coach_id,
            'year': year,
            'month': month,
            'day': day
        }

        # Pull any matching object from the database
        data = availability_coll.find_one(query)

        # If no matching object, create a default object
        if not data:
            data = self.create_day(coach_id, year, month, day)

        self._id = data.get('_id')
        self.year     = year
        self.month    = month
        self.day      = day
        self.coach_id = coach_id
        self.slots    = data['slots']
        self.appointments = data['appointments']

    @property
    def available(self):
        return self.appointments != MAX_SLOTS

    @property
    def display_date(self):
        monthname = to_display_month(self.month)
        return '{m} {d}'.format(m=monthname, d=self.day)

    def create_day(self, coach_id, year, month, day):

        #month_start, num_days = calendar.monthrange(year, month)

        _id = '%s_%s_%s_%s' % (coach_id, year, month, day)
        print(_id)
        data = {
            '_id': _id,
            'year': year,
            'month': month,
            'day': day,
            'coach_id': coach_id,
            'slots': [None] * 8,
            'locked': False,
            'appointments': 0

        }
        availability_coll.insert(data)
        return data

    def book(self, user_id, slot):
        '''Attempts to reserve a spot on a coach's calendar.

        Before an appointment slot is taken, the object is locked to prevent
        concurrent modification.
        '''
        query = {'_id': self._id}
        data = self.lock_and_query()

        # Update our current state
        self.slots = data['slots']
        self.appointments = data['appointments']

        if self.slots[slot] is None:
            self.slots[slot] = user_id
            self.appointments += 1
            field = 'slots.%d' % slot
            # Update the field directly in the database
            update = {
                '$set': {
                    field: user_id,
                    'locked': False,
                    'appointments': self.appointments
                }
            }
            availability_coll.update_one(query, update)
            return True
        else:
            # Release the lock with no change
            update = {'$set': {'locked': False}}
            availability_coll.update_one(query, update)
            return False

    def unbook(self, user_id, slot):
        '''Removes a user from a coach's calendar'''

        self.appointments -= 1

        # The specific position in the slot array to unbook
        field  = 'slots.%d' % slot
        query  = {'_id': self._id}
        update = {'$unset': {field:None}, 'appointments': self.appointments}

        # Should be no reason no lock the database here
        availability_coll.find_one_and_update(query, update)
        return True

    def lock_and_query(self):
        '''Uses an atomic update to lock the document and return the current
        state of the document from the db'''
        query = {'_id': self._id}
        op    = {'$set': {'locked': True}}

        data = availability_coll.find_one_and_update(query, op)

        # If the data is locked, try again
        while data['locked'] is True:
            data = availability_coll.find_one_and_update(query, op)
        return data


