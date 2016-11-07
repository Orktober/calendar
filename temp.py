import datetime
import data_helper

year_begin = datetime.datetime(2016, 1, 1)
data_helper.create_customer('brett.favre@example.com', 'Brett', 'Favre',
        'US/Eastern', year_begin, 'mike.holmgren@company.com')

data_helper.create_customer('aaron.rodgers@example.com', 'Aaron', 'Rodgers',
        'US/Eastern', year_begin, 'mike.holmgren@company.com')

data_helper.create_coach('mike.holmgren@company.com', 'Mike', 'Holmgren',
        'US/Pacific', [True, True, True, True, True, False, False])
