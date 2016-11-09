'''
This file is used to set up connections or objects that will be shared
throughout the app.

For the calendar application, this is mainly database / collection objs.
'''
import pymongo

from config import config

# Mongo Client
my_client = pymongo.MongoClient(config.get('MONGO_URI'))

# Root database
db = my_client[config.get('APP_DB')]

# Various collections for server obejects
coach_coll    = db[config.get('COACH_COLL')]
customer_coll = db[config.get('CUSTOMER_COLL')]
availability_coll = db[config.get('AVAILABILITY_COLL')]
