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
    DATABASE_TABLE_MONTHLY_PLANNINGS_WEEKS_DAYS = 'monthly_plannings_weeks_days'
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
                PRIMARY KEY(id_nephrologist_fk, timespan),
                FOREIGN KEY(id_nephrologist_fk) REFERENCES {}(id)
            )'''.format(
                Database.DATABASE_TABLE_NEPHROLOGISTS_PREFERENCES,
                Database.DATABASE_TABLE_NEPHROLOGISTS
            ))

            connection.execute('''CREATE TABLE IF NOT EXISTS {} (
                id_nephrologist_fk INTEGER NOT NULL,
                timespan BLOB NOT NULL,
                PRIMARY KEY(id_nephrologist_fk, timespan),
                FOREIGN KEY(id_nephrologist_fk) REFERENCES {}(id)
            )'''.format(
                Database.DATABASE_TABLE_NEPHROLOGISTS_OBLIGATIONS,
                Database.DATABASE_TABLE_NEPHROLOGISTS
            ))

            COLUMN_YEAR_PK = 'year_pk'
            COLUMN_MONTH_PK = 'month_pk'
            COLUMN_VERSION_PK = 'version_pk'
            # TODO: don't forget to enforce unicity on rows {year, month} for column isReleasedVersion
            connection.execute('''CREATE TABLE IF NOT EXISTS {0} (
                {1} INTEGER NOT NULL,
                {2} TEXT NOT NULL,
                {3} INTEGER NOT NULL,
                isReleasedVersion INTEGER NULL,
                PRIMARY KEY({1}, {2}, {3})
            )'''.format(
                Database.DATABASE_TABLE_MONTHLY_PLANNINGS,
                COLUMN_YEAR_PK,
                COLUMN_MONTH_PK,
                COLUMN_VERSION_PK
            ))

            connection.execute('''CREATE TABLE IF NOT EXISTS {0} (
                {2} INTEGER NOT NULL,
                {3} INTEGER NOT NULL,
                {4} INTEGER NOT NULL,
                {5} INTEGER NOT NULL,
                {6} INTEGER NOT NULL,
                {7} INTEGER NOT NULL,
                {8} INTEGER NOT NULL,
                PRIMARY KEY({2}, {3}, {4}, {5}, {6}, {7}, {8}),
                FOREIGN KEY({4}, {5}, {6}) REFERENCES {1}({9}, {10}, {11})
            )'''.format(
                Database.DATABASE_TABLE_MONTHLY_PLANNINGS_WEEKS_DAYS,
                Database.DATABASE_TABLE_MONTHLY_PLANNINGS,
                'day_id_pk',  # TODO: how to deal with multispanning time_slot_types (ALL_WEEKEND)? nothing on day 6...
                'week_id_pk',
                'year_fk_pk',
                'month_fk_pk',
                'version_fk_pk',
                'time_slot_type',
                'activity_type',
                COLUMN_YEAR_PK,
                COLUMN_MONTH_PK,
                COLUMN_VERSION_PK
            ))

            connection.execute('''CREATE TABLE IF NOT EXISTS {} (
                year_fk INTEGER NOT NULL,
                month_fk INTEGER NOT NULL,
                version_fk INTEGER NOT NULL,
                id_nephrologist_fk INTEGER NOT NULL,
                timeslot_type INTEGER NOT NULL,
                activity_type INTEGER NOT NULL,
                activity_count INTEGER NOT NULL,
                PRIMARY KEY(year_fk ASC, month_fk ASC, version_fk ASC, id_nephrologist_fk ASC),
                FOREIGN KEY(year_fk ASC, month_fk, version_fk) REFERENCES {}(year_pk, month_pk, version_pk),
                FOREIGN KEY(id_nephrologist_fk) REFERENCES {}(id)
            )'''.format(
                Database.DATABASE_TABLE_MONTHLY_PLANNINGS_NEPHROLOGISTS,
                Database.DATABASE_TABLE_MONTHLY_PLANNINGS,
                Database.DATABASE_TABLE_NEPHROLOGISTS
            ))