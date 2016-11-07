'''
Base object that controls interaction with the database.

Gives objects that extend this object automatic saving capability.
'''
import logging
log = logging.getLogger(__name__)

class BaseDocument(object):

    # Extending classes are expected to provide a collection
    coll = None

    # Extending classes will provide a list of fields on the object
    fields = None


    def __init__(self, _id, **kwargs):
        '''This class will load the requested id from the backing db.
        If there is no match, this is a new object'''
        self.data = {}
        self._id  = _id

        # Pull in any state from the database
        self.load(_id)

        # Add in any other params
        for k, v in kwargs.items():
            self[k] = v

        # Explicitly save the _id property
        self.data['_id'] = _id

    def __setitem__(self, key, val):
        self.data[key] = val

    def __getitem__(self, key):
        return self.data.get(key)

    def load(self, _id):
        '''Load state from the database; any property not in database is
        set to None'''
        data = self.coll.find_one({'_id': _id})
        if not data:
            data = {f: None for f in self.fields}

        self.data = data

    def save(self):
        ''' Save all state to the backing collection '''
        self.data['_id'] = self._id

        try:
            self.coll.replace_one({'_id' : self._id}, self.data, upsert=True)
            return True
        except:
            log.exception('Could not save object')
        return False


