__author__ = "Christophe"

from Enums.timeslot import TimeSlot
from Enums.activity import Activity

class Week():
    SLOTS = {
        0 : {
            TimeSlot.FIRST_SHIFT : {
                Activity.DIAL : None,
                Activity.NEPH : None,
                Activity.AA : None
            },
            TimeSlot.SECOND_SHIFT : {
                Activity.DIAL : None,
                Activity.NEPH : None,
                Activity.CP : None
            },
            TimeSlot.THIRD_SHIFT : {
                Activity.ASTR : None
            }
        },
        1 : {
            TimeSlot.FIRST_SHIFT : {
                Activity.DIAL : None,
                Activity.NEPH : None,
                Activity.CP : None
            },
            TimeSlot.SECOND_SHIFT : {
                Activity.DIAL : None,
                Activity.NEPH : None,
                Activity.CP : None
            },
            TimeSlot.THIRD_SHIFT : {
                Activity.ASTR : None
            }
        },
        2 : {
            TimeSlot.FIRST_SHIFT : {
                Activity.DIAL : None,
                Activity.NEPH : None,
                Activity.CP : None
            },
            TimeSlot.SECOND_SHIFT : {
                Activity.DIAL : None,
                Activity.NEPH : None,
                Activity.AA : None
            },
            TimeSlot.THIRD_SHIFT : {
                Activity.ASTR : None
            }
        },
        3 : {
            TimeSlot.FIRST_SHIFT : {
                Activity.DIAL : None,
                Activity.NEPH : None,
                Activity.CP : None
            },
            TimeSlot.SECOND_SHIFT : {
                Activity.DIAL : None,
                Activity.NEPH : None,
                Activity.CP : None
            },
            TimeSlot.THIRD_SHIFT : {
                Activity.ASTR : None
            }
        },
        4 : {
            TimeSlot.FIRST_SHIFT : {
                Activity.DIAL : None,
                Activity.NEPH : None,
                Activity.AA : None
            },
            TimeSlot.SECOND_SHIFT : {
                Activity.DIAL : None,
                Activity.NEPH : None,
                Activity.AA : None
            },
            TimeSlot.THIRD_SHIFT : {
                Activity.ASTR : None
            }
        },
        5 : {
            TimeSlot.FIRST_SHIFT : {
                Activity.ASTR : None
            },
            TimeSlot.SECOND_SHIFT : {
                Activity.ASTR : None
            },
            TimeSlot.THIRD_SHIFT : {
                Activity.ASTR : None
            }
        },
        6 : {
            TimeSlot.FIRST_SHIFT : {
                Activity.ASTR : None
            },
            TimeSlot.SECOND_SHIFT : {
                Activity.ASTR : None
            },
            TimeSlot.THIRD_SHIFT : {
                Activity.ASTR : None
            }
        },
        'SPECIAL_HOLIDAY': {
            TimeSlot.FIRST_SHIFT : {
                Activity.ASTR : None
            },
            TimeSlot.SECOND_SHIFT : {
                Activity.ASTR : None
            },
            TimeSlot.THIRD_SHIFT : {
                Activity.ASTR : None
            }
        }
    }