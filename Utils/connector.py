__author__ = "Christophe"

import sqlite3


class Connector():
    connection = None

    def __init__(self, databaseFilename):
        connection = sqlite3.connect(databaseFilename)

    def __enter__(self, databaseFilename):
        self.__init__(databaseFilename)

    def __exit__(self, type, value, traceback):
        self.connection.close()