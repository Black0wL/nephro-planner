__author__ = "Christophe"

import sqlite3
from Utils.parameters import Parameters
from utils.constants import Constants
# from dateutil import rrule
# from datetime import datetime, timedelta


class Nephrologist(object):
    effortWeightCountersTemplate = {
        'NEPHROLOGY': 0,
        'DIALYSIS': 0,
        'CONSULTATION': 0,
        'OBLIGATION': 0,
        'OTHERS': 0,
        'OBLIGATION_HOLIDAY': 0,
        'OBLIGATION_WEEKEND': 0
    }
    team = {}  # contains #key=id, #value=nephrologist
    offDays = []  # contains all personal off days (datetime)
    allocations = {}  # contains all personal allocations that bind a physician to a TimeSlot and a particular activity
    preferences = {}  # contains all personal preferences that bind a physician to a TimeSlot and a particular activity

    def __init__(self, _id, _name, _offdays=None, _allocations=None, _preferences=None, _counters=None):
        self.id = _id
        self.name = _name
        if _offdays:
            self.offDays = _offdays
        if _allocations:
            self.allocations = _allocations
        if _preferences:
            self.preferences = _preferences
        if _counters:
            self.counters = _counters

    def __str__(self):
        return super(self)

    def __repr__(self):
        return self.__str__()

    @classmethod
    def __load__(cls):
        with Parameters() as params, sqlite3.connect(params.data[Constants.DATABASE_FILENAME_KEY]) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM {}".format(Constants.DATABASE_TABLE_NEPHROLOGISTS))
            if cursor.rowcount == 0:


            connection.execute('''CREATE TABLE IF NOT EXISTS monthlyPlannings (
                month TEXT NOT NULL,
                version INTEGER NOT NULL,
                isReleasedVersion INTEGER NULL,
                PRIMARY KEY (month ASC, version ASC)
            )''')
        pass