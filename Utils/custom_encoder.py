__author__ = 'Christophe'

from json import JSONEncoder
from Models.nephrologist import Nephrologist
from Enums.activity import Activity
from Enums.timeslot import TimeSlot
from collections import Counter
from Models.preferences import Preferences
from Models.aversions import Aversions
from datetime import date


class CustomEncoder(JSONEncoder):
    def default(self, o):
        def __regular_enum__(p):
            return p.name

        def __regular_dict__(p):
            return dict([(self.default(key), self.default(value)) for key, value in p.iteritems()])

        def __regular_t2a__(p):
            return dict([(str(weekday), dict([(__regular_enum__(timeslot), [__regular_enum__(activity) for activity in activities]) for timeslot, activities in timeslot2activities.iteritems()])) for weekday, timeslot2activities in p.iteritems()])

        if isinstance(o, Nephrologist):
            return {"__nephrologist__": __regular_dict__(vars(o))}
            # return dict({"__type__": Nephrologist}, **__regular_dict__(vars(o)))
        elif isinstance(o, list):
            return [self.default(value) for value in o]
        elif isinstance(o, Preferences):
            return {"__preferences__": __regular_t2a__(o)}
        elif isinstance(o, Aversions):
            return {"__aversions__": __regular_t2a__(o)}
        elif isinstance(o, Activity):
            return __regular_enum__(o)
        elif isinstance(o, TimeSlot):
            return __regular_enum__(o)
        elif isinstance(o, Counter):
            return {"__counter__": __regular_dict__(o)}
        elif isinstance(o, date):
            return {"__date__": date.strftime(o, "%Y-%m-%d")}
        elif isinstance(o, int):
            return o
        else:
            return str(o)