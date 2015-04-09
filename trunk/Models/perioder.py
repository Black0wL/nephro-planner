__author__ = "Christophe"

from Utils.timedelta_extension import timedelta
from Models.period import Period
from datetime import datetime


"""
    With this class, we want to deal with multiple scenarii:
    - absolute datetime duration: from 2014-06-12T12:00:00 to 2014-06-15T05:00:00

    We does not need these scenarii:
    - date only: 2014-06-12
    - absolute date duration: from 2014-06-12 to 2014-06-15
    - relative date period: every monday
    - relative backward datetime period: every monday (from 00:00:00.000000) to 12:00:00
    - relative onward datetime period: every monday since 12:00:00 (to 23:59:59.999999)
    - datetime only
    - relative&absolute onward date period: from 2014-06-12 every monday
    - relative&absolute onward datetime period: from 2014-06-12T10:00:00 every monday morning
    - relative&absolute backward date period: every monday until 2014-06-15
    - relative&absolute backward datetime period: every monday morning until 2014-06-15T16:00:00
"""


class Perioder():
    """ constructor of the class

        @param _lower_datetime: initial absolute time reference.
        @type _lower_datetime: datetime
        @param _upper_datetime: initial relative time reference.
        @type _upper_datetime: datetime

    """
    def __init__(self, _lower_datetime=None, _upper_datetime=None):
        if _lower_datetime:
            if not isinstance(_lower_datetime, datetime):
                raise UserWarning("lower date parameter must be of {}.".format(datetime))
        self.lower_datetime = _lower_datetime  # date NULL

        if _upper_datetime:
            if not isinstance(_upper_datetime, datetime):
                raise UserWarning("upper date parameter must be of {}.".format(datetime))
        self.upper_datetime = _upper_datetime  # date NULL

    def __str__(self):
        return super(self)

    def __repr__(self):
        return self.__str__()

    """ translates a Perioder instance into a set of datetimes

        @param _year: year of the temporal focus
        @type _year: int
        @param _month: month of the temporal focus
        @type _month: int
    """
    def __transform__(self, _year, _month):
        """

        :rtype : (tuple(datetime, datetime), bool)
        :returns : a set of periods and a flag telling whether periods are a single time lap (instead of punctual dates)
        """
        import calendar

        _lower_bound = datetime(_year, _month, 1)
        _upper_bound = datetime(_year, _month, calendar.monthrange(_year, _month)[1]) + timedelta(days=1, microseconds=-1)

        if self.lower_datetime:
            if self.lower_datetime > _lower_bound:
                _lower_datetime = self.lower_datetime
            else:
                _lower_datetime = _lower_bound
        else:
            _lower_datetime = _lower_bound

        if self.upper_datetime:
            if self.upper_datetime <= _upper_bound:
                _upper_date = self.upper_datetime
            else:
                _upper_date = _upper_bound
        else:
            _upper_date = None

        _return = []
        _current = _lower_datetime
        while _current <= _upper_date:
            _current_as_timedelta = _current - _lower_bound
            _return.append(Period(_offset=_current_as_timedelta).__transform__(_year, _month))
            _current += timedelta(days=1)
            if _current > _upper_date:
                _current = _upper_date

        return _return
































