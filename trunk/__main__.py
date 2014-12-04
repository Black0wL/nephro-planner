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
        for x in Database.team():
            holidays[x.id] = x.__holidays__(month, year)

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
        current_timeslot = TimeSlot.FIRST_SHIFT

        activity_key = "a"
        nephrologist_key = "n"

        problem = Problem()
        current_weekday = current_date.weekday()
        current_preferences = dict([(x.id, x.preferences[current_weekday][current_timeslot]) for x in Database.team() if current_weekday in x.preferences and current_timeslot in x.preferences[current_weekday]])
        current_allocated = []
        current_daily_planning = month_planning.daily_plannings[current_date]
        current_activities = current_daily_planning.profile[current_timeslot]

        def func(act, nep):
            verdict = True
            # activity or nephrologist are already allocated
            if act in [x[0] for x in current_allocated if x[1] != nep] or nep in [x[1] for x in current_allocated if x[0] != act]:
                return False
            # nephrologist has clearance for specific activity
            verdict &= act in nep.activities
            # nephrologist is not in holiday
            if nep.id in holidays and current_date.day in holidays[nep.id] and current_timeslot in holidays[nep.id][current_date.day]:
                return False
            # nephrologist has a preference for the specific activity: shortcuts further checks
            if not (verdict and nep.id in current_preferences and current_timeslot in current_preferences[nep.id] and act in current_preferences[nep.id][current_timeslot]):
                # nephrologist has no aversions for specific activity
                if current_weekday in nep.aversions and current_timeslot in nep.aversions[current_weekday]:
                    verdict &= act not in nep.aversions[current_weekday][current_timeslot]
                # nephrologist has minimum counter for the specific activity
                if act in nep.counters:
                    verdict &= nep.counters[act] == min([x.counters[act] for x in Database.team() if act in x.counters])
            # conclude
            if verdict:
                current_allocated.append((act, nep))
            return verdict

        problem.addVariable(
            activity_key,
            [x for x in current_activities]
        )
        problem.addVariable(
            nephrologist_key,
            [x for x in Database.team()]
        )
        problem.addConstraint(FunctionConstraint(func), ("a", nephrologist_key))

        solutions = problem.getSolutions()
        if len(solutions) == 0:
            print("[WARNING] allocation failed to allocate any slots.")
        elif len(solutions) < len(current_activities):
            print("[WARNING] allocation failed to allocate all slots.")
        elif len(solutions) > len(current_activities):
            print("[WARNING] allocation allocated too many slots.")
        else:
            for solution in solutions:
                print(solution[nephrologist_key])
                current_daily_planning.profile[current_timeslot][solution[activity_key]] = solution[nephrologist_key]
            print(current_daily_planning)
    finally:
        pass

if __name__ == '__main__':
    main()





















