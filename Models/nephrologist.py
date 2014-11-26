__author__ = "Christophe"

from Utils.parameters import Parameters
from Utils.constants import Constants
from Utils.database import Database
from Enums.activity import Activity
from Enums.timeslot import TimeSlot
from Models.perioder import Perioder
from datetime import timedelta
import sqlite3
import calendar


class Nephrologist(object):
    """ mapper between discrete time slots and analogous datetime

        FIRST_SHIFT: from 05:00:00 to 12:59:59.999999
        SECOND_SHIFT: from 13:00:00 to 20:59:59.999999
        SECOND_SHIFT: from 21:00:00 to 04:59:59.999999
    """
    slots_temporally = {
        TimeSlot.FIRST_SHIFT.name: Perioder(
            _lower_delta=timedelta(hours=5),
            _progressive_period=timedelta(days=1),
            _upper_delta=timedelta(hours=13, microseconds=-1)
        ),
        TimeSlot.SECOND_SHIFT.name: Perioder(
            _lower_delta=timedelta(hours=13),
            _progressive_period=timedelta(days=1),
            _upper_delta=timedelta(hours=21, microseconds=-1)
        ),
        TimeSlot.THIRD_SHIFT.name: Perioder(
            _lower_delta=timedelta(hours=21),
            _progressive_period=timedelta(days=1),
            _upper_delta=timedelta(days=1, hours=5, microseconds=-1)
        )
    }

    """ constructor of the class

        @param _id: unique identifier of a nephrologist.
        @type _id: int
        @param _name: unique humanized identifier of a nephrologist.
        @type _name: str
        @param _activities: activities a nephrologist can be allocated on.
        @type _activities: list
        @param _holidays: holidays or recovery days of a nephrologist
        @type _holidays: list
        @param _preferences: preferential working time slot/activity combination for a nephrologist
        @type _preferences: dict
        @param _aversions: preferred not time slot/activity combination for a nephrologist
        @type _aversions: dict
    """
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
        # the activities the nephrologist can be allocated on
        self.activities = _activities if _activities else [Activity.NONE]

        if _holidays and not isinstance(_holidays, list):
            raise UserWarning("holidays should be of type {}".format(list))
        self.holidays = _holidays if _holidays else []  # contains all personal off days (datetime)

        if _preferences and not isinstance(_preferences, dict):
            raise UserWarning("preferences should be of type {}".format(dict))
        # contains all personal preferences that bind a nephrologist to a TimeSlot and a particular activity
        self.preferences = _preferences if _preferences else {}

        if _aversions and not isinstance(_aversions, dict):
            raise UserWarning("aversions should be of type {}".format(dict))
        # contains all personal aversions that a nephrologist has to a TimeSlot and a particular activity
        self.aversions = _aversions if _aversions else {}

    def __holidays__(self, _month, _year):
        # TODO: purpose is to provide a map { day_number: [off_time_slots]} for current {year, month}
        # eliminating 0-es provided by calendar.monthcalendar...
        for _perioder in self.holidays:
            # for _week in [x for x in calendar.monthcalendar(_year, _month)]:
            _expansion, _is_time_lap = _perioder.__expand__(_year, _month)
            if _is_time_lap:  # perioder is a set of dates
                pass
            else:
                pass
            pass
        pass

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