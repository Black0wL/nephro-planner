__author__ = "Christophe"

from Utils.parameters import Parameters
from Utils.constants import Constants
from Utils.database import Database
from Enums.activity import Activity
import sqlite3
# from dateutil import rrule
# from datetime import datetime, timedelta


class Nephrologist(object):
    counters_template = {
        Activity.NEPHROLOGY.name: 0,
        Activity.DIALYSIS.name: 0,
        Activity.CONSULTATION.name: 0,
        Activity.OTHERS.name: 0,
        Activity.OBLIGATION.name: 0,
        Activity.OBLIGATION_HOLIDAY.name: 0,
        Activity.OBLIGATION_WEEKEND.name: 0
    }
    # holidays = []  # contains all personal off days (datetime)
    # preferences = {}  # contains all personal preferences that bind a physician to a TimeSlot and a particular activity

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
    @property
    def team(cls):
        if not cls._team:
            cls._team = {}
            with Parameters() as params, sqlite3.connect(params.data[Constants.DATABASE_FILENAME_KEY]) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM {}".format(Database.DATABASE_TABLE_NEPHROLOGISTS))
                if cursor.rowcount > 0:
                    for row in cursor.fetchmany():
                        cls._team[row[0]] = Nephrologist(row[0], row[1])
        return cls._team

# print([x for x in Nephrologist.effortWeightCountersTemplate.keys()])