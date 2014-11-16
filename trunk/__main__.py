__author__ = "Christophe"

import calendar
import datetime
from Models.nephrologist import Nephrologist
from Models.week import Week
from Utils.parameters import Parameters
from Utils.connector import Connector
from Utils.constants import Constants
import sqlite3

PHYSICIANS = []
HOLIDAYS = []  # national day off
REPARTITION = {}
RULES = {}


def main():

        try:
            __init__()

            HOLIDAYS.append(datetime.datetime(2014, 7, 14))

            # populate(2014, 7)
        finally:
            pass
            # connector.__exit__()

def __init__():
    with Parameters(True) as params, sqlite3.connect(params.data[Constants.DATABASE_FILENAME_KEY]) as connection:
        connection.execute('''CREATE TABLE IF NOT EXISTS nephrologists (
            id INTEGER,
            name TEXT NOT NULL UNIQUE,
            holidays BLOB,
            preferences BLOB,
            obligations BLOB,
            PRIMARY KEY(id ASC)
        )''')

        connection.execute('''CREATE TABLE IF NOT EXISTS monthlyPlannings (
            month TEXT NOT NULL,
            version INTEGER NOT NULL,
            isReleasedVersion INTEGER NULL,
            PRIMARY KEY (month ASC, version ASC)
        )''')

        connection.commit()
    Nephrologist.__load__()

def populate(yearNumber, monthNumber):
    firstLast = calendar.monthrange(yearNumber, monthNumber)
    for dayNumber in range(firstLast[0], firstLast[1] + 1):
        currentDay = datetime.datetime(yearNumber, monthNumber, dayNumber)
        dayOfWeek = currentDay.weekday()

        if (currentDay in HOLIDAYS and not (dayOfWeek == 5 or dayOfWeek == 6)):
            #allocation = random.choice(PHYSICIANS)
            allocatedResource = __getAvailablePhysician('ASTR_HOLIDAY', currentDay)

            REPARTITION[dayNumber] = Week.SLOTS['SPECIAL_HOLIDAY'].copy()
            REPARTITION[dayNumber][Timeslot.FIRST_SHIFT][Activity.ASTR] = allocatedResource
            REPARTITION[dayNumber][Timeslot.SECOND_SHIFT][Activity.ASTR] = allocatedResource
            REPARTITION[dayNumber][Timeslot.THIRD_SHIFT][Activity.ASTR] = allocatedResource
            allocatedResource.counters['ASTR_HOLIDAY'] += 1
            # this day is an offday
            # its potential activities are reverted to Activity.ASTR
        else:
            REPARTITION[dayNumber] = Week.SLOTS[dayOfWeek].copy()
            if (dayOfWeek == 0): # monday
                REPARTITION[dayNumber][Timeslot.FIRST_SHIFT][Activity.ASTR] = allocatedResource
                REPARTITION[dayNumber][Timeslot.SECOND_SHIFT][Activity.ASTR] = allocatedResource
                REPARTITION[dayNumber][Timeslot.THIRD_SHIFT][Activity.ASTR] = allocatedResource
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
                REPARTITION[dayNumber][Activity.AA]
                REPARTITION[dayNumber + 1] = {
                    Timeslot.ALL_WEEKEND : allocatedResource
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
        # severine DIAL alloc --> ?
        # adeline DIAL alloc --> ?
        # christine DIAL alloc --> ?
        # alloc libre : lundi/mercredi/vendredi matin.
        # pas de DIAL le dimanche
        # lors qu'il y a une ASTR le weekend, le vendredi matin est AA et le vendredi AM/lundi matin sont DIAL
        # ASTR holiday/weekend non-secables

def __getAvailablePhysician(counterName, currentDay):
    return sorted([physician for physician in PHYSICIANS if (currentDay not in physician.offDays)], key= lambda x: x.counters[counterName])[0]
    # fetching first physician that is not offday for current day and that is lagging behind in terms of counter for the specific category

if __name__ == '__main__':
    main()
