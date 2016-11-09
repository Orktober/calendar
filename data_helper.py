'''
A utility to create db objects.

When run, this helper will create the sample user data that the app relies on.
'''
import datetime

from pytz import timezone
from time_utils import is_valid_timezone
from models.coach import Coach
from models.customer import Customer


def create_coach(_id, email, firstname, lastname, tz, availability):
    '''Helper to create a coach object'''
    if not is_valid_timezone(tz):
        raise Exception('Timezone {tz} is not a recognized timezone', tz)

    c = Coach(_id, email=email, firstname=firstname, lastname=lastname, tzname=tz,
            availability=availability)
    c.save()

def create_customer(_id, email, firstname, lastname, tz, coach_id):
    '''Helper to create a customer object'''

    if not is_valid_timezone(tz):
        raise Exception('Timezone {tz} is not a recognized timezone', tz)

    # For the simple data set, customers are valid for one year
    customer_from = datetime.datetime(year=2016, month=1, day=1)
    customer_to = customer_from + datetime.timedelta(days=365)

    c = Customer(_id, email=email, firstname=firstname, lastname=lastname, tzname=tz,
            customer_from=customer_from, customer_to=customer_to, coach_id=coach_id)
    c.save()


# Creates 2 sample coaches and 4 sample customers with timezone matches or mismatches
if __name__ == '__main__':
    create_coach('joe', 'joe.smith@company.com', 'Joe', 'Smith', 'US/Eastern', [True, True, True,
        True, True, False, False])
    create_coach('ella', 'ella.firth@company.com', 'Ella', 'Firth', 'US/Pacific', [True] * 7)

    create_customer('zeke', 'zeke@example.com', 'Zeke', 'Bass', 'US/Eastern', 'ella')
    create_customer('buddy', 'buddy@example.com', 'Buddy', 'Guy', 'US/Pacific', 'ella')
    create_customer('perri', 'perri@example.com', 'Perriander', 'Shaw', 'US/Eastern', 'joe')
    create_customer('nora', 'zeke@example.com', 'Nora', 'Oche', 'US/Pacific', 'joe')
