'''
Base class that represents a user of the system
'''
from models.base_document import BaseDocument

class User(BaseDocument):

    fields = ('firstname', 'lastname', 'email', 'tzname')

    def __init__(self, email, **kwargs):
        kwargs['email'] = email

        BaseDocument.__init__(self, email, **kwargs)

    @property
    def display_name(self):
        return '{first} {last}'.format(first=self['firstname'],
        last=self['lastname'])
