__author__ = "Christophe"

from Utils.parameters import Parameters
from Utils.constants import Constants
from Utils.database import Database
import sqlite3


class Nephrologist(object):
    def __init__(self, _id, _name, _holidays=None, _preferences=None):
        self.id = _id
        self.name = _name
        if _holidays: # contains all personal off days (datetime)
            self.holidays = _holidays
        if _preferences: # contains all personal preferences that bind a nephrologist to a TimeSlot and a particular activity
            self.preferences = _preferences

    def __str__(self):
        return super(self)

    def __repr__(self):
        return self.__str__()

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