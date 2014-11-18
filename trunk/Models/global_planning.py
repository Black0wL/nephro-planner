__author__ = "Christophe"

import sqlite3
from Utils.parameters import Parameters
from Utils.constants import Constants
from Utils.database import Database


def singleton(cls):
    instances = {}
    def __new__():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return __new__


@singleton
class GlobalPlanning():
    def __init__(self):
        pass

    def __load__(self, _year, _month):
        with Parameters() as params, sqlite3.connect(params.data[Constants.DATABASE_FILENAME_KEY]) as connection:
            connection.execute('''
                SELECT

                FROM {} (
                WHERE
                    isReleasedVersion = 1
                    AND (12 * year + month) < {}
            )'''.format(
                Database.DATABASE_TABLE_MONTHLY_PLANNINGS_NEPHROLOGISTS,
                (12 * _year + _month)
            ))

'''
s1=GlobalPlanning()
print(id(s1))
s2=GlobalPlanning()
print(id(s2))
if(id(s1)==id(s2)):
    print "Same"
else:
    print "Different"
'''