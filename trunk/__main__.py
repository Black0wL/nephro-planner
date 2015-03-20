__author__ = "Christophe"

from Models.monthly_planning import MonthlyPlanning
from Models.daily_planning import DailyPlanning
import calendar
from Models.nephrologist import Nephrologist
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
        for x in Database.team():
            holidays[x.id] = x.__holidays__(month, year)  # computing holidays for nephrologists

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

        activity_key = "a"
        nephrologist_key = "n"

        # Missing: for loop to include all in-scope days.
        # Missing: for loop to include all in-scope shifts.
        current_date = date(year, month, 1)  # first day for constraint solving (it's a monday!)
        current_daily_planning = month_planning.daily_plannings[current_date]  # the daily planning for the current day





        current_timeslot = TimeSlot.FIRST_SHIFT  # first shift for constraint solving

        current_team = [nep for nep in Database.team() if nep.id not in holidays or current_date.day not in holidays[nep.id] or current_timeslot not in holidays[nep.id][current_date.day] or nep in current_daily_planning[current_timeslot]]
        current_activities = [act for act in current_daily_planning.profile[current_timeslot] if current_daily_planning.profile[current_timeslot][act] is None]

        # instantiate a new problem
        problem = Problem()

        # add the different activities to allocate
        problem.addVariable(activity_key, current_activities)  # the whole nephrologists that can be allocated on this specific day/shift
        problem.addVariable(nephrologist_key, current_team)  # the whole nephrologists minus nephrologists in vacation on this specific day/shift

        problem.addConstraint(AllDifferentConstraint())
        problem.addConstraint(lambda nep, act: nep.score(current_date.weekday(), current_timeslot, act) > 0, (nephrologist_key, activity_key))
        problem.addConstraint(lambda nep, act: act in nep.activities, (nephrologist_key, activity_key))
        problem.addConstraint(lambda nep, act: nep.counters[act] == min([x.counters[act] for x in current_team]), (nephrologist_key, activity_key))
        # problem.addConstraint(lambda nep, act: , (nephrologist_key, activity_key))
        # problem.addConstraint(lambda nep, act: max([nep.score(current_weekday, current_timeslot, act)]), (nephrologist_key, activity_key))

        solutions = problem.getSolutions()
        print(len(solutions))
        print("-------------------------------------")
        print(solutions)
        print("-------------------------------------")
        for solution in solutions:
            if solution[nephrologist_key] in [current_daily_planning.profile[current_timeslot][act] for act in current_daily_planning.profile[current_timeslot]]:
                current_daily_planning.profile[current_timeslot][solution[activity_key]] = solution[nephrologist_key]
        print(current_daily_planning)
    finally:
        pass

if __name__ == '__main__':
    main()





















