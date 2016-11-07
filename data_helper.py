'''
A utility to create db objects.

Most of these functions are meant to be called from the python interpreter
directly.
'''
import datetime

from pytz import timezone
from time_utils import is_valid_timezone
from models.coach import Coach
from models.customer import Customer


def create_coach(email, firstname, lastname, tz, availibility):
    if not is_valid_timezone(tz):
        raise Exception('Timezone {tz} is not a recognized timezone', tz)

    c = Coach(email, firstname=firstname, lastname=lastname, tzname=tz)
    c.save()

def create_customer(email, firstname, lastname, tz, customer_from, coach_id):
    if not is_valid_timezone(tz):
        raise Exception('Timezone {tz} is not a recognized timezone', tz)

    # For the simple data set, customers are valid for one year
    customer_to = customer_from + datetime.timedelta(days=365)

    c = Customer(email, firstname=firstname, lastname=lastname, tzname=tz,
           customer_from=customer_from, customer_to=customer_to,
           coach_id=coach_id)
    c.save()

