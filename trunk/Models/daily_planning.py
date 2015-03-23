__author__ = "Christophe"

from week import Week
from workalendar.europe import France
from Enums.activity import Activity
from Enums.constraint_strategy import ConstraintStrategy
from Enums.timeslot import TimeSlot
from Models.nephrologist import Nephrologist
from Utils.database import Database
from collections import Counter
import copy
from constraint import *


def singleton(cls):
    instances = dict()

    def __new__(_date):
        if _date not in instances:
            instances[_date] = cls(_date)
        return instances[_date]
    return __new__


@singleton
class DailyPlanning():
    activity_key = "a"
    nephrologist_key = "n"

    def __init__(self, _date):
        self.date = _date

        # if required, _calendar.is_working_day can deal with extra working days/holidays
        _is_working_day = France().is_working_day(_date)
        _index = _date.weekday()
        # normal working day if no holiday or if weekend day
        # tip: holiday during weekend are considered as normal weekend working day
        if _is_working_day or _index in [5, 6]:
            self.profile = copy.deepcopy(Week.SLOTS[_index])
        # unusual working day if holiday
        else:
            self.profile = copy.deepcopy(Week.SLOTS[Week.KEY_SPECIAL_HOLIDAY])

        if not self.profile:
            raise UserWarning("daily planning's profile has not been successfully resolved.")

    '''
    def __allocate__(self, _time_slot_type, _activity_type, _id_nephrologist):
        if type(_time_slot_type) is not TimeSlot:
            raise UserWarning("{} parameter must be of type {}.".format(
                DailyPlanning.__allocate__.func_code.co_varnames[1],
                TimeSlot
            ))
        elif type(_time_slot_type) is not Activity:
            raise UserWarning("{} parameter must be of type {}.".format(
                DailyPlanning.__allocate__.func_code.co_varnames[2],
                Activity
            ))
        elif type(_id_nephrologist) is not int:
            raise UserWarning("{} parameter must be of type {}.".format(
                DailyPlanning.__allocate__.func_code.co_varnames[3],
                int
            ))
        elif not self.profile:
            raise UserWarning("daily planning's profile is None.")
        else:
            if _time_slot_type.name not in self.profile:
                raise UserWarning("daily planning's profile does not contain time slot {}.".format(
                    _time_slot_type
                ))
            elif _activity_type.name not in self.profile[_time_slot_type.name]:
                raise UserWarning("daily planning's profile does not contain activity type {} for time slot {}.".format(
                    _activity_type,
                    _time_slot_type
                ))
            else:
                # TODO: detect whether time slot for activity is already allocated!
                self.profile[_time_slot_type.name][_activity_type.name] = _id_nephrologist
        return self
    '''

    def __str__(self):
        import re

        def render_enum(flag, nephrologist):
            m = re.search('(?<=_)\w+', flag.name)
            r = flag.name[0]
            return (r + flag.name[1:3].lower() if not m else m.group(0)[0]) + ("({})".format(nephrologist if nephrologist else "-"))

        render = str(self.date) + ": "
        for timeslot in self.profile:
            render += timeslot.name[0] + ":"
            render += "|".join([render_enum(activity, self.profile[timeslot][activity]) for activity in self.profile[timeslot]])
            render += " "
        return render

    @property
    def counters(self, _reset=False):  # basically inverse the day profile, eluding time slots on the run
        if _reset:
            self._counters = None
        if not self._counters:
            # TODO: call Nephrologist.team() instead of Database.team()
            self._counters = dict([(x, Counter()) for x in Database.team()])  # creating a new counters profile for each nephrologist
            for (_id_nephrologist, _activity_type) in [(z, y) for x in self.profile for y in self.profile[x] for z in self.profile[x][y]]:
                self._counters[_id_nephrologist][_activity_type] += 1
        return self._counters

    def currentlyAllocatedNephrologists(self, current_timeslot):
        return [self.profile[current_timeslot][act].id for act in self.profile[current_timeslot] if self.profile[current_timeslot][act] is not None]

    # TODO: implement rule for DIALYSIS/FIRST_SHIFT
    def __allocate__(self, constraint_level, yesterday_profile, today_date, current_timeslot, holidays):
        current_team = [x for x in Database.team() if x.id not in holidays and today_date.day not in holidays[x.id] and current_timeslot not in holidays[x.id][today_date.day] or x.id not in self.currentlyAllocatedNephrologists(current_timeslot)]
        current_activities = [x for x in self.profile[current_timeslot] if self.profile[current_timeslot][x] is None]

        # instantiate a new problem
        problem = Problem()

        # add the different activities to allocate
        problem.addVariable(self.activity_key, current_activities)  # the whole nephrologists that can be allocated on this specific day/shift
        problem.addVariable(self.nephrologist_key, current_team)  # the whole nephrologists minus nephrologists in vacation on this specific day/shift

        # constraints declaration
        problem.addConstraint(AllDifferentConstraint())
        if yesterday_profile is not None and current_timeslot in yesterday_profile and current_timeslot == TimeSlot.FIRST_SHIFT:
            # print("YESTERDAY_PROFILE: " + str(yesterday_profile[current_timeslot][act]))
            problem.addConstraint(lambda nep, act: act == Activity.DIALYSIS and act in yesterday_profile[current_timeslot] and yesterday_profile[current_timeslot][act] is not None and nep.id == yesterday_profile[current_timeslot][act].id, (self.nephrologist_key, self.activity_key))
            # print("YESTERDAY_PROFILE: " + str(act))
        else:
            if ConstraintStrategy.contains(ConstraintStrategy.FOCUS_ON_PREFERENCES.value, constraint_level):
                problem.addConstraint(lambda nep, act: nep.score(today_date.weekday(), current_timeslot, act) > 0, (self.nephrologist_key, self.activity_key))
            else:
                problem.addConstraint(lambda nep, act: nep.score(today_date.weekday(), current_timeslot, act) == 0, (self.nephrologist_key, self.activity_key))

            problem.addConstraint(lambda nep, act: act in nep.activities, (self.nephrologist_key, self.activity_key))

            if not ConstraintStrategy.contains(ConstraintStrategy.DISCARD_COUNTERS.value, constraint_level):
                problem.addConstraint(lambda nep, act: nep.counters[act] == min([x.counters[act] for x in current_team]), (self.nephrologist_key, self.activity_key))

        solutions = problem.getSolutions()

        # print("LENGTH_SOLUTIONS: " + str(len(solutions)))
        # print("-------------------------------------")
        # print(solutions)
        # print("-------------------------------------")
        for solution in solutions:
            if solution[self.nephrologist_key].id not in self.currentlyAllocatedNephrologists(current_timeslot):
                self.profile[current_timeslot][solution[self.activity_key]] = solution[self.nephrologist_key]
        # print(self)
        # print("-------------------------------------")

'''
_date = date(2014, 2, 5)
s1=DailyPlanning(_date)
print(id(s1))
s2=DailyPlanning(_date)
print(id(s2))
if(id(s1)==id(s2)):
    print "Same"
else:
    print "Different"
'''
































