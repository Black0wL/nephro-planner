__author__ = "Christophe"

from datetime import date, datetime, timedelta
from Enums.timeslot import TimeSlot
from Utils.constants import Constants
import calendar


class DateDuration():
    """ constructor of the class

        @param _lower_date: initial absolute date and time reference.
        @type _lower_date: datetime
        @param _upper_date: final absolute date and time reference.
        @type _upper_date: datetime

    """
    def __init__(self, _lower_date, _upper_date):
        if _lower_date and _upper_date and _lower_date > _upper_date:
            raise UserWarning("lower bound parameter should be strictly lower to upper bound parameter.")

        if _lower_date:
            if not isinstance(_lower_date, date):
                raise UserWarning("lower bound parameter must be of {}.".format(date))
        self.lower_date = _lower_date  # date NULL

        if _upper_date:
            if not isinstance(_upper_date, date):
                raise UserWarning("upper bound parameter must be of {}.".format(date))
        self.upper_date = _upper_date  # date NULL

    def __transform__(self, month_planning):
        first_date, last_date = month_planning.__first_last_key_dates__()

        if datetime(self.lower_date.year, self.lower_date.month, self.lower_date.day) < datetime(first_date.year, first_date.month, first_date.day):
            lower_bound = first_date
        else:
            lower_bound = self.lower_date

        if datetime(self.upper_date.year, self.upper_date.month, self.upper_date.day) > datetime(last_date.year, last_date.month, last_date.day):
            upper_bound = last_date
        else:
            upper_bound = self.upper_date

        map = dict()
        for i in range((upper_bound - lower_bound).days + 1):
            map[lower_bound + timedelta(days=i)] = TimeSlot.flags()

        return map