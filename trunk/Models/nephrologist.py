__author__ = "Christophe"

from Utils.parameters import Parameters
from Utils.constants import Constants
from Utils.database import Database
from Enums.activity import Activity
import sqlite3


class Nephrologist(object):
    def __init__(self, _id, _name, _activities=Activity.highest(), _holidays=None, _preferences=None, _aversions=None):
        if not _id:
            raise UserWarning("id can not be None.")
        elif not isinstance(_id, int):
            raise UserWarning("id must be of type {}".format(int))
        self.id = _id

        if not _name:
            raise UserWarning("name can not be None.")
        elif not isinstance(_name, str):
            raise UserWarning("name must be of type {}".format(str))
        self.name = _name

        if not _activities:
            raise UserWarning("activities can not be None.")
        elif not isinstance(_activities, list):
            raise UserWarning("activities must be of type {}".format(list))
        self.activities = _activities if _activities else [Activity.NONE]  # the activities the nephrologist can be allocated on

        if _holidays and not isinstance(_holidays, list):
            raise UserWarning("holidays should be of type {}".format(list))
        self.holidays = _holidays if _holidays else []  # contains all personal off days (datetime)

        if _preferences and not isinstance(_preferences, dict):
            raise UserWarning("preferences should be of type {}".format(dict))
        self.preferences = _preferences if _preferences else {}  # contains all personal preferences that bind a nephrologist to a TimeSlot and a particular activity

        if _aversions and not isinstance(_aversions, dict):
            raise UserWarning("aversions should be of type {}".format(dict))
        self.aversions = _aversions if _aversions else {}  # contains all personal aversions that a nephrologist has to a TimeSlot and a particular activity

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