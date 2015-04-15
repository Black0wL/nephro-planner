__author__ = "Christophe"
# -*- coding: utf-8 -*-


from Models.date_duration import DateDuration
from Models.sporadic_occurrence import SporadicOccurrence
from collections import Counter
from datetime import date
from Utils.timedelta_extension import timedelta
from Enums.activity import Activity
from Enums.timeslot import TimeSlot
import sqlite3
from constants import Constants
from parameters import Parameters


class Database:
    _team = None
    DATABASE_TABLE_NEPHROLOGISTS = 'nephrologists'
    DATABASE_TABLE_NEPHROLOGISTS_HOLIDAYS = 'nephrologists_holidays'
    DATABASE_TABLE_NEPHROLOGISTS_PREFERENCES = 'nephrologists_preferences'
    DATABASE_TABLE_MONTHLY_PLANNINGS = 'monthly_plannings'

    # TODO: check if not same activity/time slot combo in aversions and preferences on the same time...
    @classmethod
    def team(cls):
        from Models.nephrologist import Nephrologist
        if not Database._team:
            Database._team = [
                Nephrologist(1, "Adeline", _preferences={
                    2: {  # wednesday
                        TimeSlot.FIRST_SHIFT: [
                            Activity.CONSULTATION
                        ]
                    },
                    4: {  # friday
                        TimeSlot.SECOND_SHIFT: [
                            Activity.CONSULTATION
                        ]
                    }
                }, _aversions={
                    0: {  # monday
                        TimeSlot.FIRST_SHIFT: [
                            # Activity.OBLIGATION_RECOVERY  # TODO: DELETE!
                        ],
                        TimeSlot.SECOND_SHIFT: [
                            # Activity.OBLIGATION_RECOVERY  # TODO: DELETE!
                        ]
                    },
                    1: {  # tuesday
                        TimeSlot.FIRST_SHIFT: [
                            # Activity.NEPHROLOGY  # TODO: DELETE!
                        ],
                        TimeSlot.THIRD_SHIFT: [
                            Activity.OBLIGATION
                        ]
                    }
                }, _holidays=[
                ], _counters=Counter({
                    # Activity.OBLIGATION: 13,  # TODO: DELETE!
                    # Activity.NEPHROLOGY: 9  # TODO: DELETE!
                })),
                Nephrologist(2, "Christine", _preferences={
                    0: {  # monday
                        TimeSlot.FIRST_SHIFT: [
                            # Activity.OTHERS,  # TODO: DELETE!
                            # Activity.DIALYSIS  # TODO: DELETE!
                        ]
                    },
                    2: {  # wednesday
                        TimeSlot.SECOND_SHIFT: [
                            Activity.CONSULTATION,
                            Activity.OBLIGATION_RECOVERY
                        ]
                    },
                    3: {  # thursday
                        TimeSlot.THIRD_SHIFT: [
                            Activity.OBLIGATION
                        ]
                    },
                    4: {  # friday
                        TimeSlot.FIRST_SHIFT: [
                            Activity.CONSULTATION
                        ]
                    }
                }, _aversions={
                    2: {  # wednesday
                        TimeSlot.THIRD_SHIFT: [
                            Activity.OBLIGATION
                        ]
                    }
                }, _counters=Counter({
                    # Activity.OBLIGATION: 9,  # TODO: DELETE!
                    # Activity.NEPHROLOGY: 11  # TODO: DELETE!
                })),
                Nephrologist(3, "Séverine", _preferences={
                    0: {  # monday
                        TimeSlot.SECOND_SHIFT: [
                            Activity.CONSULTATION
                        ]
                    },
                    1: {  # tuesday
                        TimeSlot.THIRD_SHIFT: [
                            Activity.OBLIGATION
                        ]
                    },
                    2: {  # wednesday
                        TimeSlot.SECOND_SHIFT: [
                            Activity.OBLIGATION_RECOVERY
                        ]
                    },
                    3: {  # thursday
                        TimeSlot.FIRST_SHIFT: [
                            Activity.CONSULTATION,
                            Activity.OBLIGATION_RECOVERY
                        ]
                    }
                }, _aversions={
                    0: {  # monday
                        TimeSlot.FIRST_SHIFT: [
                            # Activity.NEPHROLOGY  # TODO: DELETE!
                        ],
                        TimeSlot.THIRD_SHIFT: [
                            Activity.OBLIGATION
                        ]
                    }
                }, _holidays=[
                    # date(2014, 12, 5),  # TODO: DELETE!
                    # date(2014, 12, 7),  # TODO: DELETE!
                    # SporadicOccurrence(timedelta(days=3), timedelta(days=7)),  # TODO: DELETE!
                    # DateDuration(_lower_date=date(2014, 12, 25), _upper_date=date(2015, 1, 7))  # TODO: DELETE!
                ], _counters=Counter({
                    # Activity.OBLIGATION_WEEKEND: 7,  # TODO: DELETE!
                    # Activity.NEPHROLOGY: 13  # TODO: DELETE!
                })),
                Nephrologist(4, "Nouvelle Recrue"),
                Nephrologist(5, "Interne", _activities=[
                    Activity.NEPHROLOGY,
                    Activity.OTHERS
                ], _holidays=[
                    # date(2014, 12, 2)  # TODO: DELETE!
                ], _counters=Counter({
                    # Activity.NEPHROLOGY: 14,  # TODO: DELETE!
                    # Activity.OBLIGATION: 19,  # TODO: DELETE!
                    # Activity.OTHERS: 6  # TODO: DELETE!
                }))
            ]
        return Database._team

    @classmethod
    def __create__(cls):
        with Parameters() as params, sqlite3.connect(params.data[Constants.DATABASE_FILENAME_KEY]) as connection:
            connection.execute('''CREATE TABLE IF NOT EXISTS {} (
                id_pk INTEGER NOT NULL,
                name TEXT NOT NULL UNIQUE,
                PRIMARY KEY(id_pk ASC)
            )'''.format(Database.DATABASE_TABLE_NEPHROLOGISTS))

            # insert nephrologists
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM {}".format(Database.DATABASE_TABLE_NEPHROLOGISTS))
            if cursor.rowcount == 0:
                cursor.executemany('INSERT INTO {}(id_pk, name) VALUES (?,?)'.format(
                    Database.DATABASE_TABLE_NEPHROLOGISTS
                ), [((x.id, x.name) for x in cls.team())].__iter__())  # does it even work?
                connection.commit()

            connection.execute('''CREATE TABLE IF NOT EXISTS {} (
                id_nephrologist_fk INTEGER NOT NULL,
                timespan BLOB NOT NULL,
                PRIMARY KEY(id_nephrologist_fk ASC, timespan ASC),
                FOREIGN KEY(id_nephrologist_fk) REFERENCES {}(id_pk)
            )'''.format(
                Database.DATABASE_TABLE_NEPHROLOGISTS_HOLIDAYS,
                Database.DATABASE_TABLE_NEPHROLOGISTS
            ))

            # TODO: add nephrologists holidays!

            connection.execute('''CREATE TABLE IF NOT EXISTS {} (
                id_nephrologist_fk INTEGER NOT NULL,
                timespan BLOB NOT NULL,
                time_slot_type INTEGER NULL,
                activity_type INTEGER NULL,
                PRIMARY KEY(id_nephrologist_fk, timespan),
                FOREIGN KEY(id_nephrologist_fk) REFERENCES {}(id_pk)
            )'''.format(
                Database.DATABASE_TABLE_NEPHROLOGISTS_PREFERENCES,
                Database.DATABASE_TABLE_NEPHROLOGISTS
            ))

            # TODO: modify table schema (or TimeSpan instance fields) + add nephrologists preferences!

            connection.execute('''CREATE TABLE IF NOT EXISTS {} (
                date_pk TEXT NOT NULL,
                time_slot_type_pk INTEGER NOT NULL,
                activity_type INTEGER NOT NULL,
                id_nephrologist_fk INTEGER NOT NULL,
                PRIMARY KEY(date_pk, time_slot_type_pk, activity_type, id_nephrologist_fk),
                FOREIGN KEY(id_nephrologist_fk) REFERENCES {}(id_pk)
            )'''.format(
                Database.DATABASE_TABLE_MONTHLY_PLANNINGS,
                Database.DATABASE_TABLE_NEPHROLOGISTS
            ))