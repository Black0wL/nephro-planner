__author__ = "Christophe"

from Utils.parameters import Parameters
from Utils.constants import Constants
from Utils.database import Database
from Enums.activity import Activity
import sqlite3


class Nephrologist(object):
    def __init__(self, _id, _name, _activities=Activity.highest(), _holidays=None, _preferences=None):
        self.id = _id
        self.name = _name
        self.activities = _activities if _activities else 0  # the activities the nephrologist can be allocated on
        self.holidays = _holidays if _holidays else []  # contains all personal off days (datetime)
        self.preferences = _preferences if _preferences else []  # contains all personal preferences that bind a nephrologist to a TimeSlot and a particular activity

    def __str__(self):
        return super(self)

    def __repr__(self):
        return self.__str__()

    # TODO: load activities, holidays, preferences from DB
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