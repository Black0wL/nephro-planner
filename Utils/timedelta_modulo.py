import datetime as dt


class timedelta(dt.timedelta):
    def __div__(self, other):
        me = self.microseconds + 1000000 * (self.seconds + 86400 * self.days)
        her = other.microseconds + 1000000 * (other.seconds + 86400 * other.days)
        return float(me) / float(her)