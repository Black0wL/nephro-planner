__author__ = "Christophe"


from Models.period import Period
from collections import Counter
from timedelta_extension import timedelta
from datetime import date
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
            _team = [
                Nephrologist(1, "Adeline", _preferences={
                    2: {  # wednesday
                        TimeSlot.FIRST_SHIFT: [Activity.CONSULTATION]
                    },
                    4: {  # friday
                        TimeSlot.SECOND_SHIFT: [Activity.CONSULTATION]
                    }
                }, _aversions={
                    1: {  # tuesday
                        TimeSlot.FIRST_SHIFT: [Activity.NEPHROLOGY],  # TODO: DELETE!
                        TimeSlot.THIRD_SHIFT: [Activity.OBLIGATION]
                    }
                }, _holidays=[
                ], _counters=Counter({
                    Activity.OBLIGATION: 13,
                    Activity.NEPHROLOGY: 9
                })),
                Nephrologist(2, "Christine", _preferences={
                    0: {  # monday
                        TimeSlot.FIRST_SHIFT: [
                            Activity.OTHERS,  # TODO: DELETE!
                            Activity.DIALYSIS  # TODO: DELETE!
                        ]
                    },
                    2: {  # wednesday
                        TimeSlot.SECOND_SHIFT: [
                            Activity.CONSULTATION,
                            Activity.OBLIGATION_RECOVERY
                        ]
                    },
                    3: {  # thursday
                        TimeSlot.THIRD_SHIFT: [Activity.OBLIGATION]
                    },
                    4: {  # friday
                        TimeSlot.FIRST_SHIFT: [Activity.CONSULTATION]
                    }
                }, _aversions={
                    2: {  # wednesday
                        TimeSlot.THIRD_SHIFT: [Activity.OBLIGATION]
                    }
                }, _counters=Counter({
                    Activity.OBLIGATION: 9,
                    Activity.NEPHROLOGY: 11
                })),
                Nephrologist(3, "Severine", _preferences={
                    0: {  # monday
                        TimeSlot.SECOND_SHIFT: [Activity.CONSULTATION]
                    },
                    1: {  # tuesday
                        TimeSlot.THIRD_SHIFT: [Activity.OBLIGATION]
                    },
                    2: {  # wednesday
                        TimeSlot.SECOND_SHIFT: [Activity.OBLIGATION_RECOVERY]
                    },
                    3: {  # thursday
                        TimeSlot.FIRST_SHIFT: [
                            Activity.CONSULTATION,
                            Activity.OBLIGATION_RECOVERY
                        ]
                    }
                }, _aversions={
                    0: {  # monday
                        TimeSlot.FIRST_SHIFT: [Activity.NEPHROLOGY],  # TODO: DELETE!
                        TimeSlot.THIRD_SHIFT: [Activity.OBLIGATION]
                    }
                }, _holidays=[
                    date(2014, 12, 7),  # TODO: DELETE!
                    Period(timedelta(days=10), timedelta(days=7, hours=10)),  # TODO: DELETE!
                    date(2014, 12, 5)  # TODO: DELETE!
                ], _counters=Counter({
                    Activity.OBLIGATION: 9,
                    Activity.NEPHROLOGY: 13
                })),
                Nephrologist(4, "Interne", _activities=[
                    Activity.NEPHROLOGY,
                    Activity.OTHERS,
                    Activity.OBLIGATION_RECOVERY
                ], _holidays=[
                    date(2014, 12, 2)  # TODO: DELETE!
                ], _counters=Counter({
                    Activity.NEPHROLOGY: 4,
                    Activity.OTHERS: 6
                }))
            ]
        return _team

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