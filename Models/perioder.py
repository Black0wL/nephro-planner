__author__ = "Christophe"

from Utils.timedelta_extension import timedelta
from Models.sporadic_occurrence import SporadicOccurrence
from datetime import date, datetime


"""
    With this class, we want to deal with the following scenarii:
    - absolute date duration: from 2014-06-12 to 2014-06-15

    We do not need the following scenarii:
    - date only: 2014-06-12
    - absolute datetime duration: from 2014-06-12T12:00:00 to 2014-06-15T05:00:00
    - relative date period: every monday
    - relative backward datetime period: every monday (from 00:00:00.000000) to 12:00:00
    - relative onward datetime period: every monday since 12:00:00 (to 23:59:59.999999)
    - datetime only
    - relative&absolute onward date period: from 2014-06-12 every monday
    - relative&absolute onward datetime period: from 2014-06-12T10:00:00 every monday morning
    - relative&absolute backward date period: every monday until 2014-06-15
    - relative&absolute backward datetime period: every monday morning until 2014-06-15T16:00:00
"""

'''
class Perioder():
    """ constructor of the class

        @param _lower_date: initial absolute time reference.
        @type _lower_date: datetime
        @param _upper_date: initial relative time reference.
        @type _upper_date: datetime

    """
    def __init__(self, _lower_date=None, _upper_date=None):
        if _lower_date:
            if not isinstance(_lower_date, date):
                raise UserWarning("lower date parameter must be of {}.".format(date))
        self.lower_date = _lower_date  # date NULL

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
    def __transform__(self, _year, _month):
        """

        :rtype : (tuple(datetime, datetime), bool)
        :returns : a set of periods and a flag telling whether periods are a single time lap (instead of punctual dates)
        """
        import calendar

        _lower_bound = date(_year, _month, 1)
        _upper_bound = date(_year, _month, calendar.monthrange(_year, _month)[1])

        if self.lower_date:
            _lower_datetime = datetime(self.lower_date.year, self.lower_date.month, self.lower_date.day)
            if _lower_datetime > datetime(_lower_bound.year, _lower_bound.month, _lower_bound.day):
                _lower_date = self.lower_date
            else:
                _lower_date = _lower_bound
        else:
            _lower_date = _lower_bound

        if self.upper_date:
            _upper_datetime = datetime(self.upper_date.year, self.upper_date.month, self.upper_date.day)
            if _upper_datetime < datetime(_upper_bound.year, _upper_bound.month, _upper_bound.day):
                _upper_date = self.upper_date
            else:
                _upper_date = _upper_bound
        else:
            _upper_date = None

        _return = []
        _current = _lower_date
        while _current <= _upper_date:
            _current_as_timedelta = _current - _lower_bound
            _return.append(SporadicOccurrence(_offset=timedelta(days=_current_as_timedelta.days, seconds=_current_as_timedelta.seconds, microseconds=_current_as_timedelta.microseconds)).__transform__(_year, _month))
            if _current is _upper_date:
                break
            elif _current + timedelta(days=1) > _upper_date:
                _current = _upper_date
            else:
                _current += timedelta(days=1)

        return _return
'''
































