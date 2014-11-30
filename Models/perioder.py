__author__ = "Christophe"

from Utils.datetime_extension import datetime
from Utils.timedelta_extension import timedelta
from datetime import date


"""
    With this class, we want to deal with multiple scenarii:
    - date only: 2014-06-12
    - absolute date duration: from 2014-06-12 to 2014-06-15
    - absolute datetime duration: from 2014-06-12T12:00:00 to 2014-06-15T05:00:00
    - relative date period: every monday
    - relative backward datetime period: every monday (from 00:00:00.000000) to 12:00:00
    - relative onward datetime period: every monday since 12:00:00 (to 23:59:59.999999)

    We does not need these scenarii:
    - datetime only
    - relative&absolute onward date period: from 2014-06-12 every monday
    - relative&absolute onward datetime period: from 2014-06-12T10:00:00 every monday morning
    - relative&absolute backward date period: every monday until 2014-06-15
    - relative&absolute backward datetime period: every monday morning until 2014-06-15T16:00:00
"""


class Perioder():
    """ constructor of the class

        @param _lower_delta: initial relative time reference.
        @type _lower_delta: timedelta
        @param _lower_date: initial absolute time reference.
        @type _lower_date: timedelta
        @param _progressive_period: period on which _initial.
        @type _progressive_period: timedelta
        @param _upper_delta: initial relative time reference.
        @type _upper_delta: timedelta
        @param _upper_date: initial relative time reference.
        @type _upper_date: timedelta

        Technical note on timedeltas: only days, seconds and microseconds are stored internally.
    """
    def __init__(self, _lower_delta=None, _lower_date=None, _progressive_period=None, _upper_delta=None, _upper_date=None):
        if _lower_delta:
            if not isinstance(_lower_delta, timedelta):
                raise UserWarning("lower delta parameter must be of {}.".format(timedelta))
        self.lower_delta = _lower_delta  # timedelta  NULL

        if _lower_date:
            if not isinstance(_lower_date, date):
                raise UserWarning("lower date parameter must be of {}.".format(date))
        self.lower_date = _lower_date  # date NULL

        if _progressive_period:
            if not isinstance(_progressive_period, timedelta):
                raise UserWarning("progressive period parameter must be of {}.".format(timedelta))
        self.progressive_period = _progressive_period  # timedelta NULL

        if _upper_delta:
            if not isinstance(_upper_delta, timedelta):
                raise UserWarning("upper delta parameter must be of {}.".format(timedelta))
        self.upper_delta = _upper_delta  # timedelta NULL

        if _upper_date:
            if not isinstance(_upper_date, date):
                raise UserWarning("upper date parameter must be of {}.".format(date))
        self.upper_date = _upper_date  # date NULL

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
    def __expand__(self, _year, _month):
        """

        :rtype : (tuple(datetime, datetime), bool)
        :returns : a set of periods and a flag telling whether periods are a single time lap (instead of punctual dates)
        """
        import calendar

        _lower_bound = datetime(_year, _month, 1)
        _upper_bound = datetime(_year, _month, calendar.monthrange(_year, _month)[1]) + timedelta(days=1, microseconds=-1)

        #
        if self.lower_date and self.lower_date < _lower_bound:
            _lower_date = self.lower_date
        elif self.lower_delta:
            _lower_date = _lower_bound + self.lower_delta
        else:
            _lower_date = _lower_bound

        if self.upper_date:
            if self.upper_date <= _upper_bound:
                _upper_date = self.upper_date
            else:
                _upper_date = _upper_bound
        elif self.upper_delta:
            _upper_date = self.upper_delta
        else:
            _upper_date = None

        _return = []
        if self.progressive_period:
            _current = _lower_date
            while _current <= _upper_date:
                if _current >= _lower_date:
                    _return.append((_current, None))
                _current += timedelta(
                    days=self.progressive_period.days,
                    seconds=self.progressive_period.seconds,
                    microseconds=self.progressive_period.microseconds
                )
        else:
            _return.append((_lower_date, _upper_date))

        _return_set = set([x[1] for x in _return])
        return _return, len(_return_set) == 1 and not list(_return_set)[0]
































