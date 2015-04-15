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

        year = 2015
        month = 5
        month_planning = MonthlyPlanning(year, month)
        month_planning.__compute__()

        '''
        print("--------------------------------------------------")
        for x in Database.team():
            print(repr(x) + ": " + str(x.counters()))
        '''

        '''
        for y in current_daily_planning.profile:
            print(str(today) + "|" + str(y) + ": " + "-".join([str(x) for x in sorted(current_daily_planning.currentlyAllocatedNephrologists(y))]))
        '''

        '''
        for x in Database.team():
            print(repr(x) + ": ")
            for holiday in sorted(month_planning.holidays[x.id]):
                print("\t" + str(holiday) + ": " + "|".join([y.name[0] for y in month_planning.holidays[x.id][holiday]]))

        print("------------------------------------------------------------")
        '''

        print(month_planning)

        month_planning.output()
    finally:
        pass

if __name__ == '__main__':
    main()