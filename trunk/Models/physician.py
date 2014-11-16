__author__ = "Christophe"

import time
import json
from Models.Enums.activity import Activity
# from dateutil import rrule
# from datetime import datetime, timedelta

class Physician(object):
    effortWeightCountersTemplate = {
        'NEPHROLOGY' : 0,
        'DIALYSIS' : 0,
        'CONSULTATION' : 0,
        'OBLIGATION' : 0,
        'OTHERS' : 0,
        'OBLIGATION_HOLIDAY' : 0,
        'OBLIGATION_WEEKEND' : 0
    }
    offDays = []  # contains all personal off days (datetime)
    allocations = {} # contains all personal allocations that bind a physician to a timeslot and a particular activity
    preferences = {} # contains all personal preferences that bind a physician to a timeslot and a particular activity

    def __init__(self, _id, _name, _offDays = None, _allocations = None, _preferences = None, _counters = None):
        self.id = _id
        self.name = _name
        if _offDays is not None:
            self.offDays = _offDays
        if _allocations is not None:
            self.allocations = _allocations
        if _preferences is not None:
            self.preferences = _preferences
        if _counters is not None:
            self.counters = _counters

    def __str__(self):
        return super(self)

    def __repr__(self):
        return self.__str__()