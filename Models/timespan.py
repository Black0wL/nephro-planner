__author__ = "Christophe"

from datetime import timedelta


class TimeSpan():
    # Reminder on timedelta: only days, seconds and microseconds are stored internally.
    def __init__(self, _initial, _frequency=None, _final=None):
        self.initial = _initial  # timedelta NOT NULL
        self.frequency = _frequency  # timedelta NULL
        self.final = _final  # timedelta NULL
        self.is_coherent()

    def __str__(self):
        return super(self)

    def __repr__(self):
        return self.__str__()

    def to_slots(self):
        pass

    def to_dates(self, ):
        self.is_coherent()
        current = self.initial
        if self.frequency and self.final:
            while current < self.final:
                yield current
                current += self.frequency
        else:
            yield current

    def is_coherent(self):
        if type(self.initial) is not timedelta:
            raise UserWarning("initial parameter must be of {}.".format(timedelta))
        if self.frequency:
            if type(self.frequency) is not timedelta:
                raise UserWarning("frequency parameter must be of {}.".format(timedelta))
            if not self.final:
                raise UserWarning("when frequency parameter is set, final parameter must as well be.")
        if self.final:
            if type(self.final) is not timedelta:
                raise UserWarning("final parameter must be of {}.".format(timedelta))
            if self.final <= self.initial:
                raise UserWarning("final parameter precedes or equals initial parameter.")

# print(time())