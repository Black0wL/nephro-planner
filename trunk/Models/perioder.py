__author__ = "Christophe"

from Utils.datetime_modulo import datetime
from datetime import timedelta, date


class Perioder():
    """ constructor of the class

        @param _lower_delta: initial relative time reference.
        @type _lower_delta: timedelta
        @param _lower_date: initial absolute time reference.
        @type _lower_date: timedelta
        @param _period: period on which _initial.
        @type _period: timedelta
        @param _upper_delta: initial relative time reference.
        @type _upper_delta: timedelta
        @param _upper_date: initial relative time reference.
        @type _upper_date: timedelta

        Technical note on timedeltas: only days, seconds and microseconds are stored internally.

        As relative referential, we use first monday of a specific month.
    """
    def __init__(self, _lower_delta=None, _lower_date=None, _period=None, _upper_delta=None, _upper_date=None):
        if _lower_delta:
            if not isinstance(_lower_delta, timedelta):
                raise UserWarning("lower delta parameter must be of {}.".format(timedelta))
        self.lower_delta = _lower_delta  # timedelta  NULL

        if _lower_date:
            if not isinstance(_lower_date, date):
                raise UserWarning("lower date parameter must be of {}.".format(date))
        self.lower_date = _lower_date  # date NULL

        if _period:
            if not isinstance(_period, timedelta):
                raise UserWarning("period parameter must be of {}.".format(timedelta))
        self.period = _period  # timedelta NULL

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
    # TODO: implement!
    def __expand__(self, _year, _month):
        """

        :rtype : list
        """
        import calendar

        _lower_bound = date(_year, _month, 1)
        _upper_bound = calendar.monthrange(_year, _month)[1] + timedelta(days=1, microseconds=-1)

        #for _week in calendar.monthcalendar(_year, _month):
        #    for _day in [x for x in _week if x != 0]:
        if self.lower_delta or self.upper_delta:  # self is relatively defined
            pass
        elif self.lower_date or self.upper_date:  # self is absolutely defined
            if not (self.lower_delta or self.upper_delta):
                if self.period:
                    # converting our date to a datetime instance
                    _current = datetime(_absolute_date.year, _absolute_date.month, _absolute_date.day)

                    if self.lower_date

                    while _current <= _upper_bound:
                        if _current >= _lower_bound:
                            yield _current
                        _current += timedelta(
                            days=self.period.days,
                            seconds=self.period.seconds,
                            microseconds=self.period.microseconds
                        )
                elif _lower_bound <= _absolute_date <= _upper_bound:
                    yield _absolute_date
            else:
                pass
        else:
            yield

































