from Models.Enums.timeslot import Timeslot
from Models.Enums.activity import Activity

__author__ = "Christophe"

class Week():
    SLOTS = {
        0 : {
            Timeslot.FIRST_SHIFT : {
                Activity.DIAL : None,
                Activity.NEPH : None,
                Activity.AA : None
            },
            Timeslot.SECOND_SHIFT : {
                Activity.DIAL : None,
                Activity.NEPH : None,
                Activity.CP : None
            },
            Timeslot.THIRD_SHIFT : {
                Activity.ASTR : None
            }
        },
        1 : {
            Timeslot.FIRST_SHIFT : {
                Activity.DIAL : None,
                Activity.NEPH : None,
                Activity.CP : None
            },
            Timeslot.SECOND_SHIFT : {
                Activity.DIAL : None,
                Activity.NEPH : None,
                Activity.CP : None
            },
            Timeslot.THIRD_SHIFT : {
                Activity.ASTR : None
            }
        },
        2 : {
            Timeslot.FIRST_SHIFT : {
                Activity.DIAL : None,
                Activity.NEPH : None,
                Activity.CP : None
            },
            Timeslot.SECOND_SHIFT : {
                Activity.DIAL : None,
                Activity.NEPH : None,
                Activity.AA : None
            },
            Timeslot.THIRD_SHIFT : {
                Activity.ASTR : None
            }
        },
        3 : {
            Timeslot.FIRST_SHIFT : {
                Activity.DIAL : None,
                Activity.NEPH : None,
                Activity.CP : None
            },
            Timeslot.SECOND_SHIFT : {
                Activity.DIAL : None,
                Activity.NEPH : None,
                Activity.CP : None
            },
            Timeslot.THIRD_SHIFT : {
                Activity.ASTR : None
            }
        },
        4 : {
            Timeslot.FIRST_SHIFT : {
                Activity.DIAL : None,
                Activity.NEPH : None,
                Activity.AA : None
            },
            Timeslot.SECOND_SHIFT : {
                Activity.DIAL : None,
                Activity.NEPH : None,
                Activity.AA : None
            },
            Timeslot.THIRD_SHIFT : {
                Activity.ASTR : None
            }
        },
        5 : {
            Timeslot.FIRST_SHIFT : {
                Activity.ASTR : None
            },
            Timeslot.SECOND_SHIFT : {
                Activity.ASTR : None
            },
            Timeslot.THIRD_SHIFT : {
                Activity.ASTR : None
            }
        },
        6 : {
            Timeslot.FIRST_SHIFT : {
                Activity.ASTR : None
            },
            Timeslot.SECOND_SHIFT : {
                Activity.ASTR : None
            },
            Timeslot.THIRD_SHIFT : {
                Activity.ASTR : None
            }
        },
        'SPECIAL_HOLIDAY': {
            Timeslot.FIRST_SHIFT : {
                Activity.ASTR : None
            },
            Timeslot.SECOND_SHIFT : {
                Activity.ASTR : None
            },
            Timeslot.THIRD_SHIFT : {
                Activity.ASTR : None
            }
        }
    }