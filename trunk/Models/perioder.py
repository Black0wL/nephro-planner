__author__ = "Christophe"

from datetime import timedelta, date


class Perioder():
    # Reminder on timedelta: only days, seconds and microseconds are stored internally.
    def __init__(self, _initial_delta=None, _initial_date=date.min, _frequency=None, _final_delta=None, _final_date=date.max):
        self.initial_delta = _initial_delta  # timedelta  NULL
        self.initial_date = _initial_date  # date NULL
        self.frequency = _frequency  # timedelta NULL
        self.final_delta = _final_delta  # timedelta NULL
        self.final_date = _final_date  # date NULL
        self.is_coherent()

    def __str__(self):
        return super(self)

    def __repr__(self):
        return self.__str__()

    def to_slots(self):
        pass

    def to_dates(self):
        self.is_coherent()
        current = self.initial_date
        if self.frequency and self.final_delta:
            while current < self.final_delta:
                yield current
                current += self.frequency
        else:
            yield current

    # TODO: add to the notion of coherence the dates (not only the timedeltas)
    def is_coherent(self):
        if type(self.initial_delta) is not timedelta:
            raise UserWarning("initial parameter must be of {}.".format(timedelta))
        if self.frequency:
            if type(self.frequency) is not timedelta:
                raise UserWarning("frequency parameter must be of {}.".format(timedelta))
            if not self.final_delta:
                raise UserWarning("when frequency parameter is set, final parameter must as well be.")
        if self.final_delta:
            if type(self.final_delta) is not timedelta:
                raise UserWarning("final parameter must be of {}.".format(timedelta))
            if self.final_delta <= self.initial_delta:
                raise UserWarning("final parameter precedes or equals initial parameter.")