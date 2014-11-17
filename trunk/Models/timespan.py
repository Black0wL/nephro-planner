__author__ = "Christophe"

class TimeSpan():
    def __init__(self, _initial, _frequency, _final):
        self.initial = _initial  # datetime NOT NULL
        if _frequency is not None:
            self.frequency = _frequency  # timedelta NULL
        if _final is not None:
            self.final = _final  # datetime NULL

    def __str__(self):
        return super(self)

    def __repr__(self):
        return self.__str__()