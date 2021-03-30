# Python imports
import requests
import datetime
import json

# Internal Project imports
from helpers import get_day_of_week, get_epoch_time

def get_epoch_week(date_ = datetime.datetime.now()):
    """
    Gets the start and end of the week in epoch
    """
    start_week  = get_day_of_week(date_, 'monday')
    end_week    = get_day_of_week(date_, 'sunday')

    return get_epoch_time(start_week), get_epoch_time(end_week)

def get_ctfs_in_timeframe(url: object, start: str, end: str, limit=10):
    headers={
        # No clue why but without this you will get a 403
        'Host':         'ctftime.org',
        'user-agent':   'curl',
    }

    params = {
        'limit':    str(limit),
        'start':    str(start),
        'finish':   str(end),
    }

    return requests.get(url, params=params, headers=headers)

def get_ctfs_this_week():
    start_week, end_week = get_epoch_week()

    url = URL(
        protocol        = 'https', 
        domain          = 'ctftime', 
        generic_domain  = 'org', 
        path            = '/api/v1/events/'
        )

    start   = str(start_week).split('.')[0]
    end     = str(end_week).split('.')[0]

    return get_ctfs_in_timeframe(url=url, start=start, end=end)


class URL():

    def __init__(self, protocol: str, domain: str, generic_domain: str, path: str):
        self.protocol       = protocol
        self.domain         = domain
        self.generic_domain = generic_domain
        self.path           = path

    def __str__(self):
        return self.protocol + "://" + '.'.join([self.domain, self.generic_domain]) + self.path
    
class CTF():

    def __init__(self, title: str, description: str, url: str, ctftime_url: str):
        self. title         = title
        self.description    = description
        self.url            = url
        self.ctftime_url    = ctftime_url
    
    


if __name__ == '__main__':
    response = get_ctfs_this_week()
    print(json.dumps(response.json()))