__author__ = "Christophe"

from Utils.parameters import Parameters
from Utils.constants import Constants
from Utils.database import Database
from Enums.activity import Activity
import sqlite3
# from dateutil import rrule
# from datetime import datetime, timedelta


class Nephrologist(object):
    effortWeightCountersTemplate = {
        Activity.NEPHROLOGY.name: 0,
        Activity.DIALYSIS.name: 0,
        Activity.CONSULTATION.name: 0,
        Activity.OTHERS.name: 0,
        Activity.OBLIGATION.name: 0,
        Activity.OBLIGATION_HOLIDAY.name: 0,
        Activity.OBLIGATION_WEEKEND.name: 0
    }
    # offDays = []  # contains all personal off days (datetime)
    # allocations = {}  # contains all personal allocations that bind a physician to a TimeSlot and a particular activity
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
    def __load__(cls):
        with Parameters() as params, sqlite3.connect(params.data[Constants.DATABASE_FILENAME_KEY]) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM {}".format(Database.DATABASE_TABLE_NEPHROLOGISTS))
            if cursor.rowcount == 0:
                cursor.executemany('INSERT INTO {}(id_pk, name) VALUES (?,?)'.format(
                    Database.DATABASE_TABLE_NEPHROLOGISTS
                ), [
                    Nephrologist(1, "Sandrine"),
                    Nephrologist(2, "Christine"),
                    Nephrologist(3, "Severine")
                ].__iter__())
        pass

# print([x for x in Nephrologist.effortWeightCountersTemplate.keys()])