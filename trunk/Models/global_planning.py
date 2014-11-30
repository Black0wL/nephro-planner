__author__ = "Christophe"

from datetime import datetime, date
from Models.nephrologist import Nephrologist
from monthly_planning import MonthlyPlanning
from daily_planning import DailyPlanning
from Enums.timeslot import TimeSlot
from Enums.activity import Activity
from collections import Counter


def singleton(cls):
    instances = dict()
    def __new__():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return __new__


@singleton
class GlobalPlanning():
    def __init__(self, _year, _month):
        if not _year:
            raise UserWarning("year can not be None.")
        elif not isinstance(_year, int):
            raise UserWarning("year must be of type {}".format(int))
        self.year = _year

        if not _month:
            raise UserWarning("month can not be None.")
        elif not isinstance(_month, int):
            raise UserWarning("month must be of type {}".format(int))
        self.month = _month

        import sqlite3
        from Utils.parameters import Parameters
        from Utils.constants import Constants
        from Utils.database import Database
        with Parameters() as params, sqlite3.connect(params.data[Constants.DATABASE_FILENAME_KEY]) as connection:
            cursor = connection.cursor()

            data_set = cursor.execute('''
                SELECT
                    MIN(date_pk)
                FROM {}
                WHERE
                    date_pk <= '{}'
                GROUP BY
                    date_pk
            '''.format(
                Database.DATABASE_TABLE_MONTHLY_PLANNINGS,
                date(_year, _month, 1).isoformat()  # first date of current year/month's tuple
            ))

        self.monthly_plannings = dict({_year: dict()})  # adding current year as a key
        if data_set.rowcount > 0:
            # find first ever monthly planning date
            _min_date = datetime.strptime(data_set.fetchone()[0], "%Y-%m-%d").date()
            # load all existing monthly plannings
            # TODO: might be refactored with an enumeration()
            for (_m, _y) in [(x, y) for x in range(_min_date.year, _year+1) for y in range(1, 13) if 12*x+y >= 12*_min_date.year+_min_date.month]:
                if _y not in self.monthly_plannings:
                    self.monthly_plannings[_y] = dict()
                self.monthly_plannings[_y][_m] = MonthlyPlanning(_y, _m)

    # allocate nephrologists to activities & update counters
    def __allocate__(self):
        if self.year not in self.monthly_plannings:
            self.monthly_plannings[self.year] = dict()
        # loading current month and potentially preexisting subjacent DailyPlannings instances...
        if self.month not in self.monthly_plannings[self.year]:
            self.monthly_plannings[self.year][self.month] = MonthlyPlanning(self.year, self.month)

        _monthly_planning = self.monthly_plannings[self.year][self.month]

        _holidays = dict([(x, Nephrologist.team()[x].__holidays__(self.month, self.year)) for x in Nephrologist.team()])
        _preferences = dict([(x, Nephrologist.team()[x].__preferences__(self.month, self.year)) for x in Nephrologist.team()])
        _aversions = dict([(x, Nephrologist.team()[x].__aversions__(self.month, self.year)) for x in Nephrologist.team()])

        import calendar
        for _week in calendar.monthcalendar(self.year, self.month):
            # eliminating 0-es provided by calendar.monthcalendar...
            for _day in [x for x in _week if x != 0]:
                _date = date(self.year, self.month, _day)

                if _date in _monthly_planning:
                    _daily_planning = _monthly_planning[_date]
                else:
                    _daily_planning = DailyPlanning(_date)
                    self.monthly_plannings[self.year][self.month] = _daily_planning

                if _date not in _monthly_planning.daily_plannings:  # should we really eliminate these?
                    switch = {
                        0: lambda: usual_day(_daily_planning),  # taking care of 1st day (monday)
                        1: lambda: usual_day(_daily_planning),  # taking care of 2nd day (tuesday)
                        2: lambda: usual_day(_daily_planning),  # taking care of 3rd day (wednesday)
                        3: lambda: usual_day(_daily_planning),  # taking care of 4th day (thursday)
                        4: lambda: uncanny_day(_daily_planning)  # taking care of 5th day, 6th day, 7th day, and 8th day morning (friday, saturday, sunday, and next monday.FIRST_SHIFT)
                    }
                    index = _week.index(_day)
                    if index in switch:
                        switch[index]()

        def usual_day(__daily_planning):
            # initializing the "one activity per time slot per nephrologist throughput" watcher
            _already_allocated_id_nephrologists = {[(x, []) for x in __daily_planning]}
            # for each time slot of the daily planning that are authorized to be allocated
            # TODO: examine preferences and aversions before (deal with CONSULTATION first)


            """
                Allocate time slot/activity combos following a very specific order:
                - manage aversions and preferences combo first (if clash on that step, stop: too much subjective constraints)
                - deal with the rest
                That way:
                - Nephrologist will be allocated busy unfrustrated
                - Rule: "CONSULTATION > DIALYSIS" following an OBLIGATION[_HOLIDAY] will be managed seamlessly
            """


            for _time_slot in __daily_planning:
                # for each activity available for the current time slot that is not already allocated
                for _activity in [y for y in __daily_planning[_time_slot] if not __daily_planning[_time_slot][y]]:
                    # nephrologist who does DIALYSIS on SECOND_SHIFT does OBLIGATION on THIRD_SHIFT

                    # allocate current time slot/activity combo
                    _id_nephrologist = __allocate__(__daily_planning, _time_slot, _activity, _already_allocated_id_nephrologists[_time_slot])
                    if _time_slot is TimeSlot.SECOND_SHIFT and _activity is Activity.DIALYSIS:
                        if TimeSlot.THIRD_SHIFT in __daily_planning and Activity.OBLIGATION in __daily_planning[TimeSlot.THIRD_SHIFT]:
                            __allocate__(__daily_planning, TimeSlot.THIRD_SHIFT, Activity.OBLIGATION, _already_allocated_id_nephrologists[TimeSlot.THIRD_SHIFT], _id_nephrologist)

        def __allocate__(__daily_planning, __time_slot, __activity, __busy_id_nephrologists, __id_nephrologist=None):
            # nephrologist has a minimal counter on the specific activity
            # nephrologist is not already allocated on an activity for the current time slot
            # nephrologist has clearance for specific activity
            # nephrologist is not on holiday
            if __id_nephrologist:
                _id_nephrologist = __id_nephrologist
                _counter = self.counters()[__id_nephrologist]
            else:
                """
                    # of course, None nephrologist will have a time slot/activity expected both in preferences and aversions specifications
                    # if nephrologist has specified an aversion for the time slot/activity combo...
                    if __time_slot in _aversions[z] and __activity in _aversions[z][__time_slot]:
                        # ...if another nephrologist has a preference for this combo,
                        for y in [x for x in _preferences if __time_slot in _preferences[x] and __activity in _preferences[x][__time_slot]]:
                            continue
                """

                _possibles = []
                for z in self.counters():
                    if z in __busy_id_nephrologists:
                        continue
                    if not Activity.contains(__activity.value, Nephrologist.team()[z].activities):
                        continue
                    if _holidays[z] and _daily_planning.date.day in _holidays[z] and __time_slot in _holidays[z][_daily_planning.date.day]:
                        continue
                    _possibles.append((z, self.counters()[z]))

                from operator import itemgetter
                _id_nephrologist, _counter = min(_possibles, key=itemgetter(1)[__activity])

            if _id_nephrologist:
                # update allocation map for specific time slot
                __busy_id_nephrologists.append(_id_nephrologist)
                # allocate specific activity for specific time slot to specific nephrologist
                __daily_planning.__allocate__(__time_slot, __activity, _id_nephrologist)
                # update counting map
                if not _counter:
                    _counter = Counter()
                    self.counters()[_id_nephrologist] = _counter
                _counter[__activity] += 1

                return _id_nephrologist
            else:
                raise UserWarning(
                    "activity: {} unallocated (time slot: {}, date: {})".format(
                    __activity,
                    __time_slot,
                    __daily_planning.date
                ))

        def uncanny_day(__daily_planning):
            # TODO: choose nephrologist N that has minimal OBLIGATION_WEEKEND counter
            # TODO: N does OTHERS on FIRST_SHIFT (or OBLIGATION_HOLIDAY if DAY is holiday)
            # TODO: N does DIALYSIS on SECOND_SHIFT (or OBLIGATION_HOLIDAY if DAY is holiday)
            # TODO: N does OBLIGATION on THIRD_SHIFT (or OBLIGATION_HOLIDAY if DAY is holiday)
            # TODO: N does OBLIGATION_WEEKEND on all SHIFTS, DAY+1
            # TODO: N does OBLIGATION_WEEKEND on all SHIFTS, DAY+2
            # TODO: N does DIALYSIS on DAY+3/FIRST_SHIFT (or OBLIGATION_HOLIDAY if DAY+3 is holiday)
            # TODO: N earns +1 OBLIGATION_RECOVERY (to allocate during WEEK+1)
            pass

        return self

    @property
    def counters(self, _reset=False):
        if _reset:
            self._counters = None
        if not self._counters:
            for (_id_nephrologist, _monthly_planning_counters) in [
                (y, self.monthly_plannings[x].counters())
                for x in self.monthly_plannings
                for y in self.monthly_plannings[x].counters()]:
                if _id_nephrologist not in self._counters:
                    self._counters[_id_nephrologist] = Counter()
                self._counters[_id_nephrologist] += _monthly_planning_counters[_id_nephrologist]
        return self._counters

'''
s1=GlobalPlanning()
print(id(s1))
s2=GlobalPlanning()
print(id(s2))
if(id(s1)==id(s2)):
    print "Same"
else:
    print "Different"
'''