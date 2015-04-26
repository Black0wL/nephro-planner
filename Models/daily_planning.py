__author__ = "Christophe"

from week import Week
from workalendar.europe import France
from Enums.activity import Activity
from Enums.constraint_strategy import ConstraintStrategy
from Enums.timeslot import TimeSlot
from Utils.database import Database
import copy
from constraint import *
from datetime import timedelta
from random import randint, shuffle
from Models.free_slots import FreeSlots


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
    obligation_activities = [Activity.OBLIGATION, Activity.OBLIGATION_WEEKEND, Activity.OBLIGATION_HOLIDAY]

    def __init__(self, _date):
        self.date = _date

        # if required, _calendar.is_working_day can deal with extra working days/holidays
        self.is_working_day = France().is_working_day(_date)
        self.weekday = _date.weekday()
        # normal working day if no holiday or if weekend day
        # tip: holiday during weekend are considered as normal weekend working day
        if self.weekday in [5, 6] or self.is_working_day:
            self.profile = copy.deepcopy(Week.SLOTS[self.weekday])
        # unusual working day if holiday
        else:
            self.profile = copy.deepcopy(Week.SLOTS[Week.KEY_SPECIAL_HOLIDAY])

        if not self.profile:
            raise UserWarning("daily planning's profile has not been successfully resolved.")

    def __str__(self):
        import re
        from colorama import Fore, Back, Style, init
        init(autoreset=True)

        def render_enum(flag, nephrologist):
            m = re.search('(?<=_)\w+', flag.name)
            r = flag.name[0]
            return (r + flag.name[1:3].lower() if not m else m.group(0)[0]) + ("({})".format(str(nephrologist) if nephrologist else Back.RED + "-" + Style.RESET_ALL))

        render = str(self.date) + "[{0}]".format({0: "Mon", 1:"Tue", 2:"Wed", 3:"Thu", 4:"Fri", 5:"Sat", 6:"Sun"}[self.weekday]) + ": "
        for timeslot in self.profile:
            render += timeslot.name[0] + ":"
            render += "|".join([render_enum(activity, self.profile[timeslot][activity]) for activity in self.profile[timeslot]])
            render += " "
        print render
        return ""

    '''
    def counters(self, _reset=False):  # basically inverse the day profile, eluding time slots on the run
        if _reset:
            self.individual_counters = None
        if not self.individual_counters:
            # TODO: call Nephrologist.team() instead of Database.team()
            self.individual_counters = dict([(nep.id, nep.counters()) for nep in Database.team()])  # creating a new counters profile for each nephrologist
            for (nep_id, act_type) in [(self.profile[tim][act].id, act) for tim in self.profile for act in self.profile[tim] if self.profile[tim][act] is not None]:
                self.individual_counters[nep_id][act_type] += 1
        return self.individual_counters
    '''

    def __currently_allocated_nephrologists__(self, current_timeslot):
        return [self.profile[current_timeslot][act].id for act in self.profile[current_timeslot] if self.profile[current_timeslot][act] is not None]

    def __is_currently_allocated_activity__(self, current_timeslot, current_activity):
        return self.profile[current_timeslot][current_activity] is not None

    def __restricted_to_clearance_team__(self, current_team, current_activity):
        return [x for x in current_team if current_activity in x.activities]

    def __is_most_rested_nephrologist__(self, current_team, current_nephrologist, current_activity):
        counters = [x.counters()[current_activity] for x in self.__restricted_to_clearance_team__(current_team, current_activity)]
        return len(counters) > 0 and current_nephrologist.counters()[current_activity] == min(counters)

    def __get_activity__(self, current_timeslot, current_nephrologist):
        activities = [activity for activity in self.profile[current_timeslot] if self.profile[current_timeslot][activity] is not None and self.profile[current_timeslot][activity].id == current_nephrologist.id]
        if len(activities) == 1:
            return activities[0]
        else:
            return None

    def __slot__(self, current_timeslot, current_activity, current_nephrologist):
        if current_nephrologist is not None:
            if not self.__is_currently_allocated_activity__(current_timeslot, current_activity):
                self.profile[current_timeslot][current_activity] = current_nephrologist
                current_nephrologist.counters()[current_activity] += 1
                return True
            else:
                return False
        else:
            return False

    def __is_in_holiday__(self, nephrologist, current_timeslot, holidays, day_offset=0):
        return nephrologist.id in holidays and (self.date + timedelta(days=day_offset)) in holidays[nephrologist.id] and current_timeslot in holidays[nephrologist.id][(self.date + timedelta(days=day_offset))]

    """ constructor of the class

        @param current_timeslot: unique identifier of a nephrologist.
        @type current_timeslot: int
        @param holidays: unique humanized identifier of a nephrologist.
        @type holidays: dict
        @param yesterday_profile: activities a nephrologist can be allocated on.
        @type yesterday_profile: dict
    """
    def __team_problem__(self, current_timeslot, holidays, offset_range=[]):
        current_team = [x for x in Database.team() if x.id not in self.__currently_allocated_nephrologists__(current_timeslot)]

        '''
        if yesterday_profile is not None:
            offset_range = range(1, 4)
            # The eligible nephrologist
            if TimeSlot.THIRD_SHIFT in yesterday_profile:
                yesterday_obligations = list(set(self.obligation_activities) & set([x for x in yesterday_profile[TimeSlot.THIRD_SHIFT]]))
                if len(yesterday_obligations) == 1 and yesterday_profile[TimeSlot.THIRD_SHIFT][yesterday_obligations[0]] is not None:
                    current_team = [x for x in current_team if x.id is not yesterday_profile[TimeSlot.THIRD_SHIFT][yesterday_obligations[0]].id]
        else:
            offset_range = []
        '''

        # check whether nephrologist is scheduled for vacation for current day + days before/after in the offset range
        for offset in list(set([0]) | set(offset_range)):
            current_team = [x for x in current_team if not self.__is_in_holiday__(x, current_timeslot, holidays, offset)]

        current_activities = [x for x in self.profile[current_timeslot] if not self.__is_currently_allocated_activity__(current_timeslot, x)]

        if len(current_team) > 0 and len(current_activities) > 0:
            # instantiate a new problem
            problem = Problem()

            '''
            shuffle(current_team)
            shuffle(current_activities)
            '''

            # add the different activities to allocate
            problem.addVariable(self.nephrologist_key, current_team)  # the whole nephrologists minus nephrologists in vacation on this specific day/shift
            problem.addVariable(self.activity_key, current_activities)  # the whole nephrologists that can be allocated on this specific day/shift

            # constraints declaration
            problem.addConstraint(AllDifferentConstraint())
            problem.addConstraint(lambda nep, act: act in nep.activities, (self.nephrologist_key, self.activity_key))

            return current_team, problem
        else:
            return current_team, None

    def __allocate_whole_day__(self, constraint_level, yesterday_profile, holidays):
        for current_timeslot in self.profile:
            if ConstraintStrategy.contains(ConstraintStrategy.ALLOCATE_WEEKEND_DAYS.value, constraint_level):
                '''
                    N must have clearance for all the activities: [[OTHERS, DIALYSIS, OBLIGATION]|[OBLIGATION_HOLIDAY] + [OBLIGATION_WEEKEND]]
                    N must minimize counters for OBLIGATION_WEEKEND, then optionally for [OTHERS, DIALYSIS, OBLIGATION] or [OBLIGATION_HOLIDAY]

                    N does OTHERS on FIRST_SHIFT (or OBLIGATION_HOLIDAY if DAY is holiday)
                    N does DIALYSIS on SECOND_SHIFT (or OBLIGATION_HOLIDAY if DAY is holiday)
                    N does OBLIGATION on THIRD_SHIFT (or OBLIGATION_HOLIDAY if DAY is holiday)
                    N does OBLIGATION_WEEKEND on all SHIFTS, DAY+1
                    N does OBLIGATION_WEEKEND on all SHIFTS, DAY+2

                    Where:
                    - N: the chosen nephrologist
                    - DAY: Friday
                '''

                if self.weekday == 4:  # friday
                    if current_timeslot == TimeSlot.FIRST_SHIFT:
                        current_team, problem = self.__team_problem__(current_timeslot, holidays, range(1, 4))
                        # print(current_team)

                        if problem is not None:
                            # nephrologist has to have clearance for following activities: Activity.OTHERS, Activity.DIALYSIS, Activity.OBLIGATION
                            problem.addConstraint(lambda nep: Activity.OTHERS in nep.activities and Activity.DIALYSIS in nep.activities and Activity.OBLIGATION in nep.activities, (self.nephrologist_key))

                            # nephrologist with lesser contribution to weekend obligation activity is selected
                            problem.addConstraint(lambda nep: True in [self.__is_most_rested_nephrologist__(current_team, nep, Activity.OBLIGATION_WEEKEND)], (self.nephrologist_key))

                            solutions = problem.getSolutions()
                            if len(solutions) > 0:
                                current_shift_activities = list(set([Activity.OTHERS] + self.obligation_activities) & set([x for x in self.profile[current_timeslot]]))
                                if len(current_shift_activities) == 1:
                                    # extracting the nephrologist resolved from the constraint problem solving
                                    eligible_one = solutions[0][self.nephrologist_key]

                                    # allocating the nephrologist on his TimeSlot.FIRST_SHIFT for Activity.OTHERS
                                    self.__slot__(current_timeslot, current_shift_activities[0], eligible_one)

                                    # allocating the recovery shift to nephrologist under obligation for next week.
                                    recovery_shift = None
                                    recovery_preferences = [(x, y) for x in eligible_one.preferences for y in eligible_one.preferences[x] if Activity.OBLIGATION_RECOVERY in eligible_one.preferences[x][y]]
                                    if len(recovery_preferences) == 0:  # eligible nephrologist has no preferences for obligation recovery
                                        # generating all possible recovery shifts for the eligible nephrologist within day [0, 4] for Activity.OBLIGATION_RECOVERY that has not a negative score
                                        recovery_possibilities = [(x, y) for x in [0, 1, 2, 3, 4] for y in [TimeSlot.FIRST_SHIFT, TimeSlot.SECOND_SHIFT] if eligible_one.score(x, y, Activity.OBLIGATION_RECOVERY) == 0]
                                        # picking one randomly out of all the possible shifts list
                                        if len(recovery_possibilities) > 0:
                                            recovery_shift = recovery_possibilities[randint(0, len(recovery_possibilities)-1)]
                                            # recovery_shift = recovery_possibilities[0]
                                    else:  # eligible nephrologist has at least one preferential shift for Activity.OBLIGATION_RECOVERY
                                        # picking one preference out of the preference list in a random fashion
                                        recovery_shift = recovery_preferences[randint(0, len(recovery_preferences)-1)]
                                        # recovery_shift = recovery_preferences[0]

                                    # TODO: recompute holidays to take modification into account!
                                    # print(str(eligible_one) + ": " + str(recovery_shift))
                                    if recovery_shift is not None:
                                        recovery_index_day, recovery_slot = recovery_shift
                                        eligible_one.holidays.append(FreeSlots(self.date + timedelta(days=3+recovery_index_day), [recovery_slot]))
                    else:
                        # retrieving the nephrologist allocated for imminent weekend obligation
                        last_shift_activities = list(set([Activity.OTHERS] + self.obligation_activities) & set([x for x in self.profile[TimeSlot.FIRST_SHIFT]]))
                        if len(last_shift_activities) == 1:
                            if current_timeslot == TimeSlot.SECOND_SHIFT:
                                current_shift_activities = list(set([Activity.DIALYSIS] + self.obligation_activities) & set([x for x in self.profile[current_timeslot]]))
                                if len(current_shift_activities) == 1:
                                    # allocating the nephrologist on his TimeSlot.SECOND_SHIFT for Activity.DIALYSIS
                                    self.__slot__(current_timeslot, current_shift_activities[0], self.profile[TimeSlot.FIRST_SHIFT][last_shift_activities[0]])
                            elif current_timeslot == TimeSlot.THIRD_SHIFT:
                                current_shift_activities = list(set([Activity.OBLIGATION] + self.obligation_activities) & set([x for x in self.profile[current_timeslot]]))
                                if len(current_shift_activities) == 1:
                                    # allocating the nephrologist on his TimeSlot.THIRD_SHIFT for Activity.OBLIGATION
                                    self.__slot__(current_timeslot, current_shift_activities[0], self.profile[TimeSlot.FIRST_SHIFT][last_shift_activities[0]])
                elif self.weekday in [5, 6] and yesterday_profile is not None and TimeSlot.THIRD_SHIFT in yesterday_profile:  # saturday, sunday
                    yesterday_obligations = list(set(self.obligation_activities) & set([x for x in yesterday_profile[TimeSlot.THIRD_SHIFT]]))
                    if len(yesterday_obligations) == 1 and yesterday_profile[TimeSlot.THIRD_SHIFT][yesterday_obligations[0]] is not None:
                        today_activities = list(set(self.obligation_activities) & set([x for x in self.profile[current_timeslot]]))
                        if len(today_activities) == 1:
                            self.__slot__(current_timeslot, today_activities[0], yesterday_profile[TimeSlot.THIRD_SHIFT][yesterday_obligations[0]])
            elif ConstraintStrategy.contains(ConstraintStrategy.ALLOCATE_HOLIDAYS.value, constraint_level):
                current_team, problem = self.__team_problem__(current_timeslot, holidays)

                if current_timeslot == TimeSlot.FIRST_SHIFT:
                    if problem is not None:
                        # nephrologist with lesser contribution to weekend obligation activity is selected
                        problem.addConstraint(lambda nep: True in [self.__is_most_rested_nephrologist__(current_team, nep, Activity.OBLIGATION_HOLIDAY)], (self.nephrologist_key))
                        solutions = problem.getSolutions()
                        if len(solutions) > 0:
                            current_shift_activities = list(set([Activity.OBLIGATION_HOLIDAY]) & set([x for x in self.profile[current_timeslot]]))
                            if len(current_shift_activities) == 1:
                                self.__slot__(current_timeslot, current_shift_activities[0], solutions[0][self.nephrologist_key])
                else:
                    last_shift_activities = list(set([Activity.OBLIGATION_HOLIDAY]) & set([x for x in self.profile[TimeSlot.FIRST_SHIFT]]))
                    if len(last_shift_activities) == 1:
                        current_shift_activities = list(set([Activity.OBLIGATION_HOLIDAY]) & set([x for x in self.profile[current_timeslot]]))
                        if len(current_shift_activities) == 1:
                            self.__slot__(current_timeslot, current_shift_activities[0], self.profile[TimeSlot.FIRST_SHIFT][last_shift_activities[0]])

    def __allocate_timeslot__(self, constraint_level, yesterday_profile, current_timeslot, holidays):
        if ConstraintStrategy.contains(ConstraintStrategy.ALLOCATE_MORNING_DIALYSIS.value, constraint_level):
            if current_timeslot == TimeSlot.FIRST_SHIFT and yesterday_profile is not None and TimeSlot.THIRD_SHIFT in yesterday_profile:
                yesterday_obligations = list(set(self.obligation_activities) & set([x for x in yesterday_profile[TimeSlot.THIRD_SHIFT]]))
                if len(yesterday_obligations) == 1 and yesterday_profile[TimeSlot.THIRD_SHIFT][yesterday_obligations[0]] is not None:
                    today_activities = list(set([Activity.DIALYSIS] + self.obligation_activities) & set([x for x in self.profile[current_timeslot]]))
                    if len(today_activities) == 1:
                        self.__slot__(current_timeslot, today_activities[0], yesterday_profile[TimeSlot.THIRD_SHIFT][yesterday_obligations[0]])
                    # problem.addConstraint(lambda nep, act: act in [Activity.DIALYSIS] + obligation_activities and nep.id == yesterday_profile[TimeSlot.THIRD_SHIFT][yesterday_obligations[0]].id, (self.nephrologist_key, self.activity_key))
        else:
            current_team, problem = self.__team_problem__(current_timeslot, holidays)

            if problem is not None:
                if ConstraintStrategy.contains(ConstraintStrategy.FOCUS_ON_PREFERENCES.value, constraint_level):
                    problem.addConstraint(lambda nep, act: nep.score(self.weekday, current_timeslot, act) > 0, (self.nephrologist_key, self.activity_key))
                else:
                    # avoid strict equality to take into account that more than one nephrologist could have the same preference...
                    problem.addConstraint(lambda nep, act: nep.score(self.weekday, current_timeslot, act) >= 0, (self.nephrologist_key, self.activity_key))

                if not ConstraintStrategy.contains(ConstraintStrategy.DISCARD_COUNTERS.value, constraint_level):
                    problem.addConstraint(lambda nep, act: self.__is_most_rested_nephrologist__(current_team, nep, act), (self.nephrologist_key, self.activity_key))
                    pass

                solutions = problem.getSolutions()

                retry = False
                for solution in solutions:
                    if solution[self.nephrologist_key].id not in self.__currently_allocated_nephrologists__(current_timeslot):
                        retry |= self.__slot__(current_timeslot, solution[self.activity_key], solution[self.nephrologist_key])

                if retry:
                    self.__allocate_timeslot__(constraint_level, yesterday_profile, current_timeslot, holidays)

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
































