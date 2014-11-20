__author__ = "Christophe"

from Enums.timeslot import TimeSlot
from Models.timespan import TimeSpan
from Models.daily_planning import DailyPlanning
import sqlite3
from Utils.parameters import Parameters
from Utils.constants import Constants
from Utils.database import Database
from datetime import timedelta, date, datetime
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
    time_slots_to_time_spans = {
        TimeSlot.FIRST_SHIFT.name: TimeSpan(
            _initial=timedelta(hours=5),
            _frequency=timedelta(days=1),
            _final=timedelta(hours=13, microseconds=-1)
        ),
        TimeSlot.SECOND_SHIFT.name: TimeSpan(
            _initial=timedelta(hours=13),
            _frequency=timedelta(days=1),
            _final=timedelta(hours=21, microseconds=-1)
        ),
        TimeSlot.THIRD_SHIFT.name: TimeSpan(
            _initial=timedelta(hours=21),
            _frequency=timedelta(days=1),
            _final=timedelta(days=1, hours=5, microseconds=-1)
        )
    }

    def __init__(self, _year, _month):
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

        self.daily_plannings = {}
        if data_set.rowcount > 0:
            for row in data_set.fetchmany():
                _date = datetime.strptime(row[0], "%Y-%m-%d").date()
                self.daily_plannings[_date] = DailyPlanning(_date).__allocate__(
                    row[1],
                    row[2],
                    row[3]
                )

        # TODO: if ~toutes les dates~ not in self.daily_plannings:
        for _day in [x for _week in calendar.monthcalendar(_year, _month) for x in _week if x != 0]:
            _date = date(_year, _month, _day)
            self.daily_plannings[_date] = DailyPlanning(_date)
            # TODO: allocate nephrologists to activities & update counters














































