'''
Contains the various connections for the app
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
calendar_coll = db[config.get('CALENDAR_COLL')]
holiday_coll  = db[config.get('HOLIDAY_COLL')]
availability_coll = db[config.get('AVAILABILITY_COLL')]
