__author__ = "Christophe"

from Utils.datetime_extension import datetime
from Utils.timedelta_extension import timedelta
from Enums.timeslot import TimeSlot
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
        if _lower_bound:
            if not isinstance(_lower_bound, datetime):
                raise UserWarning("lower bound parameter must be of {}.".format(datetime))
        self.lower_date = _lower_bound  # date NULL

        if _upper_bound:
            if not isinstance(_upper_bound, datetime):
                raise UserWarning("upper bound parameter must be of {}.".format(datetime))
        self.upper_date = _upper_bound  # date NULL

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
                if not _datetime.time():
                    yield {
                        _day: TimeSlot.flags()
                    }
                    continue
                else:
                    pass

                if TimeSlot.FIRST_SHIFT:
                    _lower, _upper = Period.slots_temporally[TimeSlot.FIRST_SHIFT]
                    if _referential + _lower <= _datetime <= _referential + _upper:
                        yield {
                            _day: [
                                TimeSlot.SECOND_SHIFT,
                                TimeSlot.THIRD_SHIFT
                            ]
                        }
                elif TimeSlot.SECOND_SHIFT:
                    _lower, _upper = Period.slots_temporally[TimeSlot.FIRST_SHIFT]
                    if _referential + _lower <= _datetime <= _referential + _upper:
                        yield {
                            _day: [
                                TimeSlot.THIRD_SHIFT
                            ]
                        }
                else:
                    continue