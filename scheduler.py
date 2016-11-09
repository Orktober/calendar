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

# Useful constants
ONE_WEEK = datetime.timedelta(days=7)

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

def get_availability_range(startdate, enddate):
    '''
    Gets availability between two dates
    '''
    # If the range spans multiple months
    pass



def get_monthly_availability(coach, customer_time, week_offset):
    '''
    Gets availability for the whole month
    '''
    pass



def get_weekly_availability(coach, customer_time, week_offset):
    '''
    customer time is current time in customer timezone
    take that time, set it to the beginning of this week, and add 7*weeks_offset
    to get the week that the customer has requested
    '''

    # todo see if customer's time is past coach's last time for today, aand if
    # this is the last day of the week - advance one week
    weekday = customer_time.weekday()

    # This delta will create a datetime that's at the beginning of week N
    # Adjust by an additional day to display sunday-saturday
    start_delta = datetime.timedelta(days=(-1 *weekday) - 1 + (7*week_offset))

    start = customer_time + start_delta
    end = start + ONE_WEEK
    return CalendarDay.all_availability_in_range(start, end, coach)



@app.route('/appt/<customerid>')
def home(customerid):
    return redirect(url_for('appointment_page', customerid=customerid, offset=0))

@app.route('/appt/<customerid>/<int:offset>')
def appointment_page(customerid, offset):
    '''
    This endpoint
    - look up coach for user
    - get month, year
    - see if coach and user are in different timezones
    '''

    customer = Customer(customerid)
    coach = customer.get_coach()
    if not coach:
        return redirect(url_for('unrecognized_user'))

    now = time_utils.utcnow()
    customer_time = customer.to_timezone(now)

    days = get_weekly_availability(coach['email'], customer_time, offset)

    return render_template(
        'reservation_base.html',
        customer=customer,
        coach=coach,
        days=days,
        offset=offset
    )

@app.route('/book/<_id>/<customer>/<int:slot>')
def book(_id, customer, slot):
    c = CalendarDay.lookup_by_id(_id)
    success = c.book(customer, slot)
    if success:
        return redirect(url_for('home', customerid=customer))
    else:
        # Would like to give the user better feedback in the future
        return redirect(url_for('home', customerid=customer))


@app.route('/unbook/<_id>/<customer>/<int:slot>')
def unbook(_id, customer, slot):
    success = CalendarDay.lookup_by_id(_id).unbook(slot)
    return redirect(url_for('home', customerid=customer, error=True))

if __name__ == '__main__':
    app.run(debug=True)


