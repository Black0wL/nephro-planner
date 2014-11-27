import datetime as dt


class timedelta(dt.timedelta):
    def __div__(self, other):
        return float(self.total_microseconds()) / float(other.total_microseconds())

    def total_microseconds(self):
        return self.microseconds + 1000000 * (self.seconds + 86400 * self.days)