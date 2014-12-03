__author__ = "Christophe"

from Models.monthly_planning import MonthlyPlanning
from Models.daily_planning import DailyPlanning
import calendar
from Utils.database import Database
from datetime import date, datetime, timedelta
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

        _date = sorted(month_planning.daily_plannings.keys())[len(month_planning.daily_plannings)-1]
        _index = _date.weekday()
        if _index > 3:  # if last month's day is friday, saturday of sunday (unusual day)
            for _day in range(1, 6-_index+1):
                _date = (datetime(_date.year, _date.month, _day) + timedelta(days=1)).date()
                month_planning.daily_plannings[_date] = DailyPlanning(_date)

        # print(month_planning)

        holidays = dict()
        for id in Database.team():
        holidays = Database.team()[2].__holidays__(month, year)
        for day in holidays:
            print(str(day) + "|" + str(holidays[day]))

        problem = Problem()
        """
        problem.addVariables(
            [str(x) for x in sorted(month_planning.daily_plannings)],
            [month_planning.daily_plannings[x] for x in sorted(month_planning.daily_plannings)]
        )
        problem.addVariables(
            [x.id for x in Database.team()],
            [x for x in Database.team()]
        )
        """

        from Enums.timeslot import TimeSlot
        """
        for x, y, z in [(dai, tim, act) for dai in [month_planning.daily_plannings[date(year, month, 1)]] for tim in dai.profile for act in dai.profile[tim] if tim == TimeSlot.FIRST_SHIFT]:
            print str(x.date) + "|" + str(y.value) + "|" + str(z.value)
        """

        current_date = date(year, month, 1)
        current_weekday = current_date.weekday()
        current_timeslot = TimeSlot.FIRST_SHIFT
        allocated = []
        test = month_planning.daily_plannings[current_date].profile[current_timeslot]
        test_key = (month_planning.daily_plannings[current_date], current_timeslot)

        def func(act, nep):
            verdict = True
            # nephrologist has clearance for specific activity
            verdict &= act in nep.activities
            # nephrologist has no aversions for specific activity
            if current_weekday in nep.aversions and current_timeslot in nep.aversions[current_weekday]:
                verdict &= act not in nep.aversions[current_weekday][current_timeslot]

            """
            # nephrologist is free
            verdict &= (act, nep) not in [(x[2], x[3]) for x in allocated]
            if verdict:
                allocated.append((current_date, current_timeslot, act, nep))
            """
            return verdict

        problem.addVariable(
            test_key,
            [activity for activity in test]
        )
        problem.addVariable(
            "t",
            [x for x in Database.team()]
        )
        problem.addConstraint(AllDifferentConstraint())
        problem.addConstraint(FunctionConstraint(func), (test_key, "t"))
        """
        for solution in problem.getSolutions():
            print(solution)
        """
    finally:
        pass

if __name__ == '__main__':
    main()