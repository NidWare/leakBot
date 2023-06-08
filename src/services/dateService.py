import random
import datetime

def random_date():
    start_date = datetime.datetime(2014, 1, 1)
    end_date = datetime.datetime.now()
    time_between_dates = end_date - start_date
    random_number_of_days = random.randrange(time_between_dates.days)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    random_time = datetime.time(random.randint(0, 23), random.randint(0, 59), random.randint(0, 59))
    return datetime.datetime.combine(random_date, random_time)
