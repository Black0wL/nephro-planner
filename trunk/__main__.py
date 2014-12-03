__author__ = "Christophe"

from Models.monthly_planning import MonthlyPlanning
from Models.daily_planning import DailyPlanning
import calendar
from Utils.database import Database
from datetime import date
from constraint import *


def main():
    try:
        # from Models.nephrologist import Nephrologist
        # Database.__create__()
        # Nephrologist.__load__()
        '''
        from Models.monthly_planning import MonthlyPlanning
        MonthlyPlanning(1, 2014, 11)
        '''

        year = 2014
        month = 12
        month_planning = MonthlyPlanning(year, month)
        for _date in [date(year, month, day) for day in range(1, calendar.monthrange(year, month)[1]+1)]:
            month_planning.daily_plannings[_date] = DailyPlanning(_date)

        print(month_planning)

        problem = Problem()
        problem.addVariable("mp", [month_planning.daily_plannings[x] for x in sorted(month_planning.daily_plannings)])
        problem.addVariable("n", Database.__team__())

        problem.addConstraint(AllDifferentConstraint())
        print(problem.getSolutions())
    finally:
        pass

if __name__ == '__main__':
    main()