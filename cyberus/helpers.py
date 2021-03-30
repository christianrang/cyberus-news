"""
Modularly built helper functions
"""

def get_epoch_time(date_obj: object):
    import time
    from datetime import datetime, date

    # time_ = date(year, month, day)
    epoch_time = time.mktime(date_obj.timetuple())
    return epoch_time

def get_day_of_week(date_obj: object, day_: str):
    """
    Args:
        date_obj    (:obj: `datetime.datetime`):    datetime.datetime object describing a date in the week
    """
    from datetime import datetime, timedelta

    days = {
        'monday':       0,
        'tuesday':      1,
        'wednesday':    2,
        'thursday':     3,
        'friday':       4,
        'satday':       5,
        'sunday':       6,
    }

    start_of_week = date_obj - timedelta(days=date_obj.weekday())
    day_of_week = start_of_week + timedelta(days=days[day_.lower()])
    return day_of_week