__author__ = "Christophe"

from Utils.parameters import Parameters
from Utils.constants import Constants
from Utils.database import Database
from Enums.activity import Activity
from Enums.timeslot import TimeSlot
from Models.period import Period
from Models.duration import Duration
from datetime import date
from Utils.datetime_extension import datetime
from Utils.timedelta_extension import timedelta
import sqlite3
import calendar


class Nephrologist(object):
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
    def __init__(self, _id, _name, _activities=Activity.flags(), _holidays=None, _preferences=None, _aversions=None):
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
        _dump = dict()  # map { day_number: [off_time_slots]}
        _lowest = datetime(_year, _month, 1)
        _uppest = datetime(_year, _month, calendar.monthrange(_year, _month)[1]) + timedelta(days=1, microseconds=-1)

        for _blob in self.holidays:
            switch = {
                date: lambda: {_blob.day: TimeSlot.flags()}  if _lowest.date() <= _blob <= _uppest.date() else [],
                Period: lambda: _blob.__transform__(_year, _month),
                Duration: lambda: _blob.__transform__(_year, _month)
            }
            _type = type(_blob)
            # TODO: refactor dat shit?!
            if _type in switch:
                _slots = switch[_type]()

                _keyset = set()
                for _day_slot in _slots:
                    _keyset |= _day_slot

                for _day in list(_keyset):
                    _dump[_day] = set()
                    for _slot in [(_slots[x][_day] if _day in _slots[x] else []) for x in _slots]:
                        _dump[_day] |= set(_slot)
                    _dump[_day] = list(_dump[_day])
            else:
                raise UserWarning("days/slots dump contains unmanaged types.")
        return _dump

    def __preferences__(self, _month, _year):
        Nephrologist.__compute_days_slots_activities_map__(_month, _year, self.preferences)

    def __aversions__(self, _month, _year):
        Nephrologist.__compute_days_slots_activities_map__(_month, _year, self.aversions)

    @classmethod
    def __compute_days_slots_activities_map__(cls, _month, _year, _research_dump):
        _dump = {}
        # eliminating 0-es provided by calendar.monthcalendar...
        for _day in [y for x in calendar.monthcalendar(_year, _month) for y in x if y != 0]:
            _date = date(_year, _month, _day)
            _index = _date.weekday()
            if _index in _research_dump:
                _dump[_day] = _research_dump[_index]
        return _dump

    def __str__(self):
        return self.name[0]

    # TODO: load activities, holidays, preferences from DB
    @classmethod
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