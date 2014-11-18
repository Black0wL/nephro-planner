__author__ = "Christophe"

from Enums.timeslot import TimeSlot
from Enums.activity import Activity


class Week():
    SLOTS = {
        0: {
            TimeSlot.FIRST_SHIFT.name: {
                Activity.DIALYSIS.name: None,
                Activity.NEPHROLOGY.name: None,
                Activity.OTHERS.name: None
            },
            TimeSlot.SECOND_SHIFT.name: {
                Activity.DIALYSIS.name: None,
                Activity.NEPHROLOGY.name: None,
                Activity.CONSULTATION.name: None
            },
            TimeSlot.THIRD_SHIFT.name: {
                Activity.OBLIGATION.name: None
            }
        },
        1: {
            TimeSlot.FIRST_SHIFT.name: {
                Activity.DIALYSIS.name: None,
                Activity.NEPHROLOGY.name: None,
                Activity.CONSULTATION.name: None
            },
            TimeSlot.SECOND_SHIFT.name: {
                Activity.DIALYSIS.name: None,
                Activity.NEPHROLOGY.name: None,
                Activity.CONSULTATION.name: None
            },
            TimeSlot.THIRD_SHIFT.name: {
                Activity.OBLIGATION.name: None
            }
        },
        2: {
            TimeSlot.FIRST_SHIFT.name: {
                Activity.DIALYSIS.name: None,
                Activity.NEPHROLOGY.name: None,
                Activity.CONSULTATION.name: None
            },
            TimeSlot.SECOND_SHIFT.name: {
                Activity.DIALYSIS.name: None,
                Activity.NEPHROLOGY.name: None,
                Activity.OTHERS.name: None
            },
            TimeSlot.THIRD_SHIFT.name: {
                Activity.OBLIGATION.name: None
            }
        },
        3: {
            TimeSlot.FIRST_SHIFT.name: {
                Activity.DIALYSIS.name: None,
                Activity.NEPHROLOGY.name: None,
                Activity.CONSULTATION.name: None
            },
            TimeSlot.SECOND_SHIFT.name: {
                Activity.DIALYSIS.name: None,
                Activity.NEPHROLOGY.name: None,
                Activity.CONSULTATION.name: None
            },
            TimeSlot.THIRD_SHIFT.name: {
                Activity.OBLIGATION.name: None
            }
        },
        4: {
            TimeSlot.FIRST_SHIFT.name: {
                Activity.DIALYSIS.name: None,
                Activity.NEPHROLOGY.name: None,
                Activity.OTHERS.name: None
            },
            TimeSlot.SECOND_SHIFT.name: {
                Activity.DIALYSIS.name: None,
                Activity.NEPHROLOGY.name: None,
                Activity.OTHERS.name: None
            },
            TimeSlot.THIRD_SHIFT.name: {
                Activity.OBLIGATION.name: None
            }
        },
        5: {
            TimeSlot.FIRST_SHIFT.name: {
                Activity.OBLIGATION_WEEKEND.name: None
            },
            TimeSlot.SECOND_SHIFT.name: {
                Activity.OBLIGATION_WEEKEND.name: None
            },
            TimeSlot.THIRD_SHIFT.name: {
                Activity.OBLIGATION_WEEKEND.name: None
            }
        },
        6: {
            TimeSlot.FIRST_SHIFT.name: {
                Activity.OBLIGATION_WEEKEND.name: None
            },
            TimeSlot.SECOND_SHIFT.name: {
                Activity.OBLIGATION_WEEKEND.name: None
            },
            TimeSlot.THIRD_SHIFT.name: {
                Activity.OBLIGATION_WEEKEND.name: None
            }
        },
        'SPECIAL_HOLIDAY': {
            TimeSlot.FIRST_SHIFT.name: {
                Activity.OBLIGATION_HOLIDAY.name: None
            },
            TimeSlot.SECOND_SHIFT.name: {
                Activity.OBLIGATION_HOLIDAY.name: None
            },
            TimeSlot.THIRD_SHIFT.name: {
                Activity.OBLIGATION_HOLIDAY.name: None
            }
        }
    }