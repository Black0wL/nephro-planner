__author__ = "Christophe"

import calendar
from week import Week
from workalendar.europe import France
from Enums.activity import Activity
from Enums.timeslot import TimeSlot
import copy


def singleton(cls):
    instances = dict()

    def __new__(_date):
        if _date not in instances:
            instances[_date] = cls(_date)
        return instances[_date]
    return __new__


@singleton
class DailyPlanning():
    def __init__(self, _date):
        self.date = _date

        # if needed, _calendar.is_working_day can deal with extra working days/holidays
        if France().is_working_day(_date):
            for _week in calendar.monthcalendar(_date.year, _date.month):
                if _date.day in _week:
                    self.profile = copy.deepcopy(Week.SLOTS[_week.index(_date.day)])
        else:
            self.profile = copy.deepcopy(Week.SLOTS[Week.KEY_SPECIAL_HOLIDAY])

        if not self.profile:
            raise UserWarning("daily planning's profile has not been successfully resolved.")

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
































