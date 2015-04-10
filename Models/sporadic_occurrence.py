__author__ = "Christophe"

from Utils.timedelta_extension import timedelta
from datetime import datetime
from Enums.timeslot import TimeSlot
from Utils.constants import Constants
import calendar


class SporadicOccurrence():
    """ constructor of the class

        @param _offset: relative positive offset from first day of a specific month.
        @type _offset: timedelta
        @param _progressive_period: positive period.
        @type _progressive_period: timedelta
        @param _onward: tells whether .
        @type _onward: bool

        Technical note on timedeltas: only days, seconds and microseconds are stored internally.
    """
    def __init__(self, _offset, _progressive_period=None, _onward=True):
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

    def __transform__(self, month_planning):
        _map = dict()  # map { day_number: [off_time_slots]}
        _lowest, _highest = month_planning.__first_last_key_dates__()
        if self.offset:
            _lowest += self.offset

        _datetimes = []

        _current = _lowest  # initialization
        if self.progressive_period:
            while _lowest <= _current <= _highest:
                _datetimes.append(_current)
                _current += self.progressive_period
        else:
            _datetimes.append(_current)

        for _datetime in _datetimes:
            _map[_datetime] = TimeSlot.flags()  # all day included

        return _map



























