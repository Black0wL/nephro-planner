__author__ = "Christophe"

from Enums.timeslot import TimeSlot
from Models.timespan import TimeSpan
from datetime import timedelta


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
        ),
        TimeSlot.ALL_DAY.name: TimeSpan(
            _initial=timedelta(),
            _frequency=timedelta(days=1),
            _final=timedelta(days=1, microseconds=-1)
        ),
        TimeSlot.ALL_WEEKEND.name: TimeSpan(
            _initial=timedelta(days=5),
            _frequency=timedelta(weeks=1),
            _final=timedelta(days=7, microseconds=-1)
        )
    }

    def __init__(self, _version, _year, _month):
        import calendar
        for week in calendar.monthcalendar(_year, _month):
            print(week)