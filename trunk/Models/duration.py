__author__ = "Christophe"

from Utils.datetime_extension import datetime
from Utils.timedelta_extension import timedelta
from Enums.timeslot import TimeSlot
from Utils.constants import Constants
import calendar


class Duration():
    """ constructor of the class

        @param _lower_bound: initial absolute date and time reference.
        @type _lower_bound: datetime
        @param _upper_bound: final absolute date and time reference.
        @type _upper_bound: datetime

        Technical note on timedeltas: only days, seconds and microseconds are stored internally.
    """
    def __init__(self, _lower_bound, _upper_bound):
        if _lower_bound and _upper_bound and _lower_bound < _upper_bound:
            raise UserWarning("lower bound parameter should be strictly lower to upper bound parameter.")

        if _lower_bound:
            if not isinstance(_lower_bound, datetime):
                raise UserWarning("lower bound parameter must be of {}.".format(datetime))
        self.lower_bound = _lower_bound  # date NULL

        if _upper_bound:
            if not isinstance(_upper_bound, datetime):
                raise UserWarning("upper bound parameter must be of {}.".format(datetime))
        self.upper_bound = _upper_bound  # date NULL

    def __transform__(self, _year, _month):
        _lowest = datetime(_year, _month, 1)
        _uppest = datetime(_year, _month, calendar.monthrange(_year, _month)[1]) + timedelta(days=1, microseconds=-1)

        # bound duration within the current month
        _lower_bound = self.lower_bound if self.lower_bound > _lowest else _lowest
        _upper_bound = self.upper_bound if self.upper_bound < _uppest else _uppest

        _lower_bound_day = _lower_bound.date().day
        _upper_bound_day = _upper_bound.date().day

        if _lower_bound_day < _upper_bound_day:  # several-days duration
            for _day in [y for _week in calendar.monthcalendar(_year, _month) for y in _week if y != 0 and _lower_bound_day <= y <= _upper_bound_day]:
                if _day == _lower_bound_day:  # first duration day
                    _referential = datetime(_year, _month, _day)
                    _fragment = {_day: []}
                    for _time_slot in Constants.slots_temporally:
                        _lower, _upper = Constants.slots_temporally[_time_slot]
                        # all time slot AFTER _lower_bound are included
                        if _lower_bound <= _referential + _lower:
                            _fragment[_day].append(_time_slot)
                elif _day == _upper_bound_day:  # last duration day
                    _referential = datetime(_year, _month, _day)
                    _fragment = {_day: []}
                    for _time_slot in Constants.slots_temporally:
                        _lower, _upper = Constants.slots_temporally[_time_slot]
                        # all time slot BEFORE _upper_bound are included
                        if _referential + _upper <= _upper_bound:
                            _fragment[_day].append(_time_slot)
                else:
                    yield {
                        _day: TimeSlot.flags()  # all day included
                    }
        elif _lower_bound_day == _upper_bound_day:  # single-day duration
            _referential = datetime(_year, _month, _lower_bound_day)
            _fragment = {_lower_bound_day: []}
            for _time_slot in Constants.slots_temporally:
                _lower, _upper = Constants.slots_temporally[_time_slot]
                # all time slot AFTER _lower_bound are included
                if _lower_bound <= _referential + _lower and _referential + _upper <= _upper_bound:
                    _fragment[_lower_bound_day].append(_time_slot)






























