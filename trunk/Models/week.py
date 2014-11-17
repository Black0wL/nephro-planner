__author__ = "Christophe"

from Enums.timeslot import TimeSlot
from Enums.activity import Activity

class Week():
    SLOTS = {
        0 : {
            TimeSlot.FIRST_SHIFT : {
                Activity.DIALYSIS : None,
                Activity.NEPHROLOGY : None,
                Activity.OTHERS : None
            },
            TimeSlot.SECOND_SHIFT : {
                Activity.DIALYSIS : None,
                Activity.NEPHROLOGY : None,
                Activity.CONSULTATION : None
            },
            TimeSlot.THIRD_SHIFT : {
                Activity.OBLIGATION : None
            }
        },
        1 : {
            TimeSlot.FIRST_SHIFT : {
                Activity.DIALYSIS : None,
                Activity.NEPHROLOGY : None,
                Activity.CONSULTATION : None
            },
            TimeSlot.SECOND_SHIFT : {
                Activity.DIALYSIS : None,
                Activity.NEPHROLOGY : None,
                Activity.CONSULTATION : None
            },
            TimeSlot.THIRD_SHIFT : {
                Activity.OBLIGATION : None
            }
        },
        2 : {
            TimeSlot.FIRST_SHIFT : {
                Activity.DIALYSIS : None,
                Activity.NEPHROLOGY : None,
                Activity.CONSULTATION : None
            },
            TimeSlot.SECOND_SHIFT : {
                Activity.DIALYSIS : None,
                Activity.NEPHROLOGY : None,
                Activity.OTHERS : None
            },
            TimeSlot.THIRD_SHIFT : {
                Activity.OBLIGATION : None
            }
        },
        3 : {
            TimeSlot.FIRST_SHIFT : {
                Activity.DIALYSIS : None,
                Activity.NEPHROLOGY : None,
                Activity.CONSULTATION : None
            },
            TimeSlot.SECOND_SHIFT : {
                Activity.DIALYSIS : None,
                Activity.NEPHROLOGY : None,
                Activity.CONSULTATION : None
            },
            TimeSlot.THIRD_SHIFT : {
                Activity.OBLIGATION : None
            }
        },
        4 : {
            TimeSlot.FIRST_SHIFT : {
                Activity.DIALYSIS : None,
                Activity.NEPHROLOGY : None,
                Activity.OTHERS : None
            },
            TimeSlot.SECOND_SHIFT : {
                Activity.DIALYSIS : None,
                Activity.NEPHROLOGY : None,
                Activity.OTHERS : None
            },
            TimeSlot.THIRD_SHIFT : {
                Activity.OBLIGATION : None
            }
        },
        5 : {
            TimeSlot.FIRST_SHIFT : {
                Activity.OBLIGATION_WEEKEND : None
            },
            TimeSlot.SECOND_SHIFT : {
                Activity.OBLIGATION_WEEKEND : None
            },
            TimeSlot.THIRD_SHIFT : {
                Activity.OBLIGATION_WEEKEND : None
            }
        },
        6 : {
            TimeSlot.FIRST_SHIFT : {
                Activity.OBLIGATION_WEEKEND : None
            },
            TimeSlot.SECOND_SHIFT : {
                Activity.OBLIGATION_WEEKEND : None
            },
            TimeSlot.THIRD_SHIFT : {
                Activity.OBLIGATION_WEEKEND : None
            }
        },
        'SPECIAL_HOLIDAY': {
            TimeSlot.FIRST_SHIFT : {
                Activity.OBLIGATION_HOLIDAY : None
            },
            TimeSlot.SECOND_SHIFT : {
                Activity.OBLIGATION_HOLIDAY : None
            },
            TimeSlot.THIRD_SHIFT : {
                Activity.OBLIGATION_HOLIDAY : None
            }
        }
    }