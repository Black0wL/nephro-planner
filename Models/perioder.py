__author__ = "Christophe"

from datetime import timedelta, date


class Perioder():

    """ constructor of the class

        @param _initial_delta: initial relative time reference.
        @type _initial_delta: timedelta
        @param _initial_date: initial absolute time reference.
        @type _initial_date: timedelta
        @param _frequency: period on which _initial.
        @type _frequency: timedelta
        @param _final_delta: initial relative time reference.
        @type _final_delta: timedelta
        @param _final_date: initial relative time reference.
        @type _final_date: timedelta

        Tips for compliant usage of class:
        ==> _initial_delta XOR _initial_date = True
        ==> _final_delta XOR _final_date = True

        Technical note on timedeltas: only days, seconds and microseconds are stored internally.
    """
    def __init__(self, _initial_delta=None, _initial_date=None, _frequency=None, _final_delta=None, _final_date=None):
        if bool(_initial_delta) != bool(_initial_date):
            raise UserWarning("initial delta and initial date must result to True to a XOR operation.")

        if bool(_final_delta) != bool(_final_date):
            raise UserWarning("initial delta and initial date must result to True to a XOR operation.")

        if _initial_delta and type(_initial_delta) is not timedelta:
            raise UserWarning("initial delta parameter must be of {}.".format(timedelta))
        self.initial_delta = _initial_delta  # timedelta  NULL

        if _initial_date and type(_initial_date) is not date:
            raise UserWarning("initial date parameter must be of {}.".format(date))
        self.initial_date = _initial_date  # date NULL

        if _frequency and type(_frequency) is not timedelta:
            raise UserWarning("frequency parameter must be of {}.".format(timedelta))
        self.frequency = _frequency  # timedelta NULL

        if _final_delta and type(_final_delta) is not timedelta:
            raise UserWarning("final delta parameter must be of {}.".format(timedelta))
        self.final_delta = _final_delta  # timedelta NULL

        if _final_date and type(_final_date) is not date:
            raise UserWarning("final date parameter must be of {}.".format(date))
        self.final_date = _final_date  # date NULL



    def __str__(self):
        return super(self)

    def __repr__(self):
        return self.__str__()

    def to_slots(self):
        pass