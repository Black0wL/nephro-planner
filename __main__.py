#  -*- coding: utf-8 -*-
__author__ = "Christophe"

from Models.monthly_planning import MonthlyPlanning
from Models.daily_planning import DailyPlanning
from Enums.constraint_strategy import ConstraintStrategy
from Enums.timeslot import TimeSlot
from Enums.activity import Activity
import calendar
from Models.nephrologist import Nephrologist
from Utils.database import Database
from datetime import date, datetime, timedelta
from constraint import *


def main():
    try:
        # Database.__create__()
        # Nephrologist.__load__()

        '''
        from Enums.activity import Activity
        print sum([x.counters[y] for x in Database.team() for y in Activity.flags()])
        return
        '''

        '''
        import codecs
        import json
        from Utils.custom_encoder import CustomEncoder
        from Utils.python_object_encoder import PythonObjectEncoder
        from collections import Counter

        # print(json.dumps(Counter({Activity.OBLIGATION: 5}), cls=CustomEncoder, indent=4, sort_keys=True, ensure_ascii=False))

        from pprint import pprint

        with open("data.txt", "wb") as outfile:
        # with codecs.open("data.txt", "w", encoding="utf8") as outfile:
            s = json.dumps(Database.team(), cls=CustomEncoder, indent=4, sort_keys=True, encoding="utf-8")
            # s = "Séverine"
            # print s
            # s2u = u"%s" % s  # incorrect
            s2u = unicode(s, "utf-8")
            # print s2u
            sutf8 = s2u.encode("utf-8")
            # print sutf8
            outfile.write(sutf8)

        for n in Database.team():
            print repr(n)

        return



        from Models.preferences import Preferences
        from Models.aversions import Aversions
        def __recursive_object_hook__(o):
            def __regular_t2a__(p):
                return dict([(int(key), dict([(TimeSlot.__from_string__(timeslot), [Activity.__from_string__(activity) for activity in activities]) for timeslot, activities in timeslot2activites.iteritems()])) for key, timeslot2activites in p.iteritems()])

            if isinstance(o, list):
                return [__recursive_object_hook__(value) for value in o]
            elif "__nephrologist__" in o:
                nephrologist = o["__nephrologist__"]
                id = int(nephrologist["id"]) if "id" in nephrologist else None
                name = str(nephrologist["name"]) if "name" in nephrologist else None
                activities = [Activity.__from_string__(flag) for flag in nephrologist["activities"] if "activities" in nephrologist]
                holidays = [__recursive_object_hook__(value) for value in nephrologist["holidays"] if "holidays" in nephrologist]
                preferences = __recursive_object_hook__(nephrologist["preferences"]) if "preferences" in nephrologist else None
                aversions = __recursive_object_hook__(nephrologist["aversions"]) if "aversions" in nephrologist else None
                counters = __recursive_object_hook__(nephrologist["initial_counters"]) if "initial_counters" in nephrologist else None
                return Nephrologist(id, name, activities, holidays, preferences, aversions, counters)
            elif "__date__" in o:
                return datetime.strptime(o["__date__"], "%Y-%m-%d").date()
            elif "__preferences__" in o:
                return Preferences(__regular_t2a__(o["__preferences__"]))
            elif "__aversions__" in o:
                return Aversions(__regular_t2a__(o["__aversions__"]))
            elif "__counter__" in o:
                return Counter(dict([(Activity.__from_string__(key), value) for key, value in o["__counter__"].iteritems()]))
            else:
                return o

        from Utils.custom_decoder import CustomDecoder
        with open("data.txt", "rb") as infile:
            # reads = unicode(infile.read(), 'utf-8')
            reads = infile.read().decode("utf-8")
            print(reads)
            # print(reads)
            # data = CustomDecoder().decode(reads)
            data = json.loads(reads, object_hook=__recursive_object_hook__)
            print(type(data))
            print pprint(data)
        return
        '''







        year = 2015
        month = 5
        month_planning = MonthlyPlanning(year, month)
        month_planning.__compute__()

        '''
        print("--------------------------------------------------")
        for x in Database.team():
            print(repr(x) + ": " + str(x.counters()))
        '''

        '''
        for y in current_daily_planning.profile:
            print(str(today) + "|" + str(y) + ": " + "-".join([str(x) for x in sorted(current_daily_planning.currentlyAllocatedNephrologists(y))]))
        '''

        '''
        for x in Database.team():
            print(repr(x) + ": ")
            for holiday in sorted(month_planning.holidays[x.id]):
                print("\t" + str(holiday) + ": " + "|".join([y.name[0] for y in month_planning.holidays[x.id][holiday]]))

        print("------------------------------------------------------------")
        '''

        print(month_planning)

        month_planning.output()
    finally:
        pass

if __name__ == '__main__':
    main()