__author__ = "Christophe"

from datetime import datetime, date
from Models.nephrologist import Nephrologist
from monthly_planning import MonthlyPlanning
from daily_planning import DailyPlanning
from Enums.timeslot import TimeSlot
from Enums.activity import Activity
from collections import Counter


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
        if not _year:
            raise UserWarning("year can not be None.")
        elif not isinstance(_year, int):
            raise UserWarning("year must be of type {}".format(int))
        self.year = _year

        if not _month:
            raise UserWarning("month can not be None.")
        elif not isinstance(_month, int):
            raise UserWarning("month must be of type {}".format(int))
        self.month = _month

        import sqlite3
        from Utils.parameters import Parameters
        from Utils.constants import Constants
        from Utils.database import Database
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
            # find first ever monthly planning date
            _min_date = datetime.strptime(data_set.fetchone()[0], "%Y-%m-%d").date()
            # load all existing monthly plannings
            # TODO: might be refactored with an enumeration()
            for (_m, _y) in [(x, y) for x in range(_min_date.year, _year+1) for y in range(1, 13) if 12*x+y >= 12*_min_date.year+_min_date.month]:
                if _y not in self.monthly_plannings:
                    self.monthly_plannings[_y] = dict()
                self.monthly_plannings[_y][_m] = MonthlyPlanning(_y, _m)

    # allocate nephrologists to activities & update counters
    def __allocate__(self):
        pass

    @property
    def counters(self, _reset=False):
        if _reset:
            self._counters = None
        if not self._counters:
            for (_id_nephrologist, _monthly_planning_counters) in [
                (y, self.monthly_plannings[x].counters())
                for x in self.monthly_plannings
                for y in self.monthly_plannings[x].counters()]:
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