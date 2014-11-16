__author__ = "Christophe"

class ParameterException(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(ParameterException, self).__init__(message)