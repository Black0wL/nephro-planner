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
        self.individual_counters = None
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

    def counters(self, _reset=False):  # basically inverse the day profile, eluding time slots on the run
        if _reset:
            self.individual_counters = None
        if not self.individual_counters:
            # TODO: call Nephrologist.team() instead of Database.team()
            self.individual_counters = dict([(nep.id, nep.counters()) for nep in Database.team()])  # creating a new counters profile for each nephrologist
            for (nep_id, act_type) in [(self.profile[tim][act].id, act) for tim in self.profile for act in self.profile[tim] if self.profile[tim][act] is not None]:
                self.individual_counters[nep_id][act_type] += 1
        return self.individual_counters

    def currentlyAllocatedNephrologists(self, current_timeslot):
        return [self.profile[current_timeslot][act].id for act in self.profile[current_timeslot] if self.profile[current_timeslot][act] is not None]

    def isCurrentlyAllocatedActivity(self, current_timeslot, current_activity):
        return self.profile[current_timeslot][current_activity] is not None

    def restrictedToClearanceTeam(self, current_team, current_activity):
        return [x for x in current_team if current_activity in x.activities]

    def isVolunteerNephrologist(self, current_team, current_nephrologist, current_activity):
        return current_nephrologist.counters()[current_activity] == min([x.counters()[current_activity] for x in self.restrictedToClearanceTeam(current_team, current_activity)])

    def __allocate_friday__(self, current_timeslot, current_activity, current_nephrologist):
        if len(list(set([current_activity]) & set([x for x in self.profile[current_timeslot]]))) == 1 and self.profile[current_timeslot][current_activity] is None:
                self.__slot__(current_timeslot, current_activity, current_nephrologist)

    def __allocate__(self, constraint_level, yesterday_profile, today_date, current_timeslot, holidays):
        current_team = [x for x in Database.team() if x.id not in holidays and today_date.day not in holidays[x.id] and current_timeslot not in holidays[x.id][today_date.day] or x.id not in self.currentlyAllocatedNephrologists(current_timeslot)]
        current_activities = [x for x in self.profile[current_timeslot] if self.profile[current_timeslot][x] is None]

        # print(len(current_activities) > 0 and len(current_team) > 0)
        # print(str(len(current_activities)) + "/" + str(len(current_team)))
        # print(constraint_level)
        if ConstraintStrategy.contains(ConstraintStrategy.ALLOCATE_MORNING_DIALYSIS.value, constraint_level):
            if current_timeslot == TimeSlot.FIRST_SHIFT and yesterday_profile is not None and TimeSlot.THIRD_SHIFT in yesterday_profile:
                obligation_activities = [Activity.OBLIGATION, Activity.OBLIGATION_WEEKEND, Activity.OBLIGATION_HOLIDAY]
                yesterday_obligations = list(set(obligation_activities) & set([x for x in yesterday_profile[TimeSlot.THIRD_SHIFT]]))
                if len(yesterday_obligations) == 1 and yesterday_profile[TimeSlot.THIRD_SHIFT][yesterday_obligations[0]] is not None:
                    today_activities = list(set([Activity.DIALYSIS] + obligation_activities) & set([x for x in self.profile[current_timeslot]]))
                    if len(today_activities) == 1:
                        self.__slot__(current_timeslot, today_activities[0], yesterday_profile[TimeSlot.THIRD_SHIFT][yesterday_obligations[0]])
                    # problem.addConstraint(lambda nep, act: act in [Activity.DIALYSIS] + obligation_activities and nep.id == yesterday_profile[TimeSlot.THIRD_SHIFT][yesterday_obligations[0]].id, (self.nephrologist_key, self.activity_key))
        elif len(current_activities) > 0 and len(current_team) > 0:
            if ConstraintStrategy.contains(ConstraintStrategy.ALLOCATE_WEEKEND_DAYS.value, constraint_level):
                '''
                    N does OTHERS on FIRST_SHIFT (or OBLIGATION_HOLIDAY if DAY is holiday)
                    N does DIALYSIS on SECOND_SHIFT (or OBLIGATION_HOLIDAY if DAY is holiday)
                    N does OBLIGATION on THIRD_SHIFT (or OBLIGATION_HOLIDAY if DAY is holiday)
                    N does OBLIGATION_WEEKEND on all SHIFTS, DAY+1
                    N does OBLIGATION_WEEKEND on all SHIFTS, DAY+2

                    Where:
                    - N: the chosen nephrologist
                    - DAY: Friday
                '''
                if today_date.weekday() == 4:
                    today_nephrologists = list(set(self.restrictedToClearanceTeam(current_team, Activity.OTHERS)) & set([x for x in self.restrictedToClearanceTeam(current_team, Activity.OBLIGATION) if self.isVolunteerNephrologist(current_team, x, Activity.OBLIGATION)]))
                    if len(today_nephrologists) > 0:
                        current_nephrologist = today_nephrologists[0]
                        # TODO: pick nephrologist if already set!
                        if current_timeslot == TimeSlot.FIRST_SHIFT:
                            self.__allocate_friday__(current_timeslot, Activity.OTHERS, current_nephrologist)
                        elif current_timeslot == TimeSlot.SECOND_SHIFT:
                            self.__allocate_friday__(current_timeslot, Activity.DIALYSIS, current_nephrologist)
                        elif current_timeslot == TimeSlot.THIRD_SHIFT:
                            self.__allocate_friday__(current_timeslot, Activity.OBLIGATION, current_nephrologist)
                elif today_date.weekday() in [5, 6]:  # friday, saturday, sunday
                    pass
            else:
                # instantiate a new problem
                problem = Problem()

                # add the different activities to allocate
                problem.addVariable(self.activity_key, current_activities)  # the whole nephrologists that can be allocated on this specific day/shift
                problem.addVariable(self.nephrologist_key, current_team)  # the whole nephrologists minus nephrologists in vacation on this specific day/shift

                # constraints declaration
                problem.addConstraint(AllDifferentConstraint())

                problem.addConstraint(lambda nep, act: act in nep.activities, (self.nephrologist_key, self.activity_key))

                if ConstraintStrategy.contains(ConstraintStrategy.FOCUS_ON_PREFERENCES.value, constraint_level):
                    problem.addConstraint(lambda nep, act: nep.score(today_date.weekday(), current_timeslot, act) > 0, (self.nephrologist_key, self.activity_key))
                else:
                    problem.addConstraint(lambda nep, act: nep.score(today_date.weekday(), current_timeslot, act) == 0, (self.nephrologist_key, self.activity_key))

                if not ConstraintStrategy.contains(ConstraintStrategy.DISCARD_COUNTERS.value, constraint_level):
                    problem.addConstraint(lambda nep, act: self.isVolunteerNephrologist(current_team, nep, act), (self.nephrologist_key, self.activity_key))
                    # problem.addConstraint(lambda nep, act: sum([nep.counters()[y] for y in current_activities]) == min([sum([x.counters()[y] for y in current_activities]) for x in [y for y in current_team if act in y.activities and act in current_activities]]), (self.nephrologist_key, self.activity_key))

                solutions = problem.getSolutions()

                # print("LENGTH_SOLUTIONS: " + str(len(solutions)))
                # print("-------------------------------------")
                # print(solutions)
                # print("-------------------------------------")
                # print(current_timeslot)
                for solution in solutions:
                    if solution[self.nephrologist_key].id not in self.currentlyAllocatedNephrologists(current_timeslot):
                        self.__slot__(current_timeslot, solution[self.activity_key], solution[self.nephrologist_key])
        # print(self)
        # print("-------------------------------------")

    def __slot__(self, current_timeslot, current_activity, current_nephrologist):
        if not self.isCurrentlyAllocatedActivity(current_timeslot, current_activity):
            self.profile[current_timeslot][current_activity] = current_nephrologist
            # print(repr(solution[self.nephrologist_key]) + "|" + str(solution[self.activity_key].name) + ": " + str(solution[self.nephrologist_key].counters()[solution[self.activity_key]]))
            current_nephrologist.counters()[current_activity] += 1

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
































