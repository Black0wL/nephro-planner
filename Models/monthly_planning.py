__author__ = "Christophe"

from Enums.timeslot import TimeSlot
from Models.timespan import TimeSpan
from Models.daily_planning import DailyPlanning
import sqlite3
from Utils.parameters import Parameters
from Utils.constants import Constants
from Utils.database import Database
from datetime import timedelta, date, datetime
from collections import Counter
import calendar


def singleton(cls):
    instances = dict()

    def __new__(_year, _month):
        if _year not in instances:
            instances[_year] = dict()
        if _month not in instances[_year]:
            instances[_year][_month] = cls(_year, _month)
        return instances[_year][_month]
    return __new__


@singleton
class MonthlyPlanning():
    def __init__(self, _year, _month):
        self.year = _year
        self.month = _month

        with Parameters() as params, sqlite3.connect(params.data[Constants.DATABASE_FILENAME_KEY]) as connection:
            cursor = connection.cursor()

            data_set = cursor.execute('''
                SELECT
                    date_pk,
                    time_slot_type_pk,
                    activity_type,
                    id_nephrologist_fk
                FROM {}
                WHERE
                    date_pk >= '{}'
                    AND date_pk <= '{}'
            '''.format(
                Database.DATABASE_TABLE_MONTHLY_PLANNINGS,
                date(_year, _month, 1).isoformat(),  # first month's day
                date(_year, _month, calendar.monthrange(_year, _month)[1]).isoformat()  # last month's day
            ))

        self.daily_plannings = dict()
        if data_set.rowcount > 0:  # load an resource-allocated image of the specific days
            for row in data_set.fetchmany():
                _date = datetime.strptime(row[0], "%Y-%m-%d").date()
                self.daily_plannings[_date] = DailyPlanning(_date).__allocate__(
                    row[1],
                    row[2],
                    row[3]
                )

    @property
    def counters(self, _reset=False):
        if _reset:
            self._counters = None
        if not self._counters:
            for (_id_nephrologist, _daily_planning_counters) in [(y, self.daily_plannings[x].counters()) for x in self.daily_plannings for y in self.daily_plannings[x].counters()]:
                if _id_nephrologist not in self._counters:
                    self._counters[_id_nephrologist] = Counter()
                self._counters[_id_nephrologist] += _daily_planning_counters[_id_nephrologist]
        return self._counters

    # TODO: implement proper rendering into excel spreadsheet
    def output(self, filename, sheet_name, list1, list2, x, y, z):
        import xlwt
        book = xlwt.Workbook()
        sh = book.add_sheet(sheet_name)

        variables = [x, y, z]
        x_desc = 'Display'
        y_desc = 'Dominance'
        z_desc = 'Test'
        desc = [x_desc, y_desc, z_desc]

        col1_name = 'Stimulus Time'
        col2_name = 'Reaction Time'

        #You may need to group the variables together
        #for n, (v_desc, v) in enumerate(zip(desc, variables)):
        for n, v_desc, v in enumerate(zip(desc, variables)):
            sh.write(n, 0, v_desc)
            sh.write(n, 1, v)

        n+=1

        sh.write(n, 0, col1_name)
        sh.write(n, 1, col2_name)

        for m, e1 in enumerate(list1, n+1):
            sh.write(m, 0, e1)

        for m, e2 in enumerate(list2, n+1):
            sh.write(m, 1, e2)

        book.save(filename)














































