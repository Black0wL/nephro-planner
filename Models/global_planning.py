__author__ = "Christophe"

import sqlite3
from Utils.parameters import Parameters
from Utils.constants import Constants
from Utils.database import Database
from datetime import datetime, date
from monthly_planning import MonthlyPlanning
from collections import Counter
from daily_planning import DailyPlanning
from Enums.timeslot import TimeSlot
import calendar


def singleton(cls):
    instances = dict()
    def __new__():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return __new__


@singleton
class GlobalPlanning():
    def __init__(self, _year, _month):
        self.year = _year
        self.month = _month

        with Parameters() as params, sqlite3.connect(params.data[Constants.DATABASE_FILENAME_KEY]) as connection:
            cursor = connection.cursor()

            data_set = cursor.execute('''
                SELECT
                    MIN(date_pk)
                FROM {}
                WHERE
                    date_pk <= '{}'
                GROUP BY
                    date_pk
            '''.format(
                Database.DATABASE_TABLE_MONTHLY_PLANNINGS,
                date(_year, _month, 1).isoformat()  # first date of current year/month's tuple
            ))

        self.monthly_plannings = dict({_year: dict()})  # adding current year as a key
        if data_set.rowcount > 0:
            _min_date = datetime.strptime(data_set.fetchone()[0], "%Y-%m-%d").date()
            for (_m, _y) in [(x, y) for x in range(_min_date.year, _year+1) for y in range(1, 13) if 12*x+y >= 12*_min_date.year+_min_date.month]:  # TODO: might be refactored with an enumeration()
                if _y not in self.monthly_plannings:
                    self.monthly_plannings[_y] = dict()
                self.monthly_plannings[_y][_m] = MonthlyPlanning(_y, _m)

    # TODO: allocate nephrologists to activities & update counters
    def __complete__(self):
        if self.year not in self.monthly_plannings:
            self.monthly_plannings[self.year] = dict()
        if self.month not in self.monthly_plannings[self.year]:  # loading current month and potentially preexisting subjacent DailyPlannings instances...
            self.monthly_plannings[self.year][self.month] = MonthlyPlanning(self.year, self.month)

        existing_monthly_planning = self.monthly_plannings[self.year][self.month]

        for _week in calendar.monthcalendar(self.year, self.month):  # eliminating 0-es provided by monthcalendar...
            for _day in [x for x in _week if x != 0]:
                _date = date(self.year, self.month, _day)

                if _date in existing_monthly_planning:
                    _daily_planning = existing_monthly_planning[_date]
                else:
                    _daily_planning = DailyPlanning(_date)
                    self.monthly_plannings[self.year][self.month] = _daily_planning

                if _date not in existing_monthly_planning.daily_plannings:  # should we really eliminate these?
                    options = {
                        0: lambda y: usual_day(_daily_planning),  # taking care of 1st day (monday)
                        1: lambda y: usual_day(_daily_planning),  # taking care of 2nd day (tuesday)
                        2: lambda y: usual_day(_daily_planning),  # taking care of 3rd day (wednesday)
                        3: lambda y: usual_day(_daily_planning),  # taking care of 4th day (thursday)
                        4: lambda y: uncanny_day(_daily_planning)  # taking care of 5th day, 6th day, 7th day, and 8th day morning (friday, saturday, sunday, and next monday.FIRST_SHIFT)
                    }
                    index = _week.index(_day)
                    if index in options:
                        options[index]()

        from operator import itemgetter

        # TODO: tip! a nephrologist has only a one activity per timeslot unit throughput, dude...
        # TODO: decide... I'm not sure about the _allowed_time_slots thing.
        def usual_day(__daily_planning, _allowed_time_slots=TimeSlot.highest()):
            for (_time_slot, _activity) in [(x, y) for x in __daily_planning if TimeSlot.contains(x, _allowed_time_slots) for y in __daily_planning[x] if not __daily_planning[x][y]]:
                _id_nephrologist, counter = max([(x, self.counters()[x]) for x in self.counters()], key=itemgetter(1))  # have to find the max of self.counters()[x]
                if _id_nephrologist:  # can it ever happen?
                    __daily_planning.__allocate__(_time_slot, _activity, _id_nephrologist)
                    if not counter:  # can it ever happen?
                        counter = Counter()
                        self.counters()[_id_nephrologist] = counter
                    counter[_activity] += 1

        def uncanny_day(__daily_planning):
            # TODO: implement!
            pass

        return self

    @property
    def counters(self, _reset=False):
        if _reset:
            self._counters = None
        if not self._counters:
            for (_id_nephrologist, _monthly_planning_counters) in [(y, self.monthly_plannings[x].counters()) for x in self.monthly_plannings for y in self.monthly_plannings[x].counters()]:
                if _id_nephrologist not in self._counters:
                    self._counters[_id_nephrologist] = Counter()
                self._counters[_id_nephrologist] += _monthly_planning_counters[_id_nephrologist]
        return self._counters

'''
s1=GlobalPlanning()
print(id(s1))
s2=GlobalPlanning()
print(id(s2))
if(id(s1)==id(s2)):
    print "Same"
else:
    print "Different"
'''