__author__ = "Christophe"


import sqlite3
from Utils.parameters import Parameters
from Utils.constants import Constants
from Models.nephrologist import Nephrologist

class Database:
    DATABASE_TABLE_NEPHROLOGISTS = 'nephrologists'
    DATABASE_TABLE_NEPHROLOGISTS_HOLIDAYS = 'nephrologists_holidays'
    DATABASE_TABLE_NEPHROLOGISTS_PREFERENCES = 'nephrologists_preferences'
    DATABASE_TABLE_MONTHLY_PLANNINGS = 'monthly_plannings'

    @classmethod
    def __load__(cls):
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
                ), [
                    Nephrologist(1, "Sandrine"),
                    Nephrologist(2, "Christine"),
                    Nephrologist(3, "Severine")
                ].__iter__())
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