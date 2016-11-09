'''
Represents a single customer
'''
import logging

from settings import customer_coll
from models.user import User
from models.coach import Coach

log = logging.getLogger(__name__)

class Customer(User):

    fields = User.fields + ('customer_from', 'customer_to', 'coach_id')
    coll   = customer_coll

    def __init__(self, _id, **kwargs):
        User.__init__(self, _id, **kwargs)

    def get_coach(self):
        '''Returns the coach assigned to this user'''
        if not self['coach_id']:
            log.warn('Customer %s has no coach', self['email'])
            return None
        return Coach(self['coach_id'])



