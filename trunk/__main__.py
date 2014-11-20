__author__ = "Christophe"

import calendar
import datetime
from Enums.timeslot import TimeSlot
from Enums.activity import Activity

PHYSICIANS = []
HOLIDAYS = []  # national day off
REPARTITION = {}
RULES = {}


def main():
    try:
        # from Models.nephrologist import Nephrologist
        # Database.__load__()
        # Nephrologist.__load__()
        '''
        from Models.monthly_planning import MonthlyPlanning
        MonthlyPlanning(1, 2014, 11)

        from Models.week import Week
        print(Week.SLOTS[0])
        print(Week.SLOTS[1])
        print(Week.SLOTS[2])
        print(Week.SLOTS[3])
        print(Week.SLOTS[4])
        print(Week.SLOTS[5])
        print(Week.SLOTS[6])
        '''
    finally:
        pass

def populate(yearNumber, monthNumber):
    firstLast = calendar.monthrange(yearNumber, monthNumber)
    for dayNumber in range(firstLast[0], firstLast[1] + 1):
        currentDay = datetime.datetime(yearNumber, monthNumber, dayNumber)
        dayOfWeek = currentDay.weekday()

        if (currentDay in HOLIDAYS and not (dayOfWeek == 5 or dayOfWeek == 6)):
            #allocation = random.choice(PHYSICIANS)
            allocatedResource = __getAvailablePhysician('ASTR_HOLIDAY', currentDay)

            REPARTITION[dayNumber] = Week.SLOTS['SPECIAL_HOLIDAY'].copy()
            REPARTITION[dayNumber][TimeSlot.FIRST_SHIFT.name][Activity.OBLIGATION.name] = allocatedResource
            REPARTITION[dayNumber][TimeSlot.SECOND_SHIFT.name][Activity.OBLIGATION.name] = allocatedResource
            REPARTITION[dayNumber][TimeSlot.THIRD_SHIFT.name][Activity.OBLIGATION.name] = allocatedResource
            allocatedResource.counters['ASTR_HOLIDAY'] += 1
            # this day is an offday
            # its potential activities are reverted to Activity.OBLIGATION
        else:
            REPARTITION[dayNumber] = Week.SLOTS[dayOfWeek].copy()
            if (dayOfWeek == 0): # monday
                REPARTITION[dayNumber][TimeSlot.FIRST_SHIFT][Activity.OBLIGATION] = allocatedResource
                REPARTITION[dayNumber][TimeSlot.SECOND_SHIFT][Activity.OBLIGATION] = allocatedResource
                REPARTITION[dayNumber][TimeSlot.THIRD_SHIFT][Activity.OBLIGATION] = allocatedResource
                pass
            elif (dayOfWeek == 1): # tuesday
                pass
            elif (dayOfWeek == 2): # wednesday
                pass
            elif (dayOfWeek == 3): # thursday
                pass
            elif (dayOfWeek == 4): # friday
                allocatedResource = __getAvailablePhysician('ASTR_WEEKEND', currentDay)

                REPARTITION[dayNumber] = Week.SLOTS[dayNumber].copy()
                # REPARTITION[dayNumber][Activity.OTHERS]
                REPARTITION[dayNumber + 1] = {
                    TimeSlot.ALL_WEEKEND : allocatedResource
                }
            elif (dayOfWeek == 5):
                pass
                # this day is saturday and is not taken care of
                # all decisions regarding Activity.ASTR_WEEKEND for Timeslot.ALL_WEEKEND are taken on day 4
                # which is friday...
            elif (dayOfWeek == 6):
                pass
                # this day is sunday and is not taken care of
                # it is part of a long Activity.ASTR_WEEKEND for Timeslot.ALL_WEEKEND
                # which starts at day 5...
            else:
                pass
                # it is a regular day

    # RULESET
        # severine DIALYSIS alloc --> ?
        # adeline DIALYSIS alloc --> ?
        # christine DIALYSIS alloc --> ?
        # alloc libre : lundi/mercredi/vendredi matin.
        # pas de DIALYSIS le dimanche
        # lors qu'il y a une OBLIGATION le weekend, le vendredi matin est OTHERS et le vendredi AM/lundi matin sont DIALYSIS
        # OBLIGATION holiday/weekend non-secables

def __getAvailablePhysician(counterName, currentDay):
    return sorted([physician for physician in PHYSICIANS if (currentDay not in physician.offDays)], key= lambda x: x.counters[counterName])[0]
    # fetching first physician that is not offday for current day and that is lagging behind in terms of counter for the specific category

if __name__ == '__main__':
    main()
