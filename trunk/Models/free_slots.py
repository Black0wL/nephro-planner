__author__ = 'Christophe'

from datetime import date
from Enums.timeslot import TimeSlot


class FreeSlots():
    """ constructor of the class

        @param _date: _date on which slots are being free.
        @type _date: date
        @param _slots: the free time slots.
        @type _slots: list
        @param _is_second_shift_free: tells whether second shift is free.
        @type _is_second_shift_free: bool
        @param _is_three_shift_free: tells whether three shift is free.
        @type _is_three_shift_free: bool

    """
    def __init__(self, _date, _slots=TimeSlot.flags()):
        self.date = _date
        self.slots = _slots

    def __transform__(self, month_planning):
        _lowest, _highest = month_planning.__first_last_key_dates__()
        if _lowest <= self.date <= _highest:
            return {self.date: self.slots}
        else:
            return dict()