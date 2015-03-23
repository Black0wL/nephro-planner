__author__ = "Christophe"

from Models.monthly_planning import MonthlyPlanning
from Models.daily_planning import DailyPlanning
from Enums.constraint_strategy import ConstraintStrategy
from Enums.timeslot import TimeSlot
import calendar
from Models.nephrologist import Nephrologist
from Utils.database import Database
from datetime import date, datetime, timedelta
from constraint import *


def main():
    try:
        # Database.__create__()
        # Nephrologist.__load__()

        year = 2014
        month = 12
        month_planning = MonthlyPlanning(year, month)
        # print(month_planning)
        # for item in month_planning.iterate():
        #     print(item)

        holidays = dict()
        for x in Database.team():
            holidays[x.id] = x.__holidays__(month, year)  # computing holidays for nephrologists

        for (yesterday, today) in month_planning.iterate():
            yesterday_date = date(yesterday.year, yesterday.month, yesterday.day)
            today_date = date(today.year, today.month, today.day)  # first day for constraint solving (it's a monday!)
            current_daily_planning = month_planning.daily_plannings[today_date]  # the daily planning for the current day
            for current_timeslot in current_daily_planning.profile:
                current_daily_planning.__allocate__(ConstraintStrategy.FOCUS_ON_PREFERENCES.value, month_planning.daily_plannings[yesterday_date], today_date, current_timeslot, holidays)
                current_daily_planning.__allocate__(ConstraintStrategy.DISCARD_COUNTERS.value, month_planning.daily_plannings[yesterday_date], today_date, current_timeslot, holidays)
            # counters MUST be updated before looping

        print(month_planning)
    finally:
        pass

if __name__ == '__main__':
    main()