__author__ = "Christophe"

from base import Base


class TimeSlot(Base):
    NONE = 0
    FIRST_SHIFT = 1 << 0
    SECOND_SHIFT = 1 << 1
    THIRD_SHIFT = 1 << 2
    # ALL_DAY = 1 << 3
    # ALL_WEEKEND = 1 << 4

# FIRST_SHIFT_BOUNDARY_MIN = 5
# SECOND_SHIFT_BOUNDARY_MIN = 13
# THIRD_SHIFT_BOUNDARY_MIN = 21

# print(TimeSlot.FIRST_SHIFT.value)
# print(TimeSlot.SECOND_SHIFT.value)
# print(TimeSlot.THIRD_SHIFT.value)
# print(TimeSlot.contains(2, 5))