__author__ = "Christophe"

import sqlite3
from Utils.parameters import Parameters
from Utils.constants import Constants
from Utils.database import Database
from datetime import datetime, date
from monthly_planning import MonthlyPlanning


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

        self.monthly_plannings = dict({_year: dict()})  # adding current year as a key, because
        if data_set.rowcount > 0:
            _min_date = datetime.strptime(data_set.fetchone()[0], "%Y-%m-%d").date()
            for (_m, _y) in [(x, y) for x in range(_min_date.year, _year+1) for y in range(1, 13)
                             if 12*x+y >= 12*_min_date.year+_min_date.month]:
                if _y not in self.monthly_plannings:
                    self.monthly_plannings[_y] = {}
                self.monthly_plannings[_y][_m] = MonthlyPlanning(_y, _m)

        if _month not in self.monthly_plannings[_year]:  # because even if previous months have already been set, current month might not exist
            self.monthly_plannings[_month] = MonthlyPlanning(_year, _month)

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