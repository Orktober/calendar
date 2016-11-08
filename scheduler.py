'''
The entrypoint for the scheduler app.
'''
import pytz
import config
import datetime
import time_utils

from flask import Flask, render_template, redirect, url_for
from utils import to_display_month

from models.booking_calendar_2 import CalendarDay
from models.coach import Coach
from models.customer import Customer


app = Flask(__name__)


# Some systems / redirects that I assume would exist
# If the user is unrecognized, redirect them to a signup page
@app.route('/signup')
def signup_user():
    return render_template('signup_user.html')

# If the user clicks on the "Need help?" link, redirect to a dummy help page
@app.route('/help')
def help():
    return render_template('help.html')

# If the user clicks on the timezone explanation page
@app.route('/help/timezone')
def timezone_help():
    return render_template('timezone.html')

def get_availability(coach_id, customer_time, week_offset):
    '''
    customer time is current time in customer timezone
    take that time, set it to the beginning of this week, and add 7*weeks_offset
    to get the week that the customer has requested
    '''

    appointments = []
    # todo see if customer's time is past coach's last time for today, aand if
    # this is the last day of the week - advance one week
    customer_date = customer_time.date()

    weekday = customer_date.weekday()
    delta = datetime.timedelta(days=(-1 *weekday) + (7*week_offset))
    beginning_of_week = customer_date + delta
    ptr = beginning_of_week
    one_day = datetime.timedelta(days=1)
    for i in range(7):
        appointments.append(CalendarDay(coach_id, ptr.year, ptr.month, ptr.day))
        ptr += one_day
    return appointments

DISPLAY_TIMES = [
    'Midnight',
    '1 AM',
    '2 AM',
    '3 AM',
    '4 AM',
    '5 AM',
    '6 AM',
    '7 AM',
    '8 AM',
    '9 AM',
    '10 AM',
    '11 AM',
    'Noon',
    '1 PM',
    '2 PM',
    '3 PM',
    '4 PM',
    '5 PM',
    '6 PM',
    '7 PM',
    '8 PM',
    '9 PM',
    '10 PM',
    '11 PM',
    'Midnight'
    ]
def get_display_times(cust_time, coach_time):
    '''
    Customer is reserving times in their own timezone.

    Coach is available from 9-5 in their own timezone.

    Bookable times are [9..5] + (customer timezone - coach timezone)
    '''
    offset = get_timezone_offset(cust_time, coach_time)
    return DISPLAY_TIMES[9-offset:17-offset]

def get_timezone_offset(t1, t2):
    delta = t1 - t2
    return int(delta.days * 24 + delta.seconds / 3600)



@app.route('/appointment/<customer_id>/<int:offset>')
def appointment_page(customer_id, offset):
    '''
    This endpoint
    - look up coach for user
    - get month, year
    - see if coach and user are in different timezones
    '''

    customer = Customer(customer_id)
    coach    = customer.get_coach()
    if not coach:
        return redirect(url_for('unrecognized_user'))

    coachname = coach.display_name

    customername = customer.display_name
    customeremail = customer['email']

    now = time_utils.utcnow()
    month = now.month
    year = now.year

    customer_time = customer.to_timezone(now)
    coach_time = coach.to_timezone(now)
    hours = get_display_times(customer_time, coach_time)
    days = get_availability(coach['email'], customer_time, offset)

    tz_different = (coach['tzname'] != customer ['tzname'])
    return render_template(
        'reservation_base.html',
        customername=customername,
        customer_id=customer_id,
        customeremail=customeremail,
        coach_id=coach['email'],
        coachname=coachname,
        month=to_display_month(month),
        year=year,
        tz_different=tz_different,
        hours=hours,
        days=days,
        offset=offset
    )

@app.route('/book/<coach_id>/<customer_id>/<int:year>/<int:month>/<int:day>/<int:slot>')
def book(coach_id, customer_id, year, month, day, slot):
    print(year)
    print(month)
    print(day)
    print(coach_id)
    c = CalendarDay(coach_id, year, month, day)
    c.book(customer_id, slot)
    return redirect(url_for('index', customer_id=customer_id))

@app.route('/unbook/<coach_id>/<customer_id>/<int:year>/<int:month>/<int:day>/<int:slot>')
def unbook(coach_id, customer_id, year, month, day, slot):
    print(year)
    print(month)
    print(day)
    print(coach_id)
    c = CalendarDay(coach_id, year, month, day)
    c.unbook(customer_id, slot)
    return redirect(url_for('index', customer_id=customer_id))

if __name__ == '__main__':
    app.run(debug=True)


