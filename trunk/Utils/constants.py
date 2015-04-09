__author__ = "Christophe"

from datetime import timedelta
from Enums.timeslot import TimeSlot


class Constants:
    DATABASE_FILENAME_KEY = 'databaseFilename'

    FIRST_SHIFT_LOWER_BOUND = 5
    SECOND_SHIFT_LOWER_BOUND = 13
    THIRD_SHIFT_LOWER_BOUND = 21
    """ mapper between discrete time slots and analogous datetime

        FIRST_SHIFT: from 05:00:00 to 12:59:59.999999
        SECOND_SHIFT: from 13:00:00 to 20:59:59.999999
        THIRD_SHIFT: from 21:00:00 to 04:59:59.999999
    """
    slots_temporally = {
        TimeSlot.FIRST_SHIFT: (
            timedelta(hours=FIRST_SHIFT_LOWER_BOUND),
            timedelta(hours=SECOND_SHIFT_LOWER_BOUND, microseconds=-1)
        ),
        TimeSlot.SECOND_SHIFT: (
            timedelta(hours=SECOND_SHIFT_LOWER_BOUND),
            timedelta(hours=THIRD_SHIFT_LOWER_BOUND, microseconds=-1)
        ),
        TimeSlot.THIRD_SHIFT: (
            timedelta(hours=THIRD_SHIFT_LOWER_BOUND),
            timedelta(days=1, hours=FIRST_SHIFT_LOWER_BOUND, microseconds=-1)
        )
    }