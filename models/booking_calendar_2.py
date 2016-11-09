import pytz
import calendar
import datetime

from bson.objectid import ObjectId
from settings import availability_coll as coll
from models.base_document import BaseDocument
from models.coach import Coach

# The maximum number of appointments per day that a coach can handle
MAX_SLOTS = 8

ONE_DAY = datetime.timedelta(days=1)

class CalendarDay(object):
    '''Represents a single day of a coach's calendar'''

    def __init__(self, coach, date, _id=None, slots=None, locked=False, appt_ct=0):

        # If this object was not prev in db, there will be no id
        if _id is None:
            slots = [None] * MAX_SLOTS
            res = coll.insert_one({
                'coach': coach,
                'date': date,
                'slots': slots,
                'locked': locked,
                'appt_ct': appt_ct
            })
            _id = res.inserted_id


        self.date = date
        self._id = _id
        self.coach = coach
        self.slots = slots
        self.appt_ct = appt_ct

        # Store this for convienence
        self.timezone = Coach(coach)['tzname']

    def update_state(self, data):
        '''Updates this object with possible new data from the db

        The only values that may change are the slots and the appointment
        count (we don't care about the locked state in this object)
        '''
        if 'slots' in data:
            self.slots = data['slots']
        if 'appt_ct' in data:
            self.appt_ct = data['appt_ct']

    def to_dict():
        return {
            '_id': self._id,
            'coach': self.coach,
            'date': self.date,
            'slots': self.slots,
            'locked': self.locked,
            'appt_ct': self.appt_ct
        }

    @property
    def year(self):
        return self.date.year

    @property
    def month(self):
        return self.date.month

    @property
    def day(self):
        return self.date.day

    def display_times_as_timezone(self, tzname):
        '''Converts the times of each slot to a display string in the specified timezone'''
        for i in range(8):
            yield self.display_time_for_slot(tzname, i)

    def display_time_for_slot(self, tzname, slot):
        coach_time = self.get_slot_time(slot)
        return coach_time.astimezone(pytz.timezone(tzname)).strftime('%-I %p %Z')

    def get_slot_time(self, slot):
        tz = self.timezone
        d = self.date

        conv = datetime.datetime(
                year=d.year, month=d.month, day=d.day, hour=9+slot,
                minute=0, second=0

        )
        conv = pytz.timezone(tz).localize(conv)
        return conv

    def available(self, slot):
        slot_time = self.get_slot_time(slot)
        now = datetime.datetime.now(tz=pytz.utc)
        return now < slot_time and self.slots[slot] is None

    def booked_by(self, slot, user):
        return self.slots[slot] == user

    def display_time(self, slot):
        return self.get_slot_time(slot)

    @property
    def display_date(self):
        return self.date.strftime('%a, %b %d')

    def _get_query(self):
        '''Returns the query that can be used to retrieve db data'''
        return {'coach': self.coach, 'date': self.date}

    def book(self, user_id, slot):
        '''Attempts to reserve a spot on a coach's calendar.

        Before an appointment slot is taken, the object is locked to prevent
        concurrent modification.
        '''
        success = True
        # Only returns when the document lock has been acquired
        query = self._get_query()
        data = self.lock_and_query(query)

        # Update our current state
        self.update_state(data)

        if self.slots[slot] is None:
            self.slots[slot] = user_id
            self.appt_ct += 1
            slot_idx = 'slots.%d' % slot

            # Update the db object, unlock
            update = {
                '$set': {
                    slot_idx : user_id,
                    'locked': False,
                },
                '$inc': {'appt_ct': 1}
            }

        else:
            # Someone else got here first - release the lock with no change
            success = False
            update = {
                    '$set': {
                        'locked': False
                        }
                    }
        coll.update_one(query, update)

    def unbook(self, slot):
        '''Removes a user from a coach's calendar'''

        # The specific position in the slot array to unbook
        slot_idx = 'slots.%d' % slot
        query = self._get_query()
        update = {'$unset': {slot_idx:None}, '$inc': {'appt_ct': -1}}

        # Should be no reason no lock the database here
        data = coll.find_one_and_update(query, update)
        self.update_state(data)

        return True

    def lock_and_query(self, query):
        '''Uses an atomic update to lock the document and return the current
        state of the document from the db'''
        retries_left = 5
        op    = {'$set': {'locked': True}}

        data = coll.find_one_and_update(query, op)

        # If the data is locked, try again
        while data['locked'] is True:
            data = coll.find_one_and_update(query, op)
            retries_left -= 1

            if retries_left is 0:
                raise IOError('Could not get object lock')

        return data

    @staticmethod
    def all_availability_in_range(_from, to, coach):
        '''Gets a range of availability from the from date (inclusive) to the to date.  '''

        # Due to a limitation in the mongodb driver, instead of using the more intuitive 'date'
        # object, we have to use a datetime with hours, min, secs set to 0
        _from = datetime.datetime(year=_from.year, month=_from.month, day=_from.day)
        to = datetime.datetime(year=to.year, month=to.month, day=to.day)

        availabilities = []
        while _from < to:
            query = { 'date': {'$eq' : _from }, 'coach' : {'$eq': coach}}
            data  = coll.find_one(query, projection={'coach': 0, 'date': 0})
            if not data:
                data = {}
            availabilities.append(CalendarDay(coach, _from, **data))
            _from += ONE_DAY

        return availabilities

    @staticmethod
    def lookup_by_id(_id):
        data = coll.find_one({'_id': ObjectId(_id)})
        if data:
            return CalendarDay(data['coach'], data['date'], _id=data['_id'], slots=data['slots'],
                    locked=data['slots'], appt_ct=data['appt_ct'])





