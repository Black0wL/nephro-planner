__author__ = "Christophe"

from Models.monthly_planning import MonthlyPlanning
from Models.daily_planning import DailyPlanning
from Enums.constraint_strategy import ConstraintStrategy
from Enums.timeslot import TimeSlot
from Enums.activity import Activity
import calendar
from Models.nephrologist import Nephrologist
from Utils.database import Database
from datetime import date, datetime, timedelta
from constraint import *


def main():
    try:
        # Database.__create__()
        # Nephrologist.__load__()

        '''
        from Enums.activity import Activity
        print sum([x.counters[y] for x in Database.team() for y in Activity.flags()])
        return
        '''

        year = 2014
        month = 12
        month_planning = MonthlyPlanning(year, month)
        # print(month_planning)
        # for item in month_planning.iterate():
        #     print(item)

        holidays = dict()
        for x in Database.team():
            holidays[x.id] = x.__holidays__(month, year)  # computing holidays for nephrologists
            # print(holidays[x.id])

        '''
        for x in Database.team():
            print(repr(x) + ": " + str(x.activities))
        '''

        for (yesterday, today) in month_planning.iterate():
            if yesterday is not None:
                yesterday_profile = month_planning.daily_plannings[date(yesterday.year, yesterday.month, yesterday.day)].profile
            else:
                yesterday_profile = None

            current_daily_planning = month_planning.daily_plannings[date(today.year, today.month, today.day)]  # the daily planning for the current day

            # if today_date is weekend day or today_date is holiday
            if current_daily_planning.weekday in [4, 5, 6] or not current_daily_planning.is_working_day:
                # allocate all damn day in the same time
                current_daily_planning.__allocate_whole_day__(ConstraintStrategy.ALLOCATE_WEEKEND_DAYS.value, yesterday_profile, holidays)
                current_daily_planning.__allocate_whole_day__(ConstraintStrategy.ALLOCATE_HOLIDAYS.value, yesterday_profile, holidays)

            # allocate all day's timeslots separately
            for current_timeslot in current_daily_planning.profile:
                current_daily_planning.__allocate_timeslot__(ConstraintStrategy.ALLOCATE_MORNING_DIALYSIS.value, yesterday_profile, current_timeslot, holidays)
                current_daily_planning.__allocate_timeslot__(ConstraintStrategy.FOCUS_ON_PREFERENCES.value, yesterday_profile, current_timeslot, holidays)
                current_daily_planning.__allocate_timeslot__(ConstraintStrategy.NONE.value, yesterday_profile, current_timeslot, holidays)
                # current_daily_planning.__allocate_timeslot__(ConstraintStrategy.DISCARD_COUNTERS.value, yesterday_profile, current_timeslot, holidays)  # ultimate padding strategy

            '''
            print("--------------------------------------------------")
            for x in Database.team():
                print(repr(x) + ": " + str(x.counters()))
            '''

            '''
            for y in current_daily_planning.profile:
                print(str(today) + "|" + str(y) + ": " + "-".join([str(x) for x in sorted(current_daily_planning.currentlyAllocatedNephrologists(y))]))
            '''
            # print("-".join([str(x) for x in current_daily_planning.currentlyAllocatedNephrologists(current_timeslot)]))
            # print(" | ".join([str(x) + ": " + str(x.counters()[Activity.OBLIGATION]) for x in Database.team()]))
            # month_planning.counters()  # counters MUST be updated before looping
            # print(Database.team()[0].counters())
        print("------------------------------------------------------------")
        print(month_planning)
    finally:
        pass

if __name__ == '__main__':
    main()