__author__ = "Christophe"

from Enums.timeslot import TimeSlot
from Enums.activity import Activity


class Week():
    KEY_SPECIAL_HOLIDAY = 'SPECIAL_HOLIDAY'
    SLOTS = {
        0: {
            TimeSlot.FIRST_SHIFT: {
                Activity.DIALYSIS: None,
                Activity.NEPHROLOGY: None,
                Activity.OTHERS: None
            },
            TimeSlot.SECOND_SHIFT: {
                Activity.DIALYSIS: None,
                Activity.NEPHROLOGY: None,
                Activity.CONSULTATION: None
            },
            TimeSlot.THIRD_SHIFT: {
                Activity.OBLIGATION: None
            }
        },
        1: {
            TimeSlot.FIRST_SHIFT: {
                Activity.DIALYSIS: None,
                Activity.NEPHROLOGY: None,
                Activity.CONSULTATION: None
            },
            TimeSlot.SECOND_SHIFT: {
                Activity.DIALYSIS: None,
                Activity.NEPHROLOGY: None,
                Activity.CONSULTATION: None
            },
            TimeSlot.THIRD_SHIFT: {
                Activity.OBLIGATION: None
            }
        },
        2: {
            TimeSlot.FIRST_SHIFT: {
                Activity.DIALYSIS: None,
                Activity.NEPHROLOGY: None,
                Activity.CONSULTATION: None
            },
            TimeSlot.SECOND_SHIFT: {
                Activity.DIALYSIS: None,
                Activity.NEPHROLOGY: None,
                Activity.OTHERS: None
            },
            TimeSlot.THIRD_SHIFT: {
                Activity.OBLIGATION.name: None
            }
        },
        3: {
            TimeSlot.FIRST_SHIFT: {
                Activity.DIALYSIS: None,
                Activity.NEPHROLOGY: None,
                Activity.CONSULTATION: None
            },
            TimeSlot.SECOND_SHIFT: {
                Activity.DIALYSIS: None,
                Activity.NEPHROLOGY: None,
                Activity.CONSULTATION: None
            },
            TimeSlot.THIRD_SHIFT: {
                Activity.OBLIGATION: None
            }
        },
        4: {
            TimeSlot.FIRST_SHIFT: {
                Activity.DIALYSIS: None,
                Activity.NEPHROLOGY: None,
                Activity.OTHERS: None
            },
            TimeSlot.SECOND_SHIFT: {
                Activity.DIALYSIS: None,
                Activity.NEPHROLOGY: None,
                Activity.OTHERS: None
            },
            TimeSlot.THIRD_SHIFT: {
                Activity.OBLIGATION: None
            }
        },
        5: {
            TimeSlot.FIRST_SHIFT: {
                Activity.OBLIGATION_WEEKEND: None
            },
            TimeSlot.SECOND_SHIFT: {
                Activity.OBLIGATION_WEEKEND: None
            },
            TimeSlot.THIRD_SHIFT: {
                Activity.OBLIGATION_WEEKEND: None
            }
        },
        6: {
            TimeSlot.FIRST_SHIFT: {
                Activity.OBLIGATION_WEEKEND: None
            },
            TimeSlot.SECOND_SHIFT: {
                Activity.OBLIGATION_WEEKEND: None
            },
            TimeSlot.THIRD_SHIFT: {
                Activity.OBLIGATION_WEEKEND: None
            }
        },
        KEY_SPECIAL_HOLIDAY: {  # can replace DAY 0, 1, 2, 3, 4 if holiday (but never 5, 6)
            TimeSlot.FIRST_SHIFT: {
                Activity.OBLIGATION_HOLIDAY: None
            },
            TimeSlot.SECOND_SHIFT: {
                Activity.OBLIGATION_HOLIDAY: None
            },
            TimeSlot.THIRD_SHIFT: {
                Activity.OBLIGATION_HOLIDAY: None
            }
        }
    }