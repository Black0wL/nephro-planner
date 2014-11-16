__author__ = "Christophe"

import os
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
from Utils.constants import Constants


class Parameters():
    filename = 'parameters.yaml'

    def __init__(self, _updateOnExit=False):
        if _updateOnExit:
            self.updateOnExit = _updateOnExit

    def __enter__(self):
        if not os.path.isfile(Parameters.filename) or os.stat(Parameters.filename)[6]==0:
            with open(Parameters.filename, 'w') as self.file:
                document = """
                    {}: 'data.db'
                """.format(Constants.DATABASE_FILENAME_KEY)
                self.file.write(dump(load(document), Dumper=Dumper))

        with open(Parameters.filename, 'r') as self.file:
            self.data = load(self.file.read(), Loader=Loader)

        return self

    def __exit__(self, type, value, traceback):
        if self.updateOnExit:
            with open(Parameters.filename, 'w') as self.file:
                self.file.write(dump(self.data, Dumper=Dumper))  # python will convert \n to os.linesep