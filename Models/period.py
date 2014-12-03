__author__ = "Christophe"

from Utils.timedelta_extension import timedelta
from Utils.datetime_extension import datetime
from Enums.timeslot import TimeSlot
from Utils.constants import Constants
import calendar


class Period():
    """ constructor of the class

        @param _offset: relative positive offset from first monday of a specific month.
        @type _offset: timedelta
        @param _progressive_period: positive period.
        @type _progressive_period: timedelta
        @param _onward: tells whether .
        @type _onward: bool

        Technical note on timedeltas: only days, seconds and microseconds are stored internally.
    """
    def __init__(self, _offset, _progressive_period, _onward=True):
        if _offset:
            if not isinstance(_offset, timedelta):
                raise UserWarning("offset parameter must be of {}.".format(timedelta))
            elif _offset.total_microseconds() < 0:
                raise UserWarning("offset parameter must be positive.")
        self.offset = _offset  # timedelta  NULL

        if _progressive_period:
            if not isinstance(_progressive_period, timedelta):
                raise UserWarning("period parameter must be of {}.".format(timedelta))
            elif _progressive_period.total_microseconds() <= 0:
                raise UserWarning("period parameter must be strictly positive.")
        self.progressive_period = _progressive_period  # timedelta NULL

        if _onward:
            if not isinstance(_onward, bool):
                raise UserWarning("onward parameter must be of {}.".format(bool))
            self.onward = _onward
        else:
            self.onward = False

    def __transform__(self, _year, _month):
        _map = dict()  # map { day_number: [off_time_slots]}
        _lowest = datetime(_year, _month, 1)
        if self.offset:
            _lowest += self.offset
        _uppest = datetime(_year, _month, calendar.monthrange(_year, _month)[1]) + timedelta(days=1, microseconds=-1)
        _datetimes = []

        _current = _lowest  # initialization
        if self.progressive_period:
            while _lowest <= _current <= _uppest:
                _datetimes.append(_current)
                _current += self.progressive_period
        else:
            _datetimes.append(_current)

        for _day in range(_lowest.day, _uppest.day + 1):
            _referential = datetime(_year, _month, _day)
            for _datetime in _datetimes:
                if _datetime.date() == _referential.date():
                    if not _datetime.time():
                        _map[_day] = TimeSlot.flags()  # all day included
                    else:
                        _fragment = {_day: []}
                        for _time_slot in Constants.slots_temporally:
                            _lower, _upper = Constants.slots_temporally[_time_slot]
                            if self.onward:  # all time slot AFTER _datetime are included
                                if _referential + _lower >= _datetime:  # started slot are earned
                                    _fragment[_day].append(_time_slot)
                            else:  # all time slot BEFORE _datetime are included
                                if _referential + _upper <= _datetime:
                                    _fragment[_day].append(_time_slot)
                        if _fragment[_day]:
                            _map[_day] = _fragment[_day]
        return _map



























