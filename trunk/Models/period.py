__author__ = "Christophe"

from Utils.timedelta_extension import timedelta
from Utils.datetime_extension import datetime
from Enums.timeslot import TimeSlot
import calendar


class Period():
    FIRST_SHIFT_LOWER_BOUND = 5
    SECOND_SHIFT_LOWER_BOUND = 13
    THIRD_SHIFT_LOWER_BOUND = 21
    """ mapper between discrete time slots and analogous datetime

        FIRST_SHIFT: from 05:00:00 to 12:59:59.999999
        SECOND_SHIFT: from 13:00:00 to 20:59:59.999999
        SECOND_SHIFT: from 21:00:00 to 04:59:59.999999
    """
    slots_temporally = {
        TimeSlot.FIRST_SHIFT: (
            timedelta(hours=FIRST_SHIFT_LOWER_BOUND),
            timedelta(hours=SECOND_SHIFT_LOWER_BOUND, microseconds=-1)
        ),
        TimeSlot.SECOND_SHIFT: (
            timedelta(hours=SECOND_SHIFT_LOWER_BOUND),
            timedelta(hours=THIRD_SHIFT_LOWER_BOUND, microseconds=-1)
        ),
        TimeSlot.THIRD_SHIFT: (
            timedelta(hours=THIRD_SHIFT_LOWER_BOUND),
            timedelta(days=1, hours=FIRST_SHIFT_LOWER_BOUND, microseconds=-1)
        )
    }

    """ constructor of the class

        @param _offset: relative positive offset from first monday of a specific month.
        @type _offset: timedelta
        @param _progressive_period: positive period.
        @type _progressive_period: timedelta

        Technical note on timedeltas: only days, seconds and microseconds are stored internally.
    """
    def __init__(self, _offset, _progressive_period):
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

    # TODO: implement
    def __transform__(self, _year, _month):
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

        for _day in [y for _week in calendar.monthcalendar(_year, _month) for y in _week if y != 0]:
            _referential = datetime(_year, _month, _day)
            for _datetime in _datetimes:
                if not _datetime.time():  # holiday is all day
                    yield {
                        _day: TimeSlot.flags()
                    }
                    continue
                else:
                    _fragment = {_day: []}
                    for _time_slot, _lower in [(x, y) for x in Period.slots_temporally for (y, z) in Period.slots_temporally[TimeSlot.FIRST_SHIFT]]:
                        if _referential + _lower <= _datetime:
                            _fragment[_day].append(_time_slot)

                    if _fragment[_day]:
                        yield _fragment[_day]



























