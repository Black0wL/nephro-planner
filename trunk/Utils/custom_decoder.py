__author__ = 'Christophe'

from json import JSONDecoder
from Models.nephrologist import Nephrologist
from Enums.activity import Activity
from Enums.timeslot import TimeSlot
from collections import Counter
from Models.preferences import Preferences
from Models.aversions import Aversions
from datetime import datetime


class CustomDecoder(JSONDecoder):
    '''
    def decode(self, o):
        def __regular_t2a__(p):
            return dict([(int(key), dict([(TimeSlot.__from_string__(timeslot), [Activity.__from_string__(activity) for activity in activities]) for timeslot, activities in timeslot2activites.iteritems()])) for key, timeslot2activites in p.iteritems()])

        if isinstance(o, list):
            print("LIST")
            return [self.decode(value) for value in o]
        elif "__nephrologist__" in o:
            print("Nephrologist")
            print(len(o))
            print(type(o))
            print("__nephrologist__" in o)
            nephrologist = o["__nephrologist__"]
            print(nephrologist["id"])
            id = int(nephrologist["id"]) if "id" in nephrologist else None
            name = nephrologist["name"] if "name" in nephrologist else None
            activities = [Activity.__from_string__(flag) for flag in nephrologist["activities"] if "activities" in nephrologist]
            holidays = [self.decode(value) for value in nephrologist["holidays"] if "holidays" in nephrologist]
            preferences = self.decode(nephrologist["preferences"]) if "preferences" in nephrologist else None
            aversions = self.decode(nephrologist["aversions"]) if "aversions" in nephrologist else None
            counters = self.decode(nephrologist["initial_counters"]) if "initial_counters" in nephrologist else None
            return Nephrologist(id, name, activities, holidays, preferences, aversions, counters)
        elif "__date__" in o:
            return datetime.datetime.strptime(o["__date__"], "%Y-%m-%d").date()
        elif "__preferences__" in o:
            return Preferences(__regular_t2a__(o["__preferences__"]))
        elif "__aversions__" in o:
            return Preferences(__regular_t2a__(o["__aversions__"]))
        elif "__counter__" in o:
            return Counter(dict([(Activity.__from_string__(key), value) for key, value in o["__counter__"].iteritems()]))
        else:
            return super(CustomDecoder, self).decode(o)
    '''
    '''
    @classmethod
    def __master_object_hook__(o, a):
        def __regular_t2a__(p):
            return dict([(int(key), dict([(TimeSlot.__from_string__(timeslot), [Activity.__from_string__(activity) for activity in activities]) for timeslot, activities in timeslot2activites.iteritems()])) for key, timeslot2activites in p.iteritems()])

        print(o)

        if isinstance(o, list):
            print("LIST")
            return [CustomDecoder.__master_object_hook__(value) for value in o]
        elif "__nephrologist__" in o:
            print("Nephrologist")
            print(len(o))
            print(type(o))
            print("__nephrologist__" in o)
            nephrologist = o["__nephrologist__"]
            print(nephrologist["id"])
            id = int(nephrologist["id"]) if "id" in nephrologist else None
            name = nephrologist["name"] if "name" in nephrologist else None
            activities = [Activity.__from_string__(flag) for flag in nephrologist["activities"] if "activities" in nephrologist]
            holidays = [CustomDecoder.__master_object_hook__(value) for value in nephrologist["holidays"] if "holidays" in nephrologist]
            preferences = CustomDecoder.__master_object_hook__(nephrologist["preferences"]) if "preferences" in nephrologist else None
            aversions = CustomDecoder.__master_object_hook__(nephrologist["aversions"]) if "aversions" in nephrologist else None
            counters = CustomDecoder.__master_object_hook__(nephrologist["initial_counters"]) if "initial_counters" in nephrologist else None
            return Nephrologist(id, name, activities, holidays, preferences, aversions, counters)
        elif "__date__" in o:
            return datetime.datetime.strptime(o["__date__"], "%Y-%m-%d").date()
        elif "__preferences__" in o:
            return Preferences(__regular_t2a__(o["__preferences__"]))
        elif "__aversions__" in o:
            return Preferences(__regular_t2a__(o["__aversions__"]))
        elif "__counter__" in o:
            return Counter(dict([(Activity.__from_string__(key), value) for key, value in o["__counter__"].iteritems()]))
        else:
            return o
    '''