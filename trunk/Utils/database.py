__author__ = "Christophe"


import sqlite3
from Utils.parameters import Parameters
from Utils.constants import Constants

class Database:
    DATABASE_TABLE_NEPHROLOGISTS = 'nephrologists'
    DATABASE_TABLE_NEPHROLOGISTS_HOLIDAYS = 'nephrologists_holidays'
    DATABASE_TABLE_NEPHROLOGISTS_PREFERENCES = 'nephrologists_preferences'
    DATABASE_TABLE_NEPHROLOGISTS_OBLIGATIONS = 'nephrologists_obligations'
    DATABASE_TABLE_MONTHLY_PLANNINGS = 'monthly_plannings'
    DATABASE_TABLE_MONTHLY_PLANNINGS_NEPHROLOGISTS = 'monthly_plannings_nephrologists'

    @classmethod
    def __load__(cls):
        with Parameters() as params, sqlite3.connect(params.data[Constants.DATABASE_FILENAME_KEY]) as connection:
            connection.execute('''CREATE TABLE IF NOT EXISTS {} (
                id_pk INTEGER NOT NULL,
                name TEXT NOT NULL UNIQUE,
                PRIMARY KEY(id_pk ASC)
            )'''.format(Database.DATABASE_TABLE_NEPHROLOGISTS))

            connection.execute('''CREATE TABLE IF NOT EXISTS {} (
                id_nephrologist_fk INTEGER NOT NULL,
                timespan BLOB NOT NULL,
                PRIMARY KEY(id_nephrologist_fk ASC, timespan ASC),
                FOREIGN KEY(id_nephrologist_fk) REFERENCES {}(id)
            )'''.format(
                Database.DATABASE_TABLE_NEPHROLOGISTS_HOLIDAYS,
                Database.DATABASE_TABLE_NEPHROLOGISTS
            ))

            connection.execute('''CREATE TABLE IF NOT EXISTS {} (
                id_nephrologist_fk INTEGER NOT NULL,
                timespan BLOB NOT NULL,
                PRIMARY KEY(id_nephrologist_fk ASC, timespan ASC),
                FOREIGN KEY(id_nephrologist_fk) REFERENCES {}(id)
            )'''.format(
                Database.DATABASE_TABLE_NEPHROLOGISTS_PREFERENCES,
                Database.DATABASE_TABLE_NEPHROLOGISTS
            ))

            connection.execute('''CREATE TABLE IF NOT EXISTS {} (
                id_nephrologist_fk INTEGER NOT NULL,
                timespan BLOB NOT NULL,
                PRIMARY KEY(id_nephrologist_fk ASC, timespan ASC),
                FOREIGN KEY(id_nephrologist_fk) REFERENCES {}(id)
            )'''.format(
                Database.DATABASE_TABLE_NEPHROLOGISTS_OBLIGATIONS,
                Database.DATABASE_TABLE_NEPHROLOGISTS
            ))

            connection.execute('''CREATE TABLE IF NOT EXISTS {} (
                month TEXT NOT NULL,
                version INTEGER NOT NULL,
                isReleasedVersion INTEGER NULL,
                PRIMARY KEY (month ASC, version ASC)
            )'''.format(Database.DATABASE_TABLE_MONTHLY_PLANNINGS))

            connection.execute('''CREATE TABLE IF NOT EXISTS {} (
                month_fk TEXT NOT NULL,
                version_fk INTEGER NOT NULL,
                id_nephrologist_fk INTEGER NOT NULL,
                activity_type INTEGER NOT NULL,
                activity_count INTEGER NOT NULL,
                PRIMARY KEY (month_fk ASC, version_fk ASC, id_nephrologist_fk ASC),
                FOREIGN KEY(month_fk, version_fk) REFERENCES {}(id),
                FOREIGN KEY(id_nephrologist_fk) REFERENCES {}(id)
            )'''.format(
                Database.DATABASE_TABLE_MONTHLY_PLANNINGS_NEPHROLOGISTS,
                Database.DATABASE_TABLE_MONTHLY_PLANNINGS,
                Database.DATABASE_TABLE_NEPHROLOGISTS
            ))